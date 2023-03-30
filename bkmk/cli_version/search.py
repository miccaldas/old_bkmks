"""
Command line implementation of the 'search' function in 'bkmks'.
"""
import datetime
import os
import pickle
import subprocess

import click
import snoop
from mysql.connector import Error, connect
from snoop import pp

from bkmk.configs.config import tput_config


def type_watch(source, value):
    return "type({})".format(source), type(value)


snoop.install(watch_extras=[type_watch])


# @snoop
def show_results():
    """
    Outputs the search query results as ascii tables.
    """
    cnf = tput_config()

    entries = []
    with open("srch.bin", "rb") as f:
        while True:
            try:
                entries.append(pickle.load(f))
            except EOFError:
                break
    results = [i for sublst in entries for i in sublst]

    title_str = "SEARCH RESULTS"
    title_width = int(
        cnf["init_width"] + (len(cnf["separator"]) / 2) - (len(f"{title_str}") / 2)
    )
    # Here we needed to do three things; one, set id value to string as we'll its len()
    # value and ints don't have length; delete quotation marks from comments and title,
    # as bash is finicky displaying it, and three, turn the datetime value to a string,
    # so we can access its len() value.
    vals = [
        (
            str(a),
            b.replace("'", ""),
            c.replace("'", ""),
            d,
            e,
            f,
            g,
            h.strftime("%d-%m-%Y_%H:%M"),
        )
        for a, b, c, d, e, f, g, h in results
    ]
    lns_val = [
        (len(a), len(b), len(c), len(d), len(e), len(f), len(g), len(h))
        for a, b, c, d, e, f, g, h in vals
    ]
    lens_val = [item for t in lns_val for item in t]

    names = ["id", "title", "comment", "link", "k1", "k2", "k3", "tempo"]
    lens_nms = [len(nm) for nm in names]

    values = []
    for v in vals:
        values.append(
            [
                ("id", v[0]),
                ("title", v[1]),
                ("comment", v[2]),
                ("link", v[3]),
                ("k1", v[4]),
                ("k2", v[5]),
                ("k3", v[6]),
                ("tempo", v[7]),
            ]
        )

    hi_ln_val = max(lens_val)
    hi_ln_nms = max(lens_nms)
    vh = int(hi_ln_val + hi_ln_nms + 3)
    sep = "-"
    traces = "".join(sep * vh)
    ntraces = f"+-{traces}-+"
    ud_len = len(ntraces)

    with open("see_results.bash", "w") as f:
        f.write("#!/usr/bin/env bash\n\n")
        f.write("tput clear\n\n")
        f.write(f"tput cup {cnf['init_height']} ")
        f.write(f"{title_width}\n")
        f.write(f"tput setaf {cnf['title_color']}\n")
        f.write("tput bold\n")
        f.write(f'echo "{title_str}"\n')
        f.write("tput sgr0\n\n")
        f.write(f"tput cup {cnf['separator_height']} {cnf['init_width']}\n")
        f.write(f"echo '{cnf['separator']}'\n")
        table_width = int(
            (len(f"{ntraces}") / 2) - cnf["init_width"] + (len(cnf["separator"]) / 2)
        )
        first_item_height = int(cnf["separator_height"] + 4)
        rng_values_lst = range(len(values))
        rng_lst = [int(r) for r in rng_values_lst]

        for r in rng_lst:
            n_id_len0 = int(hi_ln_nms - len(values[r][0][0]))
            v_id_len0 = int(hi_ln_val - len(values[r][0][1]))
            space_id_n0 = "".join(" " * n_id_len0)
            space_id_v0 = "".join(" " * v_id_len0)
            n_title_len0 = int(hi_ln_nms - len(values[r][1][0]))
            v_title_len0 = int(hi_ln_val - len(values[r][1][1]))
            space_title_n0 = "".join(" " * n_title_len0)
            space_title_v0 = "".join(" " * v_title_len0)
            n_comment_len0 = int(hi_ln_nms - len(values[r][2][0]))
            v_comment_len0 = int(hi_ln_val - len(values[r][2][1]))
            space_comment_n0 = "".join(" " * n_comment_len0)
            space_comment_v0 = "".join(" " * v_comment_len0)
            n_link_len0 = int(hi_ln_nms - len(values[r][3][0]))
            v_link_len0 = int(hi_ln_val - len(values[r][3][1]))
            space_link_n0 = "".join(" " * n_link_len0)
            space_link_v0 = "".join(" " * v_link_len0)
            n_k1_len0 = int(hi_ln_nms - len(values[r][4][0]))
            v_k1_len0 = int(hi_ln_val - len(values[r][4][1]))
            space_k1_n0 = "".join(" " * n_k1_len0)
            space_k1_v0 = "".join(" " * v_k1_len0)
            n_k2_len0 = int(hi_ln_nms - len(values[r][5][0]))
            v_k2_len0 = int(hi_ln_val - len(values[r][5][1]))
            space_k2_n0 = "".join(" " * n_k2_len0)
            space_k2_v0 = "".join(" " * v_k2_len0)
            n_k3_len0 = int(hi_ln_nms - len(values[r][6][0]))
            v_k3_len0 = int(hi_ln_val - len(values[r][6][1]))
            space_k3_n0 = "".join(" " * n_k3_len0)
            space_k3_v0 = "".join(" " * v_k3_len0)
            n_tempo_len0 = int(hi_ln_nms - len(values[r][7][0]))
            v_tempo_len0 = int(hi_ln_val - len(values[r][7][1]))
            space_tempo_n0 = "".join(" " * n_tempo_len0)
            space_tempo_v0 = "".join(" " * v_tempo_len0)

            if r == 0:
                f.write(f"tput cup {cnf['separator_height'] + 3} {table_width}\n")
                f.write(f"echo '{ntraces}'\n")
                f.write(f"tput cup {first_item_height} {table_width}\n")
                f.write(
                    f"echo '| {values[r][0][0]}{space_id_n0} | {values[r][0][1]}{space_id_v0} |'\n"
                )
                f.write(f"tput cup {first_item_height + 1} {table_width}\n")
                f.write(
                    f"echo '| {values[r][1][0]}{space_title_n0} | {values[r][1][1]}{space_title_v0} |'\n"
                )
                f.write(f"tput cup {first_item_height + 2} {table_width}\n")
                f.write(
                    f"echo '| {values[r][2][0]}{space_comment_n0} | {values[r][2][1]}{space_comment_v0} |'\n"
                )
                f.write(f"tput cup {first_item_height + 3} {table_width}\n")
                f.write(
                    f"echo '| {values[r][3][0]}{space_link_n0} | {values[r][3][1]}{space_link_v0} |'\n"
                )
                f.write(f"tput cup {first_item_height + 4} {table_width}\n")
                f.write(
                    f"echo '| {values[r][4][0]}{space_k1_n0} | {values[r][4][1]}{space_k1_v0} |'\n"
                )
                f.write(f"tput cup {first_item_height + 5} {table_width}\n")
                f.write(
                    f"echo '| {values[r][5][0]}{space_k2_n0} | {values[r][5][1]}{space_k2_v0} |'\n"
                )
                f.write(f"tput cup {first_item_height + 6} {table_width}\n")
                f.write(
                    f"echo '| {values[r][6][0]}{space_k3_n0} | {values[r][6][1]}{space_k3_v0} |'\n"
                )
                f.write(f"tput cup {first_item_height + 7} {table_width}\n")
                f.write(
                    f"echo '| {values[r][7][0]}{space_tempo_n0} | {values[r][7][1]}{space_tempo_v0} |'\n"
                )
                f.write(f"tput cup {first_item_height + 8} {table_width}\n")
                f.write(f"echo '{ntraces}'\n")
                f.write(f"tput cup {first_item_height + 9} {table_width}\n")
                f.write("echo ' '\n")
            else:
                f.write(
                    pp(f"tput cup {first_item_height + 11 * r + 1} {table_width}\n")
                )
                f.write(f"echo '{ntraces}'\n")
                f.write(f"tput cup {first_item_height + 11 * r + 2} {table_width}\n")
                f.write(
                    f"echo '| {values[r][0][0]}{space_id_n0} | {values[r][0][1]}{space_id_v0} |'\n"
                )
                f.write(f"tput cup {first_item_height + 11 * r + 3} {table_width}\n")
                f.write(
                    f"echo '| {values[r][1][0]}{space_title_n0} | {values[r][1][1]}{space_title_v0} |'\n"
                )
                f.write(f"tput cup {first_item_height + 11 * r + 4} {table_width}\n")
                f.write(
                    f"echo '| {values[r][2][0]}{space_comment_n0} | {values[r][2][1]}{space_comment_v0} |'\n"
                )
                f.write(f"tput cup {first_item_height + 11 * r + 5} {table_width}\n")
                f.write(
                    f"echo '| {values[r][3][0]}{space_link_n0} | {values[r][3][1]}{space_link_v0} |'\n"
                )
                f.write(f"tput cup {first_item_height + 11 * r + 6} {table_width}\n")
                f.write(
                    f"echo '| {values[r][4][0]}{space_k1_n0} | {values[r][4][1]}{space_k1_v0} |'\n"
                )
                f.write(f"tput cup {first_item_height + 11 * r + 7} {table_width}\n")
                f.write(
                    f"echo '| {values[r][5][0]}{space_k2_n0} | {values[r][5][1]}{space_k2_v0} |'\n"
                )
                f.write(f"tput cup {first_item_height + 11 * r + 8} {table_width}\n")
                f.write(
                    f"echo '| {values[r][6][0]}{space_k3_n0} | {values[r][6][1]}{space_k3_v0} |'\n"
                )
                f.write(f"tput cup {first_item_height + 11 * r + 9} {table_width}\n")
                f.write(
                    f"echo '| {values[r][7][0]}{space_tempo_n0} | {values[r][7][1]}{space_tempo_v0} |'\n"
                )
                f.write(f"tput cup {first_item_height + 11 * r + 10} {table_width}\n")
                f.write(f"echo '{ntraces}'\n")
                f.write(f"tput cup {first_item_height + 11 * r + 11} {table_width}\n")
                f.write("echo ' '\n")

        f.write(f"tput cup {11 * len(rng_lst) + 13} {table_width}\n")
        f.write("read -p 'Press any key to exit. ' choice\n")
        f.write('echo "${choice}" > /dev/null\n')
        f.write("tput clear\n")
        f.write("tput sgr0\n")
        f.write("tput rc")

    subprocess.run("sudo chmod +x see_results.bash", cwd=os.getcwd(), shell=True)
    subprocess.run("./see_results.bash", cwd=os.getcwd(), shell=True)


@click.command()
@click.argument("srch")
# @snoop
def db_call(srch):
    """
    Accepts only one string which is the search query.\n
    Doesn't have options so use only the 'bksrch' command
    followed by the string query.\n
    Outputs a pickle file, 'srch.bin' and calls the 'show_results'
    function.
    """

    q1 = "SELECT id, title, comment, link, k1, k2, k3, tempo "
    q2 = "FROM bkmks WHERE MATCH(title, comment, k1, k2, k3) "
    q3 = f"AGAINST('{srch}')"

    try:
        conn = connect(host="localhost", user="mic", password="xxxx", database="bkmks")
        cur = conn.cursor()
        query = f"{q1}{q2}{q3}"
        cur.execute(query)
        records = cur.fetchall()
    except Error as e:
        err_msg = "Error while connecting to db", e
        print("Error while connecting to db", e)
        if err_msg:
            return query, err_msg
    finally:
        if conn:
            conn.close()

    with open("srch.bin", "wb") as f:
        pickle.dump(records, f)

    show_results()

    os.remove("srch.bin")
    os.remove("see_results.bash")


if __name__ == "__main__":
    db_call()
