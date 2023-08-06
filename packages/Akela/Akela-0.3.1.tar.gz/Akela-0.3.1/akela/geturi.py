from sys import argv, stdout
from akela.uri import URI
from akela.config import Config
import os.path
def start():
    try:
        url = argv[1]
    except IndexError:
        print(f"Usage: {argv[0]} uri")
        print("uri - идентификатор документа")
        return
    Config().setcfg()
    A = URI(url)
    A.parse()
    print(A.resource)

if __name__ == "__main__":
    start()
