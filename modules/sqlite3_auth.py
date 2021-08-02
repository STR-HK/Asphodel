from modules.mysqlite3 import cursor


def auth_init_database():
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS auth(token TEXT, forever TEXT, expire TEXT)"
    )


auth_init_database()


def auth_return_tuple_data(column):
    cursor.execute("SELECT {} FROM auth".format(column))
    return cursor.fetchall()


def auth_insert_value(token, forever=False, expire=None):
    cursor.execute(
        "INSERT INTO auth(token, forever, expire) VALUES (?,?,?)",
        (token, forever, expire),
    )


def auth_remove_row_by_token_name(tokenname):
    cursor.execute("DELETE FROM auth WHERE token={}".format(tokenname))


def auth_update_expire(expire, tokenname):
    cursor.execute("UPDATE auth SET expire = ? WHERE token = ?", (expire, tokenname))
