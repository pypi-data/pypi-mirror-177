import requests, os.path, os, configparser
from markdownify import markdownify
from akela.config import Config

class Akela:
    """ Class for embedding Akela """
    Encod = "default"
    pageheader = None
    head = {"User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}
    pagecode = None
    def setcfg(self):
        Config().setcfg()
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
        b = markdownify(page, heading_style="ATX")
        self.pagecode = b
