"""
Module that'll do some housekeeping on the bookmarks db.
"""
import snoop
from mysql.connector import Error, connect
from snoop import pp

# import os
# import subprocess
from thefuzz import fuzz, process


def type_watch(source, value):
    return "type({})".format(source), type(value)


snoop.install(watch_extras=[type_watch])


class Diagnostics:
    """
    Here we'll house methods that'll analyze keywords that are
    too similar, repeated content and empty lines.
    """

    def __init__(self):
        pass

    @snoop
    def kwd_lst(self):
        """
        Creates a set of keywords from bkmks, taken
        from k1, k2 and k3.
        """
        try:
            conn = connect(
                host="localhost", user="mic", password="xxxx", database="bkmks"
            )
            cur = conn.cursor()
            query = "SELECT k1 FROM bkmks UNION DISTINCT SELECT k2 FROM bkmks UNION DISTINCT SELECT k3 FROM bkmks"
            cur.execute(query)
            records = cur.fetchall()
            recs = [i for t in records for i in t]
            rec = [i.strip() for i in recs]
        except Error as e:
            print("Error while connecting to db ", e)
        finally:
            if conn:
                conn.close()

        self.records = [i for i in rec if len(i) >= 2]

    @snoop
    def kwd_similarity(self):
        """
        We analyze the keywords to find repeated values.
        I took the resulting list from the output because
        it took so long to run, and I don't want to run it
        again. I'll just clean the results in mycli.
        """
        val_lst = []
        for i in range(len(self.records)):
            vals = process.extract(self.records[i], self.records)
            values = [val for val in vals if val[1] >= 95 and val[1] <= 100]
            if len(values) > 1:
                val_lst.append(values)

        self.val_lst = [[('shortener', 100), ('url shortener', 95)], [('questionary', 100), ('questionnary', 96)], [('add-gitignore', 100), ('gitignore', 95)], [('visualizer', 100), ('visualize', 95)], [('scrape-search-engine', 100), ('scrape search engine', 100)], [('scrape-search-engine', 100), ('scrape search engine', 100)], [('url shortener', 100), ('shortener', 95)], [('questionnary', 100), ('questionary', 96)], [('cheat sheet', 100), ('cheatsheet', 95)], [('web framework', 100), ('framework', 95)], [('converters', 100), ('converter', 95), ('converter', 95)], [('framework', 100), ('web framework', 95)], [('cheatsheet', 100), ('cheat sheet', 95), ('cheatsheets', 95)], [('gitignore', 100), ('add-gitignore', 95)], [('characters', 100), ('character', 95)], [('converter', 100), ('converter', 100), ('converters', 95)], [('converter', 100), ('converter', 100), ('converters', 95)], [('colorscheme', 100), ('colorschemes', 96)], [('colorschemes', 100), ('colorscheme', 96)], [('visualize', 100), ('visualizer', 95)], [('cheatsheets', 100), ('cheatsheet', 95)], [('character', 100), ('characters', 95)]]


dgs = Diagnostics()
# dgs.kwd_lst()
# dgs.kwd_similarity()
