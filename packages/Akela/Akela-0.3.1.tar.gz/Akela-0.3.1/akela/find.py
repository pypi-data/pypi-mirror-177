from sys import argv
from akela.uri import URI
from akela.config import Config
import os.path

def start():
    try:
        url = argv[1]
        query = argv[2]
    except IndexError:
        print(f"Usage: {argv[0]} uri query")
        print("uri - идентификатор *МЕСТА* (akela-zim://place)")
        print("query - имя необходимого документа")
        return
    Config().setcfg()
    A = URI(url)
    suglist = A.searchzimdoc(query)
    for sug in suglist:
        print(sug)

if __name__ == "__main__":
    start()
