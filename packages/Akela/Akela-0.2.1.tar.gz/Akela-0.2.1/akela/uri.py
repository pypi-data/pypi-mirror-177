import re
from akela.config import Config
from akela.zimread import ZIMREAD

class URI:
    config = Config()
    resource = None
    def __init__(self, uri):
        self.uri = re.match("^(([^:/?#]+):)?(//([^/?#]*))?([^?#]*)(\?([^#]*))?(#(.*))?", uri).groups()
        
    def namespace(self):
        if type(self.uri) is tuple:
            # print(f"Namespace is {self.uri[1]}")
            return self.uri[1]
    def place(self):
        if type(self.uri) is tuple:
            # print(f"Place is {self.uri[3]}")
            return self.uri[3]
    def path(self):
        if type(self.uri) is tuple:
            # print(f"Path is {self.uri[4]}")
            return self.uri[4]
            
    def parse(self):
        if self.namespace() == "akela-zim":
            fname = self.config.getzimlocation(self.place())
            zim = ZIMREAD(fname)
            zim.getarticle(self.path())
            self.resource = zim.page
    
            
