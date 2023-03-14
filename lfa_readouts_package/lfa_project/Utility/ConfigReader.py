import configparser
import platform 

class ConfigReader():

    def __init__(self):
        self.config = configparser.ConfigParser()

        if platform.system() == 'Windows':
            configPath = "lfa_readouts_package\lfa_project\config.ini"
        else:
            configPath = "lfa_project/config.ini"
        self.config.read(configPath)

    def getConfigString(self, section, option):
        return self.config.get(section, option)

    def getConfigInt(self, section, option):
        return self.config.getint(section, option)
    
    def getConfigBoolean(self, section, option):
        return self.config.getboolean(section, option)

