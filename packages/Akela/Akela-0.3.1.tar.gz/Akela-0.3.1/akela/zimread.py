"""ZIM archives reader

Class ZIMREAD can extract web pages and binary data.

Web pages will be converted to Markdown and binary
data will be encoded using base64.

"""

from libzim.reader import Archive                                                               
from libzim.search import Query, Searcher                                                       
from libzim.suggestion import SuggestionSearcher
from markdownify import markdownify
from base64 import b64encode
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
    def getrawblob(self, name):
        """Returns base64-encoded blob of a file"""
        blob = bytes(self.archive.get_entry_by_path(name).get_item().content)
        return str(b64encode(blob), 'ascii')
    def savearticle(self, fname):
        """Save extracted article to a file"""
        with open(os.path.expanduser("~")+"/.akela/library/"+fname, 'w') as f:
            f.write(self.page)
          
    def searchzimdoc(self, search):
        """ Search document in ZIM archive """
        suggestion_searcher = SuggestionSearcher(self.archive)                                 
        suggestion = suggestion_searcher.suggest(search)                       
        suggestion_count = suggestion.getEstimatedMatches()                           
        return list(suggestion.getResults(0, suggestion_count))

