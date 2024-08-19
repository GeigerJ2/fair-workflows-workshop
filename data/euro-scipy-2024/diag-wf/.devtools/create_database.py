import sqlite3
import numpy as np
import io
import os


def adapt_array(arr):
    """
    http://stackoverflow.com/a/31312102/190597 (SoulNibbler)
    """
    out = io.BytesIO()
    np.save(out, arr)
    out.seek(0)
    return sqlite3.Binary(out.read())

def convert_array(arr_text):
    out = io.BytesIO(arr_text)
    out.seek(0)
    return np.load(out)

def create_sqlite_database(database_filename: str):
    """ create a database connection to an SQLite database """
    sqlite3.register_adapter(np.ndarray, lambda x: x.tobytes())
    sqlite3.register_converter("NP_NDARRAY", np.frombuffer)
    with sqlite3.connect(database_filename, detect_types=sqlite3.PARSE_DECLTYPES) as conn:


        cur = conn.cursor()
        cur.execute("""CREATE TABLE matrices (
                                            pk INTEGER NOT NULL PRIMARY KEY,
                                            arr NP_NDARRAY,
                                            arr_rows INTEGER, 
                                            arr_cols INTEGER)""")

        rng = np.random.default_rng(seed=0)
        for pk in range(50):
            rows = 11 + rng.integers(-10, 10)
            mat = rng.random((rows, rows))

            cur.execute("INSERT INTO matrices (pk, arr, arr_rows, arr_cols) VALUES (?, ?, ?, ?)",
                        (pk, mat, mat.shape[0], mat.shape[1]))



if __name__ == '__main__':
    create_sqlite_database("matrices.db")
