"""
Command line version for adding bookmarks to bkmks.
"""
import click
import snoop
from mysql.connector import Error, connect
from snoop import pp


def type_watch(source, value):
    return "type({})".format(source), type(value)


snoop.install(watch_extras=[type_watch])


@click.command()
@click.option("-t", "--title")
@click.option("-c", "--comment", prompt=True)
@click.option("-l", "--link")
@click.option("-k", "--keywords", nargs=3)
# @snoop
def add(title, comment, link, keywords):
    """
    All information is gathered through cli options.
    The command is 'bkadd' and it's universal.
    Options are:\n
    1. '-t/--title' Insert title of bookmark.\n
    2. '-c/--comment' Insert comment to bookmark. The
       program will automatically open a prompt for you
       to write. Just enter all other values, press Enter
       and the prompt will appear.\n
    3. '-l/--link' Insert URL of bookmark.\n
    4. '-k/--keywords' Insert up to three keywords.
    """

    query = "INSERT INTO bkmks (title, comment, link, k1, k2, k3) VALUES (%s, %s, %s, %s, %s, %s)"
    k1, k2, k3 = keywords
    answers = [title, comment, link, k1, k2, k3]
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


if __name__ == "__main__":
    add()
