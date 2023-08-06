"""Akela configuration file reading module

Class Config reads settings from ~/.akela/bm.ini and
creates ~/.akela/bm.ini file and ~/.akela/library
directory.

At the moment, it has only Zim section for keeping
a list of available ZIM files.

Use this syntax to describe them:

[Zim]
wikisource = /home/akela/.local/share/kiwix/wikisource_ru_all_maxi_2022-09.zim
wikipedia = /home/akela/.local/share/kiwix/wikipedia_ru_all_maxi_2022-11.zim

"""

import os.path, configparser

class Config:
    """Akela configuration file reading class"""
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
            with open(os.path.expanduser("~")+"/.akela/bm.ini", 'w') as f:
                cfg = configparser.ConfigParser()
                cfg['Zim'] = {'test':'test.zim'}
                cfg.write(f)
            # self.setconf('Zim', 'test', 'test.zim')
        if not os.path.exists(os.path.expanduser("~")+"/.akela/library"):
            os.mkdir(os.path.expanduser("~"+"/.akela/library"))
            
    def getconf(self, group, key):
        """ Get a configuration value """
        cfg = configparser.ConfigParser()
        cfg.read(os.path.expanduser("~")+"/.akela/bm.ini")
        return cfg[group][key]
    def getzimlocation(self, name):
        """Get location of given ZIM file alias 'name'"""
        return self.getconf("Zim", name)
