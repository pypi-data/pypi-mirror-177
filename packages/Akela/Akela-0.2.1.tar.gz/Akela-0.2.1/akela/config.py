import os.path, configparser

class Config:
    def setconf(self, group, key, val):
        """ Configure a value """
        cfg = configparser.ConfigParser()
        cfg.read(os.path.expanduser("~")+"/.akela/bm.ini")
        if group not in cfg:
            cfg[group] = {}
        cfg[group][key] = val
        with open(os.path.expanduser("~")+"/.akela/bm.ini", "w") as f:
            cfg.write(f)
    def setcfg(self):
        """ Generate a config for akela. """
        if not os.path.exists(os.path.expanduser("~")+"/.akela/"):
            os.mkdir(os.path.expanduser("~")+"/.akela")
            with open(os.path.expanduser("~")+"/.akela/bm.ini", 'w'):
                pass
        if not os.path.exists(os.path.expanduser("~")+"/.akela/library"):
            os.mkdir(os.path.expanduser("~"+"/.akela/library"))
        self.setconf('Zim', 'test', 'test.zim')
    def getconf(self, group, key):
        """ Get a configuration value """
        cfg = configparser.ConfigParser()
        cfg.read(os.path.expanduser("~")+"/.akela/bm.ini")
        return cfg[group][key]
    def getzimlocation(self, name):
        return self.getconf("Zim", name)
