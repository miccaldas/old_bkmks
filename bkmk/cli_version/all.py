"""
Shows all content on the bkmks database.
"""
import datetime
import os
import subprocess

import snoop
from blessed import Terminal
from mysql.connector import Error, connect
from snoop import pp

from bkmk.configs.config import tput_config


def type_watch(source, value):
    return "type({})".format(source), type(value)


snoop.install(watch_extras=[type_watch])


# @snoop
def all():
    """
    I'm trying again with the 'blessed' library, and I like the results.
    Using Tput for some time prepared me for this.
    """
    term = Terminal()
    query = "SELECT * FROM bkmks"
    try:
        conn = connect(host="localhost", user="mic", password="xxxx", database="bkmks")
        cur = conn.cursor()
        cur.execute(query)
        records = cur.fetchall()
    except Error as e:
        err_msg = "Error while connecting to the db", e
        print("Error while connecting to the db", e)
        if err_msg:
            return query, err_msg
    finally:
        if conn:
            conn.close()

    for record in records:
        record = (
            term.bold(str(record[0])),
            term.bold(record[1]),
            term.bold(record[2]),
            term.red_bold(record[3]),
            term.bold(record[4]),
            term.bold(record[5]),
            term.bold(record[6]),
            term.bold(record[7].strftime("%d-%m-%Y_%H:%M")),
            term.bold(
                "--------------------------------------------------------------------"
            ),
        )

        for line in record:
            print("\n".join(term.wrap(line, width=145, initial_indent=" " * 40)))


if __name__ == "__main__":
    all()
