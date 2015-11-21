import psycopg2
import contextlib


def connect():
    """Connect to the PostgreSQL database.  Returns a
    database connection."""
    db = psycopg2.connect("dbname=catalog user=postgres password=postgres host=localhost")
    return db

@contextlib.contextmanager
def get_cursor():
    """
    Helper function for using cursors.  Helps to avoid a lot of connect,
    execute, commit code
    """
    conn = connect()
    cur = conn.cursor()
    try:
        yield cur
    except:
        raise
    else:
        conn.commit()
    finally:
        cur.close()
        conn.close()