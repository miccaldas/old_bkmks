"""
All the functions pertaining to showing the entirety of the database.
"""
import os
import pickle
import subprocess

import snoop
from mysql.connector import Error, connect
from snoop import pp


def type_watch(source, value):
    return "type({})".format(source), type(value)


snoop.install(out="snoop.log", overwrite=True, watch_extras=[type_watch])


# @snoop
def see_db_call():
    """
    Call to see all of the
    database. Called by
    'call_see'. Tput has a
    problem with ticks, so
    we have to make sure
    they're deleted from the
    output.
    """
    try:
        conn = connect(host="localhost", user="mic", password="xxxx", database="bkmks")
        cur = conn.cursor()
        query = "SELECT * FROM bkmks"
        cur.execute(query)
        rec = cur.fetchall()
        reco = [
            (
                i,
                l.replace('"', ""),
                m.replace('"', ""),
                n.replace('"', ""),
                o,
                p,
                q,
                t,
            )
            for i, l, m, n, o, p, q, t in rec
        ]
        records = [
            (
                i,
                l.replace("'", ""),
                m.replace("'", ""),
                n.replace("'", ""),
                o,
                p,
                q,
                t,
            )
            for i, l, m, n, o, p, q, t in rec
        ]

        with open("see_results.bin", "wb") as f:
            pickle.dump(reco, f)
        conn.close()
    except Error as e:
        err_msg = "Error while connecting to db", e
        print("Error while connecting to db", e)
        if err_msg:
            return query, err_msg

    return query


# @snoop
def see_output_page():
    """
    Creates page template to
    see all of the database
    content.
    Called by 'call_see'
    """

    with open("/home/mic/python/bkmk/bkmk/see_results.bin", "rb") as f:
        results = pickle.load(f)

    terminal_size = os.get_terminal_size()
    height = terminal_size.lines
    width = terminal_size.columns
    text = "SEARCH RESULTS"
    init_height = int(height / 3)
    init_width = 10
    init_pos = f"{init_height} {init_width}"
    separator_height = int(init_height + 2)
    separator = "--------- [X] ---------"
    separator_width = init_width
    space_under_separator = len(results) * 9 + 3
    choice_width = init_width
    title_color = 2

    with open("see.bash", "w") as f:
        f.write("#!/usr/bin/env bash\n\n")
        f.write("tput clear\n\n")
        f.write(f"tput cup {init_pos}\n")
        f.write(f"tput setaf {title_color}\n")
        f.write("tput bold\n")
        f.write(f"echo {text}\n")
        f.write("tput sgr0\n")
        f.write(f"tput cup {separator_height} {separator_width}\n")
        f.write(f"echo '{separator}'\n")
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
                f.write(
                    f"tput cup {separator_height + (rng_lst[0] + 2)} {choice_width + 2}\n"
                )
                f.write(f"echo 'ID. {results[i][0]}'\n")
                f.write(
                    f"tput cup {separator_height + (rng_lst[1] + 2)} {choice_width + 2}\n"
                )
                f.write(f'echo "Title. {results[i][1]}"\n')
                f.write(
                    f"tput cup {separator_height + (rng_lst[2] + 2)} {choice_width + 2}\n"
                )
                f.write(f'echo "Comment. {results[i][2]}"\n')
                f.write(
                    f"tput cup {separator_height + (rng_lst[3] + 2)} {choice_width + 2}\n"
                )
                f.write("tput setaf 1\n")
                f.write(f'echo "Link. {results[i][3]}"\n')
                f.write("tput sgr0\n")
                f.write(
                    f"tput cup {separator_height + (rng_lst[4] + 2)} {choice_width + 2}\n"
                )
                f.write(f'echo "K1. {results[i][4]}"\n')
                f.write(
                    f"tput cup {separator_height + (rng_lst[5] + 2)} {choice_width + 2}\n"
                )
                f.write(f'echo "K2. {results[i][5]}"\n')
                f.write(
                    f"tput cup {separator_height + (rng_lst[6] + 2)} {choice_width + 2}\n"
                )
                f.write(f'echo "K3. {results[i][6]}"\n')
                f.write(
                    f"tput cup {separator_height + (rng_lst[7] + 2)} {choice_width + 2}\n"
                )
                f.write(f'echo "Time. {results[i][7]}"\n\n\n')
            else:
                # 'upper' represents the last height number used. So we know that we have to
                # use heights 'higher' than that value.
                upper = rng_lst[-1]
                init_rng = range(upper + 2, (upper + 2 + len(results[i])))
                rng_lst = [i for i in init_rng]
                f.write('echo " "\n')
                f.write(
                    f"tput cup {separator_height + rng_lst[0] + 2} {choice_width + 2}\n"
                )
                f.write(f"echo 'ID. {results[i][0]}'\n")
                pp(f"{results[i][0]}")
                f.write(
                    f"tput cup {separator_height + rng_lst[1] + 2} {choice_width + 2}\n"
                )
                f.write(f'echo "Title. {results[i][1]}"\n')
                f.write(
                    f"tput cup {separator_height + rng_lst[2] + 2} {choice_width + 2}\n"
                )
                f.write(f'echo "Comment. {results[i][2]}"\n')
                f.write(
                    f"tput cup {separator_height + rng_lst[3] + 2} {choice_width + 2}\n"
                )
                f.write("tput setaf 1\n")
                f.write(f'echo "Link. {results[i][3]}"\n')
                f.write("tput sgr0\n")
                f.write(
                    f"tput cup {separator_height + rng_lst[4] + 2} {choice_width + 2}\n"
                )
                f.write(f'echo "K1. {results[i][4]}"\n')
                f.write(
                    f"tput cup {separator_height + rng_lst[5] + 2} {choice_width + 2}\n"
                )
                f.write(f'echo "K2. {results[i][5]}"\n')
                f.write(
                    f"tput cup {separator_height + rng_lst[6] + 2} {choice_width + 2}\n"
                )
                f.write(f'echo "K3. {results[i][6]}"\n')
                f.write(
                    f"tput cup {separator_height + rng_lst[7] + 2} {choice_width + 2}\n"
                )
                f.write(f'echo "Time. {results[i][7]}"\n\n\n')

        f.write("echo ' '\n")
        f.write(f"tput cup {space_under_separator + len(results) + 2} {choice_width}\n")
        # Without it the page would close immediately. I still have to understand this better.
        f.write("read -p 'Enter any key to quit: ' choice\n")
        f.write('echo "${choice}" > ')
        f.write("collection_choice.txt\n\n")
        f.write("clear\n")
        f.write("tput sgr0\n")
        f.write("tput rc")

    subprocess.run("sudo chmod +x see.bash", cwd=os.getcwd(), shell=True)
    subprocess.run("./see.bash", cwd=os.getcwd(), shell=True)


# @snoop
def call_see():
    """
    Calls the previous functions.
    Called by 'main.py'
    """

    see_db_call()
    see_output_page()
