"""
Serves as a main module for all the operations regarding
adding a new bookmark to the database. The information
collected here will be presented to true main function.
"""
import os
import pickle
import subprocess

import snoop
from configs.config import tput_config
from mysql.connector import Error, connect
from snoop import pp


def type_watch(source, value):
    return "type({})".format(source), type(value)


snoop.install(out="snoop.log", overwrite=True, watch_extras=[type_watch])


# @snoop
def add_db_call(answers):
    """
    Sends all the data from the 'add' questions
    to the database. Called by 'call_add'
    """

    query = "INSERT INTO bkmks (title, comment, link, k1, k2, k3) VALUES (%s, %s, %s, %s, %s, %s)"

    answers = [answers[0], answers[1], answers[2], answers[3], answers[4], answers[5]]

    try:
        conn = connect(host="localhost", user="mic", password="xxxx", database="bkmks")
        cur = conn.cursor()
        cur.execute(query, answers)
        conn.commit()
        conn.close()
    except Error as e:
        err_msg = "Error while connecting to db", e
        print("Error while connecting to db", e)
        if err_msg:
            return query, err_msg

    return query


def call_script():
    """
    Page template for all 'add' question pages. Creates a
    bash file specific for creating the question page.
    It's called by 'call_script'.
    """
    cnf = tput_config()
    title_str = "ADD A BOOKMARK"
    title_width = int(
        cnf["init_width"] + (len(cnf["separator"]) / 2) - (len(f"{title_str}") / 2)
    )
    name = "addbkmk"
    tit_str = "What is the title of your bookmark?"
    comment_str = "What is the comment for your bookmark?"
    link_str = "What is the link of the bookmark?"
    k1_str = "Give a keyword for the bookmark."
    k2_str = "Give another keyword..."
    k3_str = "And another keyword ..."

    with open(f"{name}.bash", "w") as f:
        f.write("#!/usr/bin/env bash\n\n")
        f.write("tput clear\n\n")
        f.write(f"tput cup {cnf['init_height']} {title_width}\n")
        f.write(f"tput setaf {cnf['title_color']}\n")
        f.write("tput bold\n")
        f.write(f'echo "{title_str}"\n')
        f.write("tput sgr0\n\n")
        f.write("")

        f.write(f"tput cup {cnf['separator_height']} {cnf['init_width']}\n")
        f.write(f"echo '{cnf['separator']}'\n")

        f.write(f"tput cup {cnf['separator_height'] + 4} {cnf['init_width']}\n")
        f.write(f"read -p '{tit_str}: ' choice\n")
        f.write('echo "${choice}" > title_choice.txt\n')

        f.write(f"tput cup {cnf['separator_height'] + 6} {cnf['init_width']}\n")
        f.write(f"read -p '{comment_str}: ' choice\n")
        f.write('echo "${choice}" > comment_choice.txt\n')

        f.write(f"tput cup {cnf['separator_height'] + 8} {cnf['init_width']}\n")
        f.write(f"read -p '{link_str}: ' choice\n")
        f.write('echo "${choice}" > link_choice.txt\n')

        f.write(f"tput cup {cnf['separator_height'] + 10} {cnf['init_width']}\n")
        f.write(f"read -p '{k1_str}: ' choice\n")
        f.write('echo "${choice}" > k1_choice.txt\n')

        f.write(f"tput cup {cnf['separator_height'] + 12} {cnf['init_width']}\n")
        f.write(f"read -p '{k2_str}: ' choice\n")
        f.write('echo "${choice}" > k2_choice.txt\n')

        f.write(f"tput cup {cnf['separator_height'] + 14} {cnf['init_width']}\n")
        f.write(f"read -p '{k3_str}: ' choice\n")
        f.write('echo "${choice}" > k3_choice.txt\n')

        f.write("tput clear\n")
        f.write("tput sgr0\n")
        f.write("tput rc")

    subprocess.run(f"sudo chmod +x {name}.bash", cwd=os.getcwd(), shell=True)
    subprocess.run(f"./{name}.bash", cwd=os.getcwd(), shell=True)


# @snoop
def call_add():
    """
    We call all the question functions and
    collect the information files that they
    create. Finally call the db to upload
    the data.
    """

    # This runs all 'add' questions'.
    call_script()

    # Title definition.
    with open("title_choice.txt", "r") as f:
        title = f.read()

    # Comment definition.
    with open("comment_choice.txt", "r") as f:
        comment = f.read()

    # Link definition.
    with open("link_choice.txt", "r") as f:
        link = f.read()

    # K1 definition.
    with open("k1_choice.txt", "r") as f:
        k1 = f.read()

    # K2 definition.
    with open("k2_choice.txt", "r") as f:
        k2 = f.read()

    # K3 definition.
    with open("k3_choice.txt", "r") as f:
        k3 = f.read()

    dirty_answers = [title, comment, link, k1, k2, k3]
    answers = [i.strip() for i in dirty_answers]

    add_db_call(answers)
