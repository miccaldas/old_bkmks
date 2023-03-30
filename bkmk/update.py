"""
All functions pertaining to the update functionality.
"""
import os
import subprocess
from configs.config import tput_config
import snoop
from mysql.connector import Error, connect
from snoop import pp


def type_watch(source, value):
    return "type({})".format(source), type(value)


snoop.install(out="snoop.log", overwrite=True, watch_extras=[type_watch])


# @snoop
def update_script():
    """
    Creates template for the update page.
    It's called by 'call_update'.
    """

    cnf = tput_config()
    updt_str = "What is your update you want to do?"
    col_str = "What is the column?"
    id_str = "What is the id?"
    title_str = "UPDATE"
    title_width = int(
        cnf["init_width"] + (len(cnf["separator"]) / 2) - (len(f"{title_str}") / 2)
    )


    with open("update.bash", "w") as f:
        f.write("#!/usr/bin/env bash\n\n")
        f.write("tput clear\n\n")
        f.write(f"tput cup {cnf['init_height']} {title_width}\n")
        f.write(f"tput setaf {cnf['title_color']}\n")
        f.write("tput bold\n")
        f.write('echo "UPDATE"\n')
        f.write("tput sgr0\n\n")
        f.write("")

        f.write(f"tput cup {cnf['separator_height']} {cnf['init_width']}\n")
        f.write(f"echo '{cnf['separator']}'\n")
        f.write(f"tput cup {cnf['separator_height'] + 2} {cnf['init_width']}\n")
        f.write(f"read -p '{id_str}: ' choice\n")
        f.write('echo "${choice}" > update_id_choice.txt\n')
        f.write(f"tput cup {cnf['separator_height'] + 4} {cnf['init_width']}\n")
        f.write(f'read -p "{col_str}: " choice\n')
        f.write('echo "${choice}" > update_col_choice.txt\n')
        f.write(f"tput cup {cnf['separator_height'] + 6} {cnf['init_width']}\n")
        f.write(f'read -p "{updt_str}: " choice\n')
        f.write('echo "${choice}" > update_updt_choice.txt\n')
        f.write("tput clear\n")
        f.write("tput sgr0\n")
        f.write("tput rc")

    subprocess.run("sudo chmod +x update.bash", cwd=os.getcwd(), shell=True)
    subprocess.run("./update.bash", cwd=os.getcwd(), shell=True)


# @snoop
def update_db_call():
    """
    Calls the database to make an update.
    Uses information created by 'update_script'.
    Called by 'call_update'.
    """

    with open("update_id_choice.txt", "r") as f:
        dirty_id = f.read()
        str_id = dirty_id.strip()
        ids = int(str_id)
    with open("update_col_choice.txt", "r") as f:
        dirty_column = f.read()
        column = dirty_column.strip()
    with open("update_updt_choice.txt", "r") as f:
        dirty_update = f.read()
        update = dirty_update.strip()

    try:
        conn = connect(host="localhost", user="mic", password="xxxx", database="bkmks")
        cur = conn.cursor()
        query = f"UPDATE bkmks SET {column} = '{update}' WHERE id = {ids}"
        cur.execute(query)
        conn.commit()
    except Error as e:
        err_msg = "Error while connecting to db", e
        print("Error while connecting to db", e)
        if err_msg:
            return query, err_msg
    finally:
        if conn:
            conn.close()

    return query


# @snoop
def call_update():
    """
    Calls the other functions in the module.
    It's called by 'main.py'
    """
    update_script()
    update_db_call()
