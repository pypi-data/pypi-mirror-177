import sqlite3

# A class to help order your sqlite queries.


class SqliteQuery:
    def __init__(self):
        pass

    def writeonly_query(self, databasepath, query):
        # use this writeonly_query method, when
        # no results expected from query.
        # print(query)
        with sqlite3.connect(databasepath) as conn:
            cursor = conn.cursor()
            cursor.execute(query)

    def create_db_if_not_exists(self, databasepath):
        # Running the connect command is enough to do this.
        with sqlite3.connect(databasepath) as conn:
            cursor = conn.cursor()


class AppQuery:
    def __init__(self):
        pass

    def output(self, databasefile, tablename):
        # print(f"Database: {databasefile}, Table: {tablename}")
        try:
            with sqlite3.connect(databasefile) as conn:
                cursor = conn.cursor()
                cursor.execute(f"SELECT * FROM {tablename}")
                rows = cursor.fetchall()
                # print(f"TYPE:{type(rows)}")
                for row in rows:
                    print(row)
            pass
        except:
            print(f"{databasefile} does not exist. Please create it. Check --help")
