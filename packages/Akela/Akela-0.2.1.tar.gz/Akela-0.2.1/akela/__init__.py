__version__ = "0.2.1"

from sys import argv
from akela.akela import Akela

def start():
    try:
        url = argv[1]
        path = os.path.expanduser('~')+f'/.akela/library/{argv[2]}'
    except IndexError:
        print(f"Usage: {argv[0]} url name")
        print("url - адрес скачиваемой страницы")
        print("name - имя файла в каталоге ~/.akela/library/")
        return
    A = Akela()
    A.setcfg()
    A.load(url)
    with open(path, 'w') as f:
        f.write(A.pagecode)

if __name__ == "__main__":
    start()
