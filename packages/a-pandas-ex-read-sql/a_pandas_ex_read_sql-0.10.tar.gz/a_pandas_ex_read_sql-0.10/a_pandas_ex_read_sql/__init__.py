import sqlite3
import pandas as pd


def read_sqlite(path: str) -> dict:
    try:
        with sqlite3.connect(path) as sqlconn:
            tables = tuple(
                pd.read_sql_query(
                    "SELECT name FROM sqlite_master WHERE type='table';", sqlconn
                )["name"]
            )
            sqlconv = {
                t: pd.read_sql_query(f"SELECT * from {t}", sqlconn) for t in tables
            }
        return sqlconv
    except Exception as fe:
        print(fe)
        print(
            "Error! You might need to update the sqlite3.dll file!\nGo to: https://www.sqlite.org/download.html ,\ndownload the dll and put it in the DLLs folder of your env!"
        )


def pd_add_read_sql_file():
    pd.Q_read_sql = read_sqlite


# $ pip install a-pandas-ex-read-sql
# from a_pandas_ex_read_sql import pd_add_read_sql_file
# pd_add_read_sql_file()
# import pandas as pd
# dict_with_dfs = pd.Q_read_sql(r"F:\msgstorexxxxxxxxxxxxxxxxx.db")
