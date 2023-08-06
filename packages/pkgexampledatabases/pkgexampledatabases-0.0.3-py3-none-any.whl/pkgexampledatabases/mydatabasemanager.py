from .mypathmanager import MyPathManager
import json
from .mysqlitemanager import SqliteQuery

# A class to convert json descriptions of a database
# to a real database.
class ConfigToDatabase:
    def __init__(self):
        self.createdatabase = CreateDatabase()
        self.createtable = CreateTable()
        self.mypathmanager = MyPathManager()

    def run_config(self, configfilepath, databasedir):
        with open(configfilepath) as database_recipie:
            json_content = json.load(database_recipie)
            if "DataBases" not in json_content:
                print("Database descriptions not found...")
            else:
                databases = json_content["DataBases"]
                for database in databases:
                    databasename = database["DatabaseName"] + ".db"
                    databasepath = databasedir + databasename
                    self.createdatabase.create_database(databasepath)
                    if "Tables" in database:
                        tables = database["Tables"]
                        for table in tables:
                            if "TableName" in table:
                                tablename = table["TableName"]
                                if "Fields" in table:
                                    fields = table["Fields"]
                                    self.createtable.create_table(
                                        databasepath, tablename, fields
                                    )
                                    return databasepath


class CreateDatabase:
    def __init__(self):
        self.sqlitequery = SqliteQuery()

    def create_database(self, databasepath):
        self.sqlitequery.create_db_if_not_exists(databasepath)


class CreateTable:
    def __init__(self):
        self.sqlitequery = SqliteQuery()

    def create_table(self, databasepath, tablename, fields):
        query = self.make_table_query(tablename, fields)
        self.sqlitequery.writeonly_query(databasepath, query)

    def make_table_query(self, tablename: str, fields: list) -> str:
        query_top = f"CREATE TABLE IF NOT EXISTS {tablename} ("
        query_tail = " );"
        query_body = ""
        for field in fields:
            fieldname = field["FieldName"]
            fieldtype = field["FieldType"]
            if "Constraint" in field:
                fieldconstraint = " " + field["Constraint"]
            else:
                fieldconstraint = ""
            query_body = query_body + f"{fieldname} {fieldtype}{fieldconstraint},"
        make_table_query = query_top + query_body[:-1] + query_tail
        return make_table_query
