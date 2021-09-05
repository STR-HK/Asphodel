from .database import authDB
from .database import authCursor

def auth_init_database():
    """
    Create `auth` table if not exists
    """
    authCursor.execute(
        "CREATE TABLE IF NOT EXISTS auth(token TEXT, forever TEXT, expire TEXT, permission TEXT)"
    )

auth_init_database()


def auth_return_tuple_data(column):
    """
    Return Entire column of `column` in `auth` table
    """
    authCursor.execute("SELECT {} FROM auth".format(column))
    return authCursor.fetchall()


def auth_insert_value(token, forever=False, expire=None, permission=None):
    """
    Insert
    
    | `token` | `forever` | `expire` | `permisstion` | 

    to `auth`
    """
    authCursor.execute(
        "INSERT INTO auth(token, forever, expire, permission) VALUES (?, ?, ?, ?)",
        (token, forever, expire, permission),
    )


def auth_remove_row_by_token_name(token):
    """
    Delete Where `token` is in `auth`
    """
    authCursor.execute("DELETE FROM auth WHERE token={}".format(token))


def auth_update_expire(expire, token):
    """
    Set `expire` Where `token` is in `auth`
    """
    authCursor.execute("UPDATE auth SET expire = ? WHERE token = ?", (expire, token))


# INSERT INTO auth(token, forever, expire) VALUES ('a', 0, '2021-10-23 02:43:02.119374')