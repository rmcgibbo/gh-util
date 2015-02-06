import sys
import stat
import os
from os.path import isfile, isdir, join
import github3
from getpass import getpass
from . import appdirs

try:
    input = raw_input
except NameError:
    input = input

try:
    from urllib import quote_plus
except ImportError:
    from urllib.parse import quote_plus

dirs = appdirs.AppDirs('gh_util', 'rmcgibbo')


def tfa_callback():
    code = ''
    while not code:
        # The user could accidentally press Enter before being ready,
        # let's protect them from doing that.
        code = input('Enter 2FA code: ')
    return code


def authorize():
    username = input('Username: ')
    sys.stderr.write("%s's " % username)
    password = getpass(stream=sys.stderr)

    note = 'prs-since.py'
    note_url = 'http://github.com/rmcgibbo/prs-since'
    scopes = []

    auth = github3.authorize(
        username, password, scopes, note,
        note_url, two_factor_callback=tfa_callback)

    store_token(auth)
    return load_token()


def store_token(auth):
    if not isdir(dirs.user_data_dir):
        os.makedirs(dirs.user_data_dir)
    tokenfile = join(dirs.user_data_dir, '%s.token' % quote_plus('https://api.github.com'))

    if isfile(tokenfile):
        os.unlink(tokenfile)
    with open(tokenfile, 'w') as fd:
        fd.write(auth.token + '\n')
        fd.write(str(auth.id))
    os.chmod(tokenfile, stat.S_IRUSR)


def load_token():
    tokenfile = join(dirs.user_data_dir, '%s.token' % quote_plus('https://api.github.com'))
    token = id = ''
    with open(tokenfile, 'r') as fd:
        token = fd.readline().strip()
        id = fd.readline().strip()

    gh = github3.GitHub()
    gh.login(token=token)
    return gh


def github_handle():
    try:
        return load_token()
    except OSError:
        return github3.GitHub()
