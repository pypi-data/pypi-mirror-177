from sys import argv
from akela.uri import URI
import os.path
def start():
    try:
        url = argv[1]
        path = os.path.expanduser('~')+f'/.akela/library/{argv[2]}'
    except IndexError:
        print(f"Usage: {argv[0]} uri name")
        print("uri - идентификатор документа")
        print("name - имя файла в каталоге ~/.akela/library/")
        return
    A = URI(url)
    A.parse()
    with open(path, 'w') as f:
        f.write(A.resource)

if __name__ == "__main__":
    start()
