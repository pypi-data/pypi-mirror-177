"""URI Parser module.

Class URI can parse protocols http, https and 
akela-zim, needed for reading ZIM archives.
Before use akela-zim schema you need to describe
your files like this:

[Zim]
wikisource = /home/akela/.local/share/kiwix/wikisource_ru_all_maxi_2022-09.zim
wikipedia = /home/akela/.local/share/kiwix/wikipedia_ru_all_maxi_2022-11.zim

"""
import re, requests
from akela.config import Config
from akela.zimread import ZIMREAD
from markdownify import markdownify
from libzim.reader import Archive                                             
from libzim.search import Query, Searcher                                     
from libzim.suggestion import SuggestionSearcher

isimage = lambda path: path.endswith('.webp') or \
    path.endswith('.png') or \
    path.endswith('.gif') or \
    path.endswith('.jpg') or \
    path.endswith('.jpeg') or \
    path.endswith('.bmp')

class URI:
    """ URI handler class """
    config = Config()
    resource = None
    Encod = "default"
    head = {"User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}
    def __init__(self, uri):
        """ Parse URI """
        self.rawuri = uri
        self.uri = re.match("^(([^:/?#]+):)?(//([^/?#]*))?([^?#]*)(\?([^#]*))?(#(.*))?", uri).groups()
        
    def seturi(self, uri):
        """ Parse new URI """
        self.rawuri = uri
        self.uri = re.match("^(([^:/?#]+):)?(//([^/?#]*))?([^?#]*)(\?([^#]*))?(#(.*))?", uri).groups()
        
    def namespace(self):
        """ Get protocol """
        if type(self.uri) is tuple:
            # print(f"Namespace is {self.uri[1]}")
            return self.uri[1]
    def place(self):
        """ Get place (ZIM archive or web server) """
        if type(self.uri) is tuple:
            # print(f"Place is {self.uri[3]}")
            return self.uri[3]
    def path(self):
        """ Get path to resource """
        if type(self.uri) is tuple:
            # print(f"Path is {self.uri[4]}")
            return self.uri[4]
            
    def load(self, url):
        """Load web page and try to convert it to markdown"""
        enq = self.Encod
        urli = url
        page = requests.get(urli, headers=self.head)
        if enq.lower() not in ['default', '']:
            page.encoding = enq
        page = page.text
        b = markdownify(page, heading_style="ATX")
        self.resource = b
        
    def parse(self):
        """ Handle URI """
        if isimage(self.path()):
            self.getbinary()
            return
        if self.namespace() == "akela-zim":
            fname = self.config.getzimlocation(self.place())
            zim = ZIMREAD(fname)
            zim.getarticle(self.path())
            self.resource = zim.page
        elif self.namespace() in ['http', 'https']:
            self.load(self.rawuri)
    
    def getbinary(self):
        """ Get binary resource """
        if self.namespace() == "akela-zim":
            fname = self.config.getzimlocation(self.place())
            zim = ZIMREAD(fname)
            self.resource = zim.getrawblob(self.path())
            
    def datauri(self, mime):
        """ Create data: URI for base64-encoded data """
        return f'data:{mime};base64,{self.resource}'
      
    def searchzimdoc(self, search):
        """ Search document in ZIM archive """
        if self.namespace() == "akela-zim":
            fname = self.config.getzimlocation(self.place())
            zim = ZIMREAD(fname)
            return zim.searchzimdoc(search)
