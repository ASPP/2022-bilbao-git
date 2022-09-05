import json
import random
from random import randint

def get_credentials():
    username = input('Enter your username: ')
    password = pwhash(input(f'Enter your password {username}: '))

    return username, password

def read_passwdb():
    with open('passwd.json', 'r') as pwdb_file:
        pwdb = json.load(pwdb_file)
    return pwdb

def write_passwdb(pwdb):
    with open('passwd.json', 'w') as pwdb_file:
        json.dump(pwdb, pwdb_file)
        
def pwhash(password):
    salt = random.randint(1, 1000000)
    pwh = 0
    for i, char in enumerate(password):
        pwh += (i + 1) * ord(char) + salt
    return pwh


def add_user(pwdb, username, password):
    if username not in pwdb:
        pwdb[username] = password


def authenticate(username, password, pwdb):
    if username in pwdb:
        if password == pwdb[username]:
            return True
        else:
            return False
    else:
        add_user(pwdb, username, password)
        return True

def main():
    username, password = get_credentials()
    pwdb = read_passwdb()
    status = authenticate(username, password, pwdb)
    if status:
        print('Success!')
    else:
        print('Wrong username or password!')
    write_passwdb(pwdb)

if __name__ == '__main__':
    main()
