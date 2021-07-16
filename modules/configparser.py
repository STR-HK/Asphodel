import sqlite3

connect = sqlite3.connect("tasks.db")
cursor = connect.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS
                    taskmgr(path TEXT, creationtime_t TEXT, creationtime TEXT,
                    name TEXT, size TEXT, bytesize TEXT, length TEXT, lengthIso TEXT,
                    type TEXT, resolution TEXT, tags TEXT, extension TEXT, children TEXT)
                """.replace('\n','').replace('\t',''))

cursor.execute('SELECT name FROM taskmgr')
print(cursor.fetchall())

def insert_value(path=None, creationtime_t=None, creationtime=None, name=None, size=None, bytesize=None, length=None, lengthIso=None, type_=None, resolution=None, tags=None, extension=None, children=None):
    cursor.execute('INSERT INTO taskmgr(path, creationtime_t, creationtime, name, size, bytesize, length, lengthIso, type, resolution, tags, extension, children) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)', (path, str(creationtime_t), creationtime, name, size, str(bytesize), length, lengthIso, str(type_), str(resolution), str(tags), extension, str(children)))
    connect.commit()
