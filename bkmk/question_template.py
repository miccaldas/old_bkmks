"""
Template for all windows who have
just one question in them and don't
need frther handling.
It's called by 'notes.py', 'search.py'
"""
import os
import pickle
import subprocess
import sys
from configs.config import tput_config
import snoop
from snoop import pp


def type_watch(source, value):
    return "type({})".format(source), type(value)


snoop.install(out="snoop.log", overwrite=True, watch_extras=[type_watch])


# @snoop
def question_template(name, text):
    """
    Creates a bash file specific for creating one
    question pages.
    """
    cnf = tput_config()
    title_width = int(
        cnf["init_width"] + (len(cnf["separator"]) / 2) - (len(f"{text}") / 2)
    )

    with open(f"{name}.bash", "w") as f:
        f.write("#!/usr/bin/env bash\n\n")
        f.write("tput clear\n\n")
        f.write(f"tput cup {cnf['init_height']} {title_width}\n")
        f.write(f"tput setaf {cnf['title_color']}\n")
        f.write("tput bold\n")
        f.write(f'echo "{text}"\n')
        f.write("tput sgr0\n\n")
        f.write("")

        f.write(f"tput cup {cnf['separator_height']} {cnf['init_width']}\n")
        f.write(f"echo '{cnf['separator']}'\n")

        f.write(f"tput cup {cnf['separator_height'] + 4} {cnf['init_width']}\n")
        f.write("read -p '[»»] ' choice\n")
        # The next line doesn't have a line break at the end because it
        # and the line next to it are supposed to be just one line.
        # It was needed because the '{}' in the f-string and in the bash
        # variable definition, weren't getting along.
        f.write('echo "${choice}" > ')
        f.write(f"{name}_choice.txt\n\n")
        f.write("tput clear\n")
        f.write("tput sgr0\n")
        f.write("tput rc")

    subprocess.run(f"sudo chmod +x {name}.bash", cwd=os.getcwd(), shell=True)
    subprocess.run(f"./{name}.bash", cwd=os.getcwd(), shell=True)








