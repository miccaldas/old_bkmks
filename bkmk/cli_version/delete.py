"""
Command line version of the delete function bookmarks.
Called by 'bkdlt' command.
The reason for the line breaks in the function docstring
is due to the fact that Click rearranges you text when
putting i in the 'help' option. This helps.
"""
import click
import snoop

from mysql.connector import Error, connect
from snoop import pp


def type_watch(source, value):
    return "type({})".format(source), type(value)


snoop.install(watch_extras=[type_watch])


@click.command()
@click.option("--dlt")
#@snoop
def delete(dlt):
    """
    Function that deletes one, several or
    range of entries in the 'bkmks' database.\n
    You can use its sole option, '--dlt' in the following form:\n
    1. Delete non sequential entries. Surround the ids with quotation
       marks and separate them with a comma:\n
       "dlt '435, 436'", for example.
    \n
    2. Delete sequential entries. Envelop first and last ids with quotation
       marks and separate them with a dash:\n
       "dlt '437'-'439'".\n
       You may include spaces, but they'll be deleted by the application.\n
    3. Delete single entry. Write the id surrounded by quotation marks:\n
       "dlt '66'"
    """

    split_lst = []
    if "," in dlt:
        # When inputing id strings to delete as a sole string, as it is convenient, MySQL
        # creates an error, since it expects a tuple of strings in the query. First we have
        # to split the id's at the comma. Splitting with space or space + comma doesn't work.
        lst = dlt.split(",")
        # Splitting creates empty spaces inside the strings. This eliminates them.
        nlst = [i.strip() for i in lst]
        # Finally we turn the list to tuple, the desired format by MySQL.
        nt = tuple(nlst)
        query = f"DELETE FROM bkmks WHERE id IN {nt}"
    if "-" in dlt:
        if " - " in dlt:
            answers = dlt.replace(" ", "")
            split_lst = answers.split("-")
        else:
            split_lst = dlt.split("-")
        query = f"DELETE FROM bkmks WHERE id BETWEEN {split_lst[0]} AND {split_lst[1]}"
    if "," not in dlt and "-" not in dlt:
        query = f"DELETE FROM bkmks WHERE id = {dlt}"

    try:
        conn = connect(host="localhost", user="mic", password="xxxx", database="bkmks")
        cur = conn.cursor()
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


if __name__ == "__main__":
    delete()
