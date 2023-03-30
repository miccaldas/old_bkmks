"""
Command line version of the 'update' function for bkmks.
"""
import click
import snoop
from mysql.connector import Error, connect
from snoop import pp


def type_watch(source, value):
    return "type({})".format(source), type(value)


snoop.install(watch_extras=[type_watch])


@click.command()
@click.option("-i", "--ident", type=int)
@click.option("-c", "--column")
@click.option("-u", "--update", prompt=True)
# @snoop
def update(ident, column, update):
    """
    The function is called 'bkupdt' and has three options:\n
    1. 'ident'. Integer with the id value of the line we want
       to update.\n
    2. 'column'. String of the column's name we want to update.\n
    3. 'update'. Text that you want to change. This comes as a prompt,
       so just insert the other options and press Enter to access it.
    """

    try:
        conn = connect(host="localhost", user="mic", password="xxxx", database="bkmks")
        cur = conn.cursor()
        query = f"UPDATE bkmks SET {column} = '{update}' WHERE id = {ident}"
        cur.execute(query)
        conn.commit()
        conn.close()
    except Error as e:
        err_msg = "Error while connecting to db", e
        print("Error while connecting to db", e)
        if err_msg:
            return query, err_msg

    return query


if __name__ == "__main__":
    update()
