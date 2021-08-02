import sqlite3

connect = sqlite3.connect("AsphodelData.db", check_same_thread=False)
cursor = connect.cursor()

def commit():
    connect.commit()