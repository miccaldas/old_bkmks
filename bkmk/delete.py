"""
All functions pertainig to the delete functionality.
"""
import snoop

from mysql.connector import Error, connect
from question_template import question_template
from snoop import pp


def type_watch(source, value):
    return "type({})".format(source), type(value)


snoop.install(out="snoop.log", overwrite=True, watch_extras=[type_watch])


# @snoop
def delete_db_call(answers):
    """
    Database call for deletion of a bookmark.
    Called by 'call_delete'
    """

    if "," in answers[0]:
        query = f"DELETE FROM bkmks WHERE id IN ({answers[0]})"
    if "," not in answers[0]:
        query = f"DELETE FROM bkmks WHERE id = '{answers[0]}'"
    if "-" in answers[0]:
        if " - " in answers[0]:
            answers = answers[0].replace(" ", "")
        split_lst = answers[0].split("-")
        query = f"DELETE FROM bkmks WHERE id BETWEEN {split_lst[0]} AND {split_lst[1]}"

    try:
        conn = connect(host="localhost", user="mic", password="xxxx", database="bkmks")
        cur = conn.cursor()
        query
        cur.execute(query)
        conn.commit()
        conn.close()
    except Error as e:
        err_msg = "Error while connecting to db", e
        print("Error while connecting to db", e)
        if err_msg:
            return query, err_msg

    return query


# @snoop
def call_delete():
    """
    Calls the database function.
    Called by 'main.py'
    """
    question_template("delete", "What is the id of the bookmark you want to delete?")
    with open("delete_choice.txt", "r") as f:
        dirty_delete = f.read()
        delete = dirty_delete.strip()
        answers = [delete]
    delete_db_call(answers)
