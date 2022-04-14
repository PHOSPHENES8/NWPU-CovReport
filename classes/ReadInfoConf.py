from configparser import RawConfigParser

class ReadInfoConf():

    def __init__(self, confpath = "infoconf/conf.ini") -> None:
        self.infoconf_file = confpath
        self.infoconf_file_ini = RawConfigParser()
        self.infoconf_file_ini.read(self.infoconf_file, encoding='utf-8')
    
    def get(self, section, name):
        # stu_number = infoconf_file_ini.get('driver', 'stu_number')
        # stu_passwd = infoconf_file_ini.get('driver', 'stu_passwd')
        # url = infoconf_file_ini.get('driver', 'url')
        return self.infoconf_file_ini.get(section, name)

