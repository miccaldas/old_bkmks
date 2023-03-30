"""
Main module of bkmks.
We call all other modules
from here.
"""
import os
import subprocess
import sys

import snoop
from add import call_add
from clean import clean
from configs.config import tput_config
from delete import call_delete
from notes import call_notes
from search import call_search
from see import call_see
from snoop import pp
from update import call_update


def type_watch(source, value):
    return "type({})".format(source), type(value)


snoop.install(watch_extras=[type_watch])


# @snoop
def main_script():
    """
    Creates template for the main page.
    It's called by 'main'.
    """

    # This outputs the dimensions of current terminal.
    cnf = tput_config()
    title = "WHAT DO YOU WANT TO DO?"
    title_width = int(
        cnf["init_width"] + (len(cnf["separator"]) / 2) - (len(f"{title}") / 2)
    )
    add = "Add a bookmark."
    see = "See the bookmarks"
    search = "Search the bookmarks."
    update = "Update the bookmarks."
    delete = "Delete a bookmark."
    ex = "Exit."

    with open("main.bash", "w") as f:
        f.write("#!/usr/bin/env bash\n\n")
        f.write("tput clear\n\n")
        f.write(f"tput cup {cnf['init_height']} {title_width}\n")
        f.write(f"tput setaf {cnf['title_color']}\n")
        f.write("tput bold\n")
        f.write(f'echo "{title}"\n')
        f.write("tput sgr0\n\n")

        f.write(f"tput cup {cnf['separator_height']} {cnf['init_width']}\n")
        f.write(f"echo '{cnf['separator']}'\n")

        f.write(f"tput cup {cnf['separator_height'] + 4} {cnf['init_width']}\n")
        f.write(f'echo "1. {add}"\n')
        f.write(f"tput cup {cnf['separator_height'] + 6} {cnf['init_width']}\n")
        f.write(f'echo "2. {see}"\n')
        f.write(f"tput cup {cnf['separator_height'] + 8} {cnf['init_width']}\n")
        f.write(f'echo "3. {search}"\n')
        f.write(f"tput cup {cnf['separator_height'] + 10} {cnf['init_width']}\n")
        f.write(f'echo "4. {update}"\n')
        f.write(f"tput cup {cnf['separator_height'] + 12} {cnf['init_width']}\n")
        f.write(f'echo "5. {delete}"\n')
        f.write(f"tput cup {cnf['separator_height'] + 14} {cnf['init_width']}\n")
        f.write('echo "6. Clean Folder"\n')
        f.write(f"tput cup {cnf['separator_height'] + 16} {cnf['init_width']}\n")
        f.write('echo "7. Exit"\n')
        f.write(f"tput cup {cnf['separator_height'] + 18} {cnf['init_width']}\n")
        f.write("read -p 'Enter your choice: ' choice\n")
        f.write('echo "${choice}" > ')
        f.write("main_choice.txt\n\n")
        f.write("tput clear\n")
        f.write("tput sgr0\n")
        f.write("tput rc")

    subprocess.run("sudo chmod +x main.bash", cwd=os.getcwd(), shell=True)
    subprocess.run("./main.bash", cwd=os.getcwd(), shell=True)

    with open("main_choice.txt", "r") as f:
        dirty_mn = f.read()
        mn = dirty_mn.strip()

        return mn


# @snoop
def main():
    """
    We ask the user what he wants
    to do, and choose the right module to resolve it.
    We delete all transient files
    after running any function.
    """

    mn = main_script()

    if mn == "1":
        call_add()

    if mn == "2":
        call_see()

    if mn == "3":
        call_search()
        with open("search_results_choice.txt", "r") as f:
            dirty_results = f.read()
            results = dirty_results.strip()
            if results == "n":
                call_notes()
            else:
                pass

    if mn == "4":
        call_update()

    if mn == "5":
        call_delete()

    if mn == "6":
        clean()

    if mn == "7":
        sys.exit()

    clean()


if __name__ == "__main__":
    main()
