import sqlite3

class DBHandler:

    def dict_factory(cursor, row):
        fields = [column[0] for column in cursor.description]
        return {key: value for key, value in zip(fields, row)}
    
    CONNECTION = sqlite3.connect("db/db.sqlite", check_same_thread=False)
    CONNECTION.row_factory = dict_factory
    CURSOR = CONNECTION.cursor()


    @staticmethod
    def execute(command, *values):
        DBHandler.CURSOR.execute(command, tuple(values))
        DBHandler.CONNECTION.commit()

    @staticmethod
    def field(command, *values):
        DBHandler.CURSOR.execute(command, tuple(values))
        fetch =  DBHandler.CURSOR.fetchone()
        if fetch is not None:
            return fetch[0]
        return None

    @staticmethod
    def record(command, *values):
        DBHandler.CURSOR.execute(command, tuple(values))
        return DBHandler.CURSOR.fetchone()

    @staticmethod
    def records(command, *values):
        DBHandler.CURSOR.execute(command, tuple(values))
        return DBHandler.CURSOR.fetchall()

    @staticmethod
    def column(command, *values):
        DBHandler.CURSOR.execute(command, tuple(values))
        return [list(item.values())[0] for item in DBHandler.CURSOR.fetchall()]



