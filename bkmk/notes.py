"""
Gets results of the 'notes' db, to suplemment
the results of the 'bkmks' database.
"""

import os
import pickle
import subprocess

import snoop

from mysql.connector import Error, connect
from question_template import question_template
from snoop import pp


def type_watch(source, value):
    return "type({})".format(source), type(value)


snoop.install(out="snoop.log", overwrite=True, watch_extras=[type_watch])


@snoop
def notes_output_page():
    """
    Here we had to give up pn centering the content because,
    for tput, a multilined but one object, is something he
    can't fathom. On the other hand, it allows for a much
    simpler page construction. It is called by 'main.py'
    when the user says that he didn't found what he
    wanted, at the end of the bkmks search.
    Called by 'call_notes'.
    """

    # Document produced by 'notes_db_call'
    with open("/home/mic/python/bkmks_python/bkmks_python/notes.bin", "rb") as f:
        res = pickle.load(f)
    detuple = [i for t in res for i in t]
    # Notes come with an initial line break that destroys presentation in
    # 'bkmks'. This gets rid of the first ocurrence of '\n'.
    minusbreak = [entry[1:] for entry in detuple]
    # For convenience of handling, it's best to turn it to list again.
    relst = [minusbreak]
    # The shell gets very confusad with quotation marks and backticks.
    # Here we delete them.
    lst_quote_marks = [item for sublst in relst for item in sublst]
    lst_sans_apostrph = [obj.replace("'", "") for obj in lst_quote_marks]
    lst_sans_backticks = [tick.replace("`", "") for tick in lst_sans_apostrph]
    results = [c.replace('"', "") for c in lst_sans_backticks]

    terminal_size = os.get_terminal_size()
    height = terminal_size.lines
    width = terminal_size.columns
    # Couldn't get the text and separator in the same line.
    # They would start on the previous one and continue to
    # the next. Giving it some spaces inside their strings,
    # solved it.
    text = "  NOTES RESULTS"
    init_height = int(height / 3)
    init_width = 172
    # Notice there's no initial width value. That's because
    # anything I put in there would make worse the title and
    # separator problem. In desperation I deleted it, and it
    # helped. A little.
    init_pos = f"{init_height}"
    separator_height = int(init_height + 2)
    separator = "  --------- [»»] ---------"
    separator_width = init_width
    choice_width = init_width
    title_color = 2

    with open("test.bash", "w") as f:
        f.write("#!/usr/bin/env bash\n\n")
        f.write("tput clear\n\n")
        f.write(f"tput setaf {title_color}\n")
        f.write(f"tput cup {init_pos}\n")
        f.write("tput bold\n")
        f.write(f"echo '{text}'\n")
        f.write("tput sgr0\n")
        f.write(f"tput cup {separator_height} {init_width}\n")
        f.write(f"echo '{separator}'\n")
        for i in range(len(results)):
            f.write("tput bold\n")
            # To judge line height, we need to know what height was the anterior
            # line, and choose a value under it. The first entry in results
            # doesn't have anterior values. So it has to be treated differently.
            if i == 0:
                f.write(f"tput cup {separator_height + 4} {init_width}\n")
                f.write(f'echo "{results[i]}"\n')
                f.write("echo ' '\n")
                f.write('echo " "\n')
            else:
                # Notice that I didn't need to use Tput height-width values for these
                # strings. That's because they're multilined objects that will always
                # start on the leftmost width value, no matter what you do.
                f.write(f' echo "{results[i]}"\n')
                f.write("echo ' '\n")
                f.write('echo " "\n')
        f.write("read -p 'Press any key to exit: ' choice\n")
        f.write('echo "${choice}" > ')
        f.write("disregard_choice.txt\n\n")
        f.write("clear\n")
        f.write("tput sgr0\n")
        f.write("tput rc")

    subprocess.run("sudo chmod +x test.bash", cwd=os.getcwd(), shell=True)
    subprocess.run("./test.bash", cwd=os.getcwd(), shell=True)


@snoop
def notes_db_call(answers):
    """
    Searches the db for the query the user chose when
    searching in 'bkmks'.
    Called by 'call_notes'
    """

    # 'answers' is ona string list. Much easier working with just the string.
    answers_str = " ".join(answers)

    q1 = "SELECT note "
    q2 = "FROM notes WHERE MATCH(title, k1, k2, k3, note, url) "
    q3 = f"AGAINST('{answers_str}') ORDER BY TIME"

    try:
        conn = connect(host="localhost", user="mic", password="xxxx", database="notes")
        cur = conn.cursor()
        query = f"{q1}{q2}{q3}"
        cur.execute(query)
        records = cur.fetchall()
        with open("notes.bin", "wb") as f:
            pickle.dump(records, f)
        conn.close()
    except Error as e:
        err_msg = "Error while connecting to db", e
        print("Error while connecting to db", e)
        if err_msg:
            return query, err_msg

    return query


@snoop
def call_notes():
    """
    Calls the other functions in the module.
    Called by 'main.py'.
    """

    question_template("notes", "What is your query?")
    with open("notes_choice.txt", "r") as f:
        dirty_notes = f.read()
        notes = dirty_notes.strip()
        answers = [notes]
    notes_db_call(answers)
    notes_output_page()
