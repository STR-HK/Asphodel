import ast

from .database import configCursor


def taskmgr_init_database():
    configCursor.execute(
        """CREATE TABLE IF NOT EXISTS
                        taskmgr(path TEXT, creationtime_t TEXT, creationtime TEXT,
                        name TEXT, size TEXT, bytesize TEXT, length TEXT, lengthIso TEXT,
                        type TEXT, resolution TEXT, tags TEXT, extension TEXT, children TEXT)
                    """.replace(
            "\n", ""
        ).replace(
            "\t", ""
        )
    )


taskmgr_init_database()


def taskmgr_return_tuple_data(column):
    configCursor.execute("SELECT {} FROM taskmgr".format(column))
    return configCursor.fetchall()


def taskmgr_return_json_data(column):
    configCursor.execute("SELECT {} FROM taskmgr".format(column))
    return_list = []
    for row in configCursor.fetchall():
        solved = {
            "path": row[0],
            "creationtime_t": int(row[1]),
            "creationtime": row[2],
            "name": row[3],
            "size": row[4],
            "bytesize": int(row[5]),
            "length": row[6],
            "lengthIso": row[7],
            "type": ast.literal_eval(row[8]),
            "resolution": ast.literal_eval(row[9]),
            "tags": ast.literal_eval(row[10]),
            "extension": row[11],
            "children": ast.literal_eval(row[12]),
        }
        return_list.append(solved)
    return return_list


def taskmgr_insert_value(
    path=None,
    creationtime_t=None,
    creationtime=None,
    name=None,
    size=None,
    bytesize=None,
    length=None,
    lengthIso=None,
    type_=None,
    resolution=None,
    tags=None,
    extension=None,
    children=None,
):
    configCursor.execute(
        """INSERT INTO taskmgr(path, creationtime_t, creationtime, 
                        name, size, bytesize, length, lengthIso, 
                        type, resolution, tags, extension, children) 
                        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""".replace(
            "\n", ""
        ).replace(
            "\t", ""
        ),
        (
            path,
            str(creationtime_t),
            creationtime,
            name,
            size,
            str(bytesize),
            length,
            lengthIso,
            str(type_),
            str(resolution),
            str(tags),
            extension,
            str(children),
        ),
    )
