import configparser

class ConfigReader():

    def __init__(self):
        self.config = configparser.ConfigParser()

        self.config.read("lfa_project/config.ini")

    def getConfigString(self, section, option):
        return self.config.get(section, option)

    def getConfigInt(self, section, option):
        return self.config.getint(section, option)
    
    def getConfigBoolean(self, section, option):
        return self.config.getboolean(section, option)

