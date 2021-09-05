from . import configparser

def auth_init_database():
    """
    Create `auth` table if not exists
    """
    global authDB
    authDB = configparser.TextDatabase()

    authDB.connect('./database/auth.db')

    authDB.create_table_if_not_exists(table_name='auth', fields=['token', 'forever', 'expire', 'permission'])

auth_init_database()


def auth_select_column(column):
    """
    Return Entire column of `column` in `auth` table
    """

    authDB.select(table_name='auth', field_names= ''.format(column = column if isinstance(column, list) else [column]))

def auth_insert_value(token, forever=False, expire=None, permission=None):
    """
    Insert
    | `token` | `forever` | `expire` | `permisstion` | 
    to `auth`
    """

    authDB.insert(table_name='auth', values={'token':token, 'forever':forever, 'expire':expire, 'permission':permission})


def auth_remove_row_by_token_name(token):
    """
    Delete Where `token` is in `auth`
    """

    authDB.delete(table_name='auth', condition=f"token = '{token}'")


def auth_update_expire(expire, token):
    """
    Set `expire` Where `token` is in `auth`
    """

    authDB.update(table_name='auth', values={'expire':expire}, condition=f"token = '{token}'")


# INSERT INTO auth(token, forever, expire) VALUES ('a', 0, '2021-10-23 02:43:02.119374')
# auth_insert_value(token='alpha',forever=True)
# auth_insert_value(token='beta',forever=False, expire='2021-10-23 02:43:02.119374')
# auth_insert_value(token='gamma',forever=False)
# authDB.save()