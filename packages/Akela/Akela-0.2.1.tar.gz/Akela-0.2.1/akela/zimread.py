from libzim.reader import Archive                                                               
from libzim.search import Query, Searcher                                                       
from libzim.suggestion import SuggestionSearcher
from markdownify import markdownify
import os.path, os

class ZIMREAD:
    """ Class for extracting articles from ZIM arcives """
    def __init__(self, fname):
        """ Create an object """
        self.archive = Archive(fname)
    
    def getarticle(self, aname):
        """ Extract article named {aname} """
        page = self.archive.get_entry_by_path(aname).get_item().content
        page = bytes(page).decode('utf-8')
        self.page = markdownify(page, heading_style="ATX")
    def savearticle(self, fname):
        with open(os.path.expanduser("~")+"/.akela/library/"+fname, 'w') as f:
            f.write(self.page)
        
