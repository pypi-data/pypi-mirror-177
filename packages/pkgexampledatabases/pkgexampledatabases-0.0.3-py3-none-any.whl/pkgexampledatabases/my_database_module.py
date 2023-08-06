import argparse
from .mypathmanager import MyPathManager
from .mydatabasemanager import ConfigToDatabase
from .myappconfigmanager import MyAppConfigManager
from .mycsvhelper import MyCSVHelper
from .mysqlitemanager import AppQuery
import os


def rexdbp():
    # A class that manages this applications config file
    # my_app_config_manager = MyAppConfigManager()
    # my_app_config = my_app_config_manager.get_appconfig()
    # A class based on our previous post to help you
    # find paths inside your package, and other paths.
    # my_path_manager = MyPathManager()
    # A class that takes a config file and creates a database.
    # config_to_database = ConfigToDatabase()

    # print(my_app_config)
    # Help input csv files.
    # my_csv_helper = MyCSVHelper()
    # read out data in sqlite database and tables
    # my_app_query = AppQuery()

    # Argument parsing starts here.
    main_group_parser = argparse.ArgumentParser(
        description="A package datafiles example"
    )
    main_group_parser.add_argument(
        "-p",
        "--createpdb",
        action="store_true",
        help="Create package db from config file.",
    )
    main_group_parser.add_argument(
        "-u",
        "--createudb",
        action="store_true",
        help="Create user db from config file.",
    )
    main_group_parser.add_argument(
        "-l",
        "--importlist",
        action="store_true",
        help="Import shopping data to user home dir database",
    )
    main_group_parser.add_argument(
        "-s",
        "--importstore",
        action="store_true",
        help="Import store data to package dir database",
    )
    main_group_parser.add_argument(
        "-f",
        "--files",
        action="store_true",
        help="Show the full filepaths of all our files",
    )
    main_group_parser.add_argument(
        "-L",
        "--outputlist",
        action="store_true",
        help="Output current data in users shopping list database",
    )
    main_group_parser.add_argument(
        "-S",
        "--outputstore",
        action="store_true",
        help="Output current data in package store database",
    )
    main_group_parser.add_argument(
        "-X",
        "--deletedbs",
        action="store_true",
        help="Delete package and user databases",
    )

    my_args = main_group_parser.parse_args()

    if my_args.createpdb:
        create_package_database()

    if my_args.createudb:
        create_user_database()

    if my_args.importlist:
        create_user_database()
        import_list()

    if my_args.importstore:
        create_package_database()
        import_store()

    if my_args.files:
        printfiles()

    if my_args.outputlist:
        outputlist()

    if my_args.outputstore:
        outputstore()

    if my_args.deletedbs:
        deletedbs()


def build_file_list():
    my_app_config_manager = MyAppConfigManager()
    my_app_config = my_app_config_manager.get_appconfig()
    my_path_manager = MyPathManager()
    files = {}
    # APPLICATION CONFIG
    files["app_config_path"] = my_app_config_manager.get_appconfig_path()
    # CONFIG FILES
    files["packagedb_configfilepath"] = my_path_manager.get_config_filepath(
        my_app_config["databaseconfig"]["packagedb"]
    )
    files["userdb_configfilepath"] = my_path_manager.get_config_filepath(
        my_app_config["databaseconfig"]["userdb"]
    )
    # SAMPLE DATA FILES
    files["shoppinglist_datafile"] = my_path_manager.get_sampledata_filepath(
        my_app_config["sampledata"]["shoppinglist"]
    )
    files["store_datafile"] = my_path_manager.get_sampledata_filepath(
        my_app_config["sampledata"]["store"]
    )
    # PACKAGE DATABASE
    packagedb_file_name = my_app_config["databases"]["packagedb"]
    files["package_databasepath"] = (
        my_path_manager.get_package_datadir() + packagedb_file_name
    )

    # USER DATABASE
    userdb_file_name = my_app_config["databases"]["userdb"]
    files["userdb_databasepath"] = my_path_manager.get_user_datadir() + userdb_file_name

    return files


def create_user_database():
    my_app_config_manager = MyAppConfigManager()
    my_app_config = my_app_config_manager.get_appconfig()
    my_path_manager = MyPathManager()
    config_to_database = ConfigToDatabase()
    # First we retrieve the full data directory path in our users home dir.
    userdb_databasedir = my_path_manager.get_user_datadir()
    # We then load the name of the user databaseconfig file.
    # This is stored in the generate application YAML config file.
    user_database_config_filename = my_app_config["databaseconfig"]["userdb"]
    # Then we retrieve the full path of the config file for the user database.
    userdb_configfilepath = my_path_manager.get_config_filepath(
        user_database_config_filename
    )
    # We then run the user db config file and output a db to the user data directory.
    databasepath = config_to_database.run_config(
        userdb_configfilepath, userdb_databasedir
    )
    print(f"CREATED: {databasepath}")


def create_package_database():
    my_app_config_manager = MyAppConfigManager()
    my_app_config = my_app_config_manager.get_appconfig()
    my_path_manager = MyPathManager()
    config_to_database = ConfigToDatabase()
    # First we retrieve the full data directory path of our package.
    packagedb_databasedir = my_path_manager.get_package_datadir()
    # We then load the name of the package databaseconfig file.
    # This is stored in the generate application YAML config file.
    package_database_config_filename = my_app_config["databaseconfig"]["packagedb"]
    # Then we append the full path of the config file for the package database.
    packagedb_configfilepath = my_path_manager.get_config_filepath(
        package_database_config_filename
    )
    # We then run that config and create an sqlite db in the package data dir.
    databasepath = config_to_database.run_config(
        packagedb_configfilepath, packagedb_databasedir
    )
    print(f"CREATED: {databasepath}")


def import_list():
    my_app_config_manager = MyAppConfigManager()
    my_app_config = my_app_config_manager.get_appconfig()
    my_path_manager = MyPathManager()
    my_csv_helper = MyCSVHelper()
    # We use bulk CSV imports by calling sqlite3 from the command line
    # inside my_csv_helper.

    # LETS GET THE CSV FILEPATH
    # First we get the name of the shopping list datasample file.
    shopping_list_csv = my_app_config["sampledata"]["shoppinglist"]
    # We then append the sampledata dir path to the filename we just retrieved.
    csvfilepath = my_path_manager.get_sampledata_filepath(shopping_list_csv)

    # LETS GET THE DATABASE FILEPATH
    # First we get the name of the user database from our app config file.
    userdb_file_name = my_app_config["databases"]["userdb"]
    # Then we append the datadir to that name to get the full path of the user database.
    databasepath = my_path_manager.get_user_datadir() + userdb_file_name

    # Now we builk load the data to the shopping list table.
    my_csv_helper.bulk_load(csvfilepath, databasepath, tablename="shoppinglist")


def import_store():
    my_app_config_manager = MyAppConfigManager()
    my_app_config = my_app_config_manager.get_appconfig()
    my_path_manager = MyPathManager()
    my_csv_helper = MyCSVHelper()
    # We use bulk CSV imports by calling sqlite3 from the command line
    # inside my_csv_helper.

    # LETS GET THE CSV FILEPATH
    # First we get the name of the shopping list datasample file.
    store_csv = my_app_config["sampledata"]["store"]
    # We then append the sampledata dir path to the filename we just retrieved.
    csvfilepath = my_path_manager.get_sampledata_filepath(store_csv)

    # LETS GET THE DATABASE FILEPATH
    # First we get the name of the user database from our app config file.
    packagedb_file_name = my_app_config["databases"]["packagedb"]
    # Then we append the datadir to that name to get the full path of the user database.
    databasepath = my_path_manager.get_package_datadir() + packagedb_file_name

    # Now we builk load the data to the shopping list table.
    my_csv_helper.bulk_load(csvfilepath, databasepath, tablename="productlist")


def deletedbs():
    files = build_file_list()
    userdatabase = files["userdb_databasepath"]
    packagedatabase = files["package_databasepath"]
    try:
        os.remove(userdatabase)
        os.remove(packagedatabase)
    except:
        pass


def outputstore():
    my_app_query = AppQuery()
    files = build_file_list()
    database = files["package_databasepath"]
    tablename = "productlist"

    my_app_query.output(database, tablename)


def outputlist():
    my_app_query = AppQuery()
    files = build_file_list()
    database = files["userdb_databasepath"]
    tablename = "shoppinglist"

    my_app_query.output(database, tablename)


def printfiles():
    files = build_file_list()
    for k in files:
        print(f"{k}: {files[k]}")
