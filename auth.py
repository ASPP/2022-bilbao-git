import getpass
import json
import pathlib
import random
import string
import tempfile

# name of the file where we store the pw database
PWDB_FLNAME = pathlib.Path('pwdb.json')

# the pw database will be stored in a temporary directory
PWDB_DEFAULTPATH =  PWDB_FLNAME

# list of valid characters for salt (only ASCII letters + digits + punctuation)
CHARS = string.ascii_letters + string.digits + string.punctuation

# length of salt
SALT_LENGTH = 5

def get_credentials():
    # get input from terminal
    username = input('Enter your username: ')
    # get password using the appropriate module, so that typed characters are not
    # echoed to the terminal
    password = getpass.getpass('Enter your password: ')
    return (username, password)

def authenticate(username, pass_text, pwdb):
    status = False
    if username in pwdb:
        # get the salt from the database
        salt = pwdb[username][1]
        # calculate hash and compare with stored hash
        if pwhash(pass_text, salt) == pwdb[username][0]:
            status = True
    return status

def add_user(username, password, salt, pwdb, pwdb_path):
    # do not try to add a username twice
    if username in pwdb:
        raise Exception('Username already exists [%s]' %username)
    else:
        pwdb[username] = (pwhash(password,salt), salt)
        write_pwdb(pwdb, pwdb_path)

def read_pwdb(pwdb_path):
    # try to read from the database
    # if anything happens, report the error!
    try:
        with open(pwdb_path, 'rt') as pwdb_file:
            pwdb = json.load(pwdb_file)
    except json.decoder.JSONDecodeError as exc:
        # this happens when the json data is invalid
        raise Exception(f'Invalid database {pwdb_path}: {exc}')
    except Exception as exc:
        # this is a catch-all condition
        raise Exception(f'Unkown error reading {pwdb_path}: {exc}')
    return pwdb

def write_pwdb(pwdb, pwdb_path):
    with open(pwdb_path, 'wt') as pwdb_file:
        json.dump(pwdb, pwdb_file)

def pwhash(pass_text, salt):
    # simple additive hash -> very insecure!
    hash_ = 0
    full_pass_text = pass_text + salt
    for idx, char in enumerate(full_pass_text):
        # use idx as a multiplier, so that shuffling the characters returns a
        # different hash
        hash_ += (idx+1)*ord(char)
    return hash_

def get_salt():
    salt_chars = random.choices(CHARS, k=SALT_LENGTH)
    return ''.join(salt_chars)

if __name__ == '__main__':
    # ask for credentials
    username, password = get_credentials()

    # if the database does not exist yet, create an empty one by default
    if not PWDB_DEFAULTPATH.exists():
        write_pwdb({}, PWDB_DEFAULTPATH)

    # load the password database from file
    pwdb = read_pwdb(PWDB_DEFAULTPATH)

    # try to authenticate
    if authenticate(username, password, pwdb):
        print('Successfully authenticated!')
    elif username not in pwdb:
        # if the user is not known, ask if a new user must be added
        ans = input('Create new user [y/n]? ')
        if ans == 'y':
            salt = get_salt()
            add_user(username, password, salt, pwdb, PWDB_DEFAULTPATH)
    else:
        # report wrong password
        print('Wrong password!')
