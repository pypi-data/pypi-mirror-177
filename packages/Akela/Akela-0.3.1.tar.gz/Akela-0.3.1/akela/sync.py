"""Akela-sync is a tool for backing up saved documents

Before first start it MUST be configured manually.
Open you ~/.akela/bm.ini file and write 
options like these:

[Sync]
Remote = http(s)://server/directory
;server may be a domain name or IP address
User = username
Encrypt = 1
;Encrypt may be turned off using value like 0.
;If this option is not written encryption is not used.
Include = ~/.akela/*
;Include option may be useful if you use other
;directories for you documents

Encryption feature uses 7z archiver so please install it.

This tool returns 0 if no errors,
1 if server has rejected request,
2 if there aren't any settings in bm.ini
"""
from os import system
from os.path import expanduser as homedir
from configparser import ConfigParser
from sys import argv, exit
from getpass import getpass
import requests
def upload(remote, user, filename):
    """Upload filename to remote directory using requests"""
    # system(f"curl -v -T {filename} --user {user} {remote}")
    r = requests.put(f"{remote}/{filename}", data=open(homedir("~")+f"/{filename}", 'rb').read(), auth=(user, getpass("Пароль от сервера? ")))
    if r:
        print("Успешно")
        exit(0)
    else:
        print(f"Ошибка  {r.status_code}")
        exit(1)
    
def download(remote, user, filename):
    """Download file filename from remote directory using requests"""
    # system(f"curl -v --user {user} {remote}/{filename} > ~/{filename}")
    r = requests.get(f"{remote}/{filename}", auth=(user, getpass("Пароль от сервера? ")))
    with open(homedir("~")+f"/{filename}", 'wb') as f:
        print(r.status_code)
        if r:
            f.write(r.content)
            print("Успешно.")
            exit(0)
        else:
            print(f"Ошибка  {r.status_code}")
            exit(1)

def syncup():
    """Create a backup and upload it"""
    cfg = ConfigParser()
    cfg.read(homedir('~')+'/.akela/bm.ini')
    if 'Sync' not in cfg:
        print("Нет настроек синхронизации.")
        exit(2)
    user = cfg['Sync']['User']
    remote = cfg['Sync']['Remote']
    try:
        passon = cfg['Sync']['Encrypt']
    except:
        passon = '0'
    try:
        incldir = cfg['Sync']['Include']
    except:
        incldir = "~/.akela/*"
    if passon.lower() in ['yes', 'y', '1', 'on', 'enable', 'enabled']:
        p = getpass('Пароль: ')
        system(f'7z a -P{p} ~/akela.7z {incldir}')
        filename = "akela.7z"
    else:
        filename = "akela.zip"
        system(f'zip -9 ~/akela.zip {incldir}')
    upload(remote, user, filename)

def syncdown():
    """Download a backup"""
    cfg = ConfigParser()
    cfg.read(homedir('~')+'/.akela/bm.ini')
    if 'Sync' not in cfg:
        print("Нет настроек синхронизации.")
        exit(2)
    user = cfg['Sync']['User']
    remote = cfg['Sync']['Remote']
    try:
        passon = cfg['Sync']['Encrypt']
    except:
        passon = '0'
    if passon.lower() in ['yes', 'y', '1', 'on', 'enable', 'enabled']:
        filename = "akela.7z"
    else:
        filename = "akela.zip"
    download(remote, user, filename)

def help():
    prog = argv[0]
    print(f'{prog} up - загрузить данные на сервер')
    print(f'{prog} down - скачать данные с сервера')
    
def sync():
    try:
        if argv[1] == 'down':
            syncdown()
        elif argv[1] == 'up':
            syncup()
        else:
            help()
    except IndexError:
        help()
    
if __name__ == "__main__":
    sync()
