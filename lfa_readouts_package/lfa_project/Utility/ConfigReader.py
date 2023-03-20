import configparser
import platform 

class ConfigReader():

    def __init__(self):
        self.config = configparser.ConfigParser()

        if platform.system() == 'Windows':
            self.configPath = "lfa_readouts_package\lfa_project\config.ini"
        else:
            self.configPath = "lfa_readouts_package/lfa_project/config.ini"
        self.config.read(self.configPath)

    def getConfigString(self, section, option):
        return self.config.get(section, option)

    def getConfigInt(self, section, option):
        return self.config.getint(section, option)
    
    def getConfigBoolean(self, section, option):
        return self.config.getboolean(section, option)

    def writeToConfig(self, section, option, value):
        self.config.set(section, option, value)
        with open(self.configPath, 'w') as configfile:
            self.config.write(configfile)

