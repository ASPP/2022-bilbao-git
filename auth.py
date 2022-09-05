import json
from random import randint

def get_credentials():
    username = input('Enter your username: ')
    password = input(f'Enter your password {username}: ')
    return username, password

def read_passwdb():
    with open('passwd.json', 'r') as pwdb_file:
        pwdb = json.load(pwdb_file)
    return pwdb

def write_passwdb(pwdb):
    with open('passwd.json', 'w') as pwdb_file:
        json.dump(pwdb, pwdb_file)

def pwhash(password):
    pwh = 0
    for i, char in enumerate(password):
        pwh += (i + 1) * ord(char)
    return pwh

def add_user(pwdb, username, password):
    if username not in pwdb:
        salt = randint(100000,999999)
        x = str(salt)+password
        hash = pwhash(x)
        pwdb[username] = (salt,hash)       

def authenticate(username, password, pwdb):
    if username in pwdb:
        salt, hash = pwdb[username]
        if pwhash(str(salt)+password) == hash:
            return True
        else:
            return False
    else:
        add_user(pwdb, username, password) #make sure to add the hash into these arguments
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
