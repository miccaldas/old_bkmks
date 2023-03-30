"""
Prepares the page where the results of a search will be shown.
"""
import os
import pickle
import subprocess

import snoop
from configs.config import tput_config
from mysql.connector import Error, connect
from question_template import question_template
from snoop import pp


def type_watch(source, value):
    return "type({})".format(source), type(value)


snoop.install(out="snoop.log", overwrite=True, watch_extras=[type_watch])


@snoop
def search_output_page():
    """
    Called by 'search_db_call',
    creates page template for
    search results.
    """

    with open(
        "/home/mic/python/bkmk/bkmk/search_results.bin", "rb"
    ) as f:
        results = pickle.load(f)

    cnf = tput_config()
    text = "SEARCH RESULTS"
    title_width = int(
        cnf["init_width"] + (len(cnf["separator"]) / 2) - (len(f"{text}") / 2)
        )

    with open("search_results.bash", "w") as f:
        f.write("#!/usr/bin/env bash\n\n")
        f.write("tput clear\n\n")
        f.write(f"tput cup {cnf['init_height']} {title_width}\n")
        f.write(f"tput setaf {cnf['title_color']}\n")
        f.write("tput bold\n")
        f.write(f"echo {text}\n")
        f.write("tput sgr0\n")
        f.write(f"tput cup {cnf['separator_height']} {cnf['init_width']}\n")
        f.write(f"echo '{cnf['separator']}'\n")
        for i in range(len(results)):
            f.write("tput bold\n")
            # The way the page was consructed was that each entry set would know the
            # last height position used, so as to be able to start printing after that
            # value. The first entry has no past, so it had to be dealt separately.
            if i == 0:
                new_length = len(results[i])
                rng = range(new_length)
                # List with all the numbers of rng range.
                rng_lst = [int(r) for r in rng]
                f.write(f"tput cup {cnf['separator_height'] + 2} {cnf['init_width']}\n")
                f.write(f"echo 'ID -> {results[i][0]}'\n")
                f.write(f"tput cup {cnf['separator_height'] + 3} {cnf['init_width']}\n")
                f.write(f'echo "Title -> {results[i][1]}"\n')
                f.write(f"tput cup {cnf['separator_height'] + 4} {cnf['init_width']}\n")
                f.write(f'echo "Comment -> {results[i][2]}"\n')
                f.write(f"tput cup {cnf['separator_height'] + 5} {cnf['init_width']}\n")
                f.write("tput setaf 2\n")
                f.write(f'echo "Link -> {results[i][3]}"\n')
                f.write("tput sgr0\n")
                f.write(f"tput cup {cnf['separator_height'] + 6} {cnf['init_width']}\n")
                f.write(f'echo "K1 -> {results[i][4]}"\n')
                f.write(f"tput cup {cnf['separator_height'] + 7} {cnf['init_width']}\n")
                f.write(f'echo "K2 -> {results[i][5]}"\n')
                f.write(f"tput cup {cnf['separator_height'] + 8} {cnf['init_width']}\n")
                f.write(f'echo "K3 -> {results[i][6]}"\n')
                f.write(f"tput cup {cnf['separator_height'] + 9} {cnf['init_width']}\n")
                f.write(f'echo "Time -> {results[i][7]}"\n\n\n')
            else:
                f.write('echo " "\n')
                f.write(
                    f"tput cup {cnf['separator_height'] + 11 * i + 1} {cnf['init_width']}\n"
                )
                f.write(f"echo 'ID -> {results[i][0]}'\n")
                f.write(
                    f"tput cup {cnf['separator_height'] + 11 * i + 2} {cnf['init_width']}\n"
                )
                f.write(f'echo "Title -> {results[i][1]}"\n')
                f.write(
                    f"tput cup {cnf['separator_height'] + 11 * i + 3} {cnf['init_width']}\n"
                )
                f.write(f'echo "Comment -> {results[i][2]}"\n')
                f.write(
                    f"tput cup {cnf['separator_height'] + 11 * i + 4} {cnf['init_width']}\n"
                )
                f.write("tput setaf 2\n")
                f.write(f'echo "Link -> {results[i][3]}"\n')
                f.write("tput sgr0\n")
                f.write(
                    f"tput cup {cnf['separator_height'] + 11 * i + 5} {cnf['init_width']}\n"
                )
                f.write(f'echo "K1 -> {results[i][4]}"\n')
                f.write(
                    f"tput cup {cnf['separator_height'] + 11 * i + 6} {cnf['init_width']}\n"
                )
                f.write(f'echo "K2 -> {results[i][5]}"\n')
                f.write(
                    f"tput cup {cnf['separator_height'] + 11 * i + 7} {cnf['init_width']}\n"
                )
                f.write(f'echo "K3 -> {results[i][6]}"\n')
                f.write(
                    f"tput cup {cnf['separator_height'] + 11 * i + 8} {cnf['init_width']}\n"
                )
                f.write(f'echo "Time -> {results[i][7]}"\n\n\n')

        f.write("echo ' '\n")
        f.write(f"tput cup 120 {cnf['init_width']}\n")
        f.write("read -p 'Did you find what you wanted?[y/n]: ' choice\n")
        f.write('echo "${choice}" > ')
        f.write("search_results_choice.txt\n\n")
        f.write("clear\n")
        f.write("tput sgr0\n")
        f.write("tput rc")

    subprocess.run("sudo chmod +x search_results.bash", cwd=os.getcwd(), shell=True)
    subprocess.run("./search_results.bash", cwd=os.getcwd(), shell=True)


@snoop
def search_db_call(answers):
    """
    Database call for search for bookmark.
    Called by 'call_search'
    """

    q1 = "SELECT id, title, comment, link, k1, k2, k3, tempo "
    q2 = "FROM bkmks WHERE MATCH(title, comment, k1, k2, k3) "
    q3 = f"AGAINST('{answers[0]}')"

    try:
        conn = connect(host="localhost", user="mic", password="xxxx", database="bkmks")
        cur = conn.cursor()
        query = f"{q1}{q2}{q3}"
        cur.execute(query)
        records = cur.fetchall()
        with open("search_results.bin", "wb") as f:
            pickle.dump(records, f)
        conn.close()
    except Error as e:
        err_msg = "Error while connecting to db", e
        print("Error while connecting to db", e)
        if err_msg:
            return query, err_msg

    return query


@snoop
def call_search():
    """
    Calls the other functions in the module.
    Called by 'main.py'
    """

    question_template("search", "What are you searching for?")
    with open("search_choice.txt", "r") as f:
        dirty_search = f.read()
        search = dirty_search.strip()
        answers = [search]
    search_db_call(answers)
    search_output_page()
