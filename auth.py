import json
import random

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

def pwhash(password, salt):
    pwh = 0
    for i, char in enumerate(password + salt):
        pwh += (i + 1) * ord(char)
    return pwh

def add_user(pwdb, username, password):
    if username not in pwdb:
        salt = str(random.randint(0,10000))
        pass_hash = pwhash(password, salt)
        pwdb[username] = (salt, pass_hash)
        

def authenticate(username, entered_password, pwdb):
    if username in pwdb:
        real_password_hash = pwdb[username][1]
        entered_password_hash = pwhash(entered_password, pwdb[username][0])
        if entered_password_hash == real_password_hash:
            return True
        else:
            return False
    else:
        add_user(pwdb, username, entered_password)
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
