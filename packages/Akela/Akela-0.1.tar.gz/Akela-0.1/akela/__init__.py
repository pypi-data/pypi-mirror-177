__version__ = "0.1"

import requests, os.path, os, configparser, markdownify
from sys import argv


class Page:
    """ Class for embedding Akela """
    Encod = "default"
    pageheader = None
    head = {"User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}
    pagecode = None
    
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
        """ Generate a config for uzoenr. """
        if not os.path.exists(os.path.expanduser("~")+"/.akela/"):
            os.mkdir(os.path.expanduser("~")+"/.akela")
            with open(os.path.expanduser("~")+"/.akela/bm.ini", 'w'):
                pass
        if not os.path.exists(os.path.expanduser("~")+"/.akela/library"):
            os.mkdir(os.path.expanduser("~"+"/.akela/library"))
        self.setconf('Bookmark', 'warranty', 'about:warranty')
        self.setconf('Bookmark', 'copy', 'about:copyright')
    def getconf(self, group, key):
        """ Get a configuration value """
        cfg = configparser.ConfigParser()
        cfg.read(os.path.expanduser("~")+"/.akela/bm.ini")
        return cfg[group][key]
    def load(self, url):
        """ Load and parse the URL. Please use this function to load the web page. """
        enq = self.Encod
        if url == "about:rule":
            self.pagecode = """
«Человек есть мера всех вещей существующих, что они существуют, и несуществующих, что они не существуют»
(Протагор)
"""
            return
        urli = url
        if not url.startswith("http://") and not url.startswith("https://"):
            urli = "http://"+url
        page = requests.get(urli, headers=self.head)
        self.pageheader = page.headers
        if enq.lower() not in ['default', '']:
            page.encoding = enq
        page = page.text
        b = markdownify.markdownify(page, heading_style="ATX")
        self.pagecode = b
        
def start():
    try:
        url = argv[1]
        path = os.path.expanduser('~')+f'/.akela/library/{argv[2]}'
    except IndexError:
        print(f"Usage: {argv[0]} url name")
        print("url - адрес скачиваемой страницы")
        print("name - имя файла в каталоге ~/.akela/library/")
        return
    A = Page()
    A.setcfg()
    A.load(url)
    with open(path, 'w') as f:
        f.write(A.pagecode)

if __name__ == "__main__":
    start()
