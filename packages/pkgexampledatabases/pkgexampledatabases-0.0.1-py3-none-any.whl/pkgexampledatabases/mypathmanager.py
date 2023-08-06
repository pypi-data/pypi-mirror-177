import importlib.resources
import os

# A class to help you find full system paths inside your package,
# and other paths you might with to construct.

# More info on importlib.resources
# https://docs.python.org/3/library/importlib.resources.html

# To access files in your python package when it's build and
# installed, you must make entries in your setup.py, or your
# pyproject.toml

# The following setuptools guide has instructions for which
# ever you prefer.

# https://setuptools.pypa.io/en/latest/userguide/datafiles.html


class MyPathManager:
    def __init__(self):
        self.userdir = "/.rexdbp/"
        pass

    def get_package_datadir(self):
        # Reusing our namespace knowledge, we reference our package data dir.
        my_traversable_resource_container = importlib.resources.files(
            "pkgexampledatabases.data"
        )
        dirpath = str(my_traversable_resource_container.__dict__["_paths"][0]) + "/"
        return dirpath

    def get_user_datadir(self):
        # I've defined the user data dir to be a hidden directory in their home area.
        # You can do what you like.
        app_dir = os.path.expanduser("~") + self.userdir
        os.makedirs(app_dir, exist_ok=True)
        return f"{app_dir}"

    def get_config_filepath(self, configfilename):
        # Given a database config filename, this method will return a full system
        # filepath to the config directory in your package data file path.
        filepath = ""
        my_traversable_resource_container = importlib.resources.files(
            "pkgexampledatabases.data.config"
        ).joinpath(configfilename)
        my_pathlib_context_manager = importlib.resources.as_file(
            my_traversable_resource_container
        )
        with my_pathlib_context_manager as fullfilepath:
            filepath = str(fullfilepath)
        return filepath

    def get_sampledata_filepath(self, sampledatafilename):
        # Given a sampledata filename, this method will return a full system
        # filepath to the sampledata directory in your package data file path.
        filepath = ""
        my_traversable_resource_container = importlib.resources.files(
            "pkgexampledatabases.data.sampledata"
        ).joinpath(sampledatafilename)
        my_pathlib_context_manager = importlib.resources.as_file(
            my_traversable_resource_container
        )
        with my_pathlib_context_manager as fullfilepath:
            filepath = str(fullfilepath)
        return filepath

    def get_appconfig_filepath(self, configfilename):
        # Given a database config filename, this method will return a full system
        # filepath to the config directory in your package data file path.
        filepath = ""
        my_traversable_resource_container = importlib.resources.files(
            "pkgexampledatabases"
        ).joinpath(configfilename)
        my_pathlib_context_manager = importlib.resources.as_file(
            my_traversable_resource_container
        )
        with my_pathlib_context_manager as fullfilepath:
            filepath = str(fullfilepath)
        return filepath
