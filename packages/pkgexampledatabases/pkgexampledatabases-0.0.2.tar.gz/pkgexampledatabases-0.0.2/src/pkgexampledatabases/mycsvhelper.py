from pathlib import Path
import subprocess


class MyCSVHelper:
    def __init__(self):
        pass

    # Using sqlite3 .import is much faster than using python, or pandas to load data in to database.
    def bulk_load(self, csvfilepath, databasepath, tablename):
        # This assumes the csv file has headers, so using --skip 1 to skip headerline.
        result = subprocess.run(
            [
                "sqlite3",
                str(databasepath),
                "-cmd",
                ".mode csv",
                ".import --skip 1 "
                + str(csvfilepath).replace("\\", "\\\\")
                + f" {tablename}",
            ],
            capture_output=True,
        )
        # print(f"RESULT: {result}")
