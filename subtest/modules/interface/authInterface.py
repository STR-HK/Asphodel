from .database import authDB
from .database import authCursor

def auth_init_database():
    authCursor.execute(
        "CREATE TABLE IF NOT EXISTS auth(token TEXT, forever TEXT, expire TEXT, permission TEXT)"
    )


auth_init_database()


def auth_return_tuple_data(column):
    authCursor.execute("SELECT {} FROM auth".format(column))
    return authCursor.fetchall()


def auth_insert_value(token, forever=False, expire=None, permission=None):
    authCursor.execute(
        "INSERT INTO auth(token, forever, expire, permission) VALUES (?, ?, ?, ?)",
        (token, forever, expire),
    )

def auth_remove_row_by_token_name(tokenname):
    authCursor.execute("DELETE FROM auth WHERE token={}".format(tokenname))


def auth_update_expire(expire, tokenname):
    authCursor.execute("UPDATE auth SET expire = ? WHERE token = ?", (expire, tokenname))

# INSERT INTO auth(token, forever, expire) VALUES ('a', 0, '2021-10-23 02:43:02.119374')