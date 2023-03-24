import configparser
import platform 

class ConfigReader():

    def __init__(self):
        self.config = configparser.ConfigParser()

        if platform.system() == 'Windows':
            self.config_path = "lfa_readouts_package\lfa_project\config.ini"
        else:
            self.config_path = "lfa_readouts_package/lfa_project/config.ini"
        self.config.read(self.config_path)

    def get_config_string(self, section, option):
        return self.config.get(section, option)

    def get_config_int(self, section, option):
        return self.config.getint(section, option)
    
    def get_config_boolean(self, section, option):
        return self.config.getboolean(section, option)

    def write_to_config(self, section, option, value):
        self.config.set(section, option, value)
        with open(self.config_path, 'w') as config_file:
            self.config.write(config_file)
