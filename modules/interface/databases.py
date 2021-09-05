from ..interface.configparser import TextDatabase

AuthDB = TextDatabase()
AuthDB.connect('./database/auth.db')