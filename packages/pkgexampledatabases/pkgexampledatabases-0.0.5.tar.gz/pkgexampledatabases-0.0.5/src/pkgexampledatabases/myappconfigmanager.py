import yaml
from .mypathmanager import MyPathManager


class MyAppConfigManager:
    def __init__(self):
        self.my_path_manager = MyPathManager()
        pass

    def get_appconfig(self):
        # Hard coded location for this appconfig is in /pkgexample/appconfig.yaml
        # The following code finds the installed package location, and then reads
        # the yaml file returnting a python dict object.
        configpath = self.my_path_manager.get_appconfig_filepath("appconfig.yaml")
        with open(configpath, "r") as myyaml:
            content = yaml.safe_load(myyaml)
            return content

    def get_appconfig_path(self):
        configpath = self.my_path_manager.get_appconfig_filepath("appconfig.yaml")
        return configpath
