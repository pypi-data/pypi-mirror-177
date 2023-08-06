from __future__ import absolute_import, unicode_literals
import sys
import os
import re
import configparser
import argparse
import time
from getpass import getpass
import shutil
import logging

from blended.blended_hostlib.backend import FileSystemBackend
from blended.blended_hostlib.network import Network
from blended.blended_hostlib.controller import Controller
from blended.blended_hostlib.exceptions import BlendedException, \
    PackageNameExistsException, AccountActivationException

from blended.blendedcli.settings import *
from blended.blendedcli.settings import USER_RC as user_rc_file
from blended.blendedcli.settings import PACKAGE_LIST_RC as package_list_rc_file
from blended.blendedcli.settings import BLENDED_RC as blended_rc_file, BLENDED_DATA_DIR

os_name = sys.platform.lower()
if os_name == 'linux':
    import readline
elif os_name == 'darwin':
    import readline

if sys.version_info[0] < 3:
    from __builtin__ import raw_input as input
else:
    from builtins import input

yes = set(['yes', 'y', 'ye'])
no = set(['no', 'n'])

CACHE_DIR = IMAGE_CACHE_DIR
blended_dir = BLENDED_DIR
domain_address = DOMAIN

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        tmp_dir = sys._MEIPASS
        base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)
        data_path = BLENDED_DATA_DIR
        if not os.path.exists( os.path.join(data_path,relative_path)):
            try :
                shutil.copy(base_path,data_path)
            except Exception as e : 
                print(e)
                exit(0)
        return os.path.join(data_path,relative_path)
    except Exception:

        base_path = os.path.abspath(__file__)
    base_path = os.path.dirname(base_path) 
    return os.path.join(base_path, relative_path)

def verify_theme_dir():
    """
    """
    config = configparser.ConfigParser()
    rc_file = resource_path(user_rc_file)
    config.read(rc_file)
    theme_dir_path = config.get('Directory','directory_path')
    if theme_dir_path and os.path.exists(theme_dir_path):
        return True
    
    default_themes_dir = os.path.join( HOME_DIR, "Documents","themes")
    theme_dir_path = config.set('Directory', 'directory_path',default_themes_dir)  
    return False

def create_theme_dir():
    """
    """
    config = configparser.ConfigParser()
    rc_file = resource_path(user_rc_file)
    config.read(rc_file)
    theme_dir_path = config.get('Directory','directory_path')
    if not theme_dir_path: 
        theme_dir_path = os.path.join( HOME_DIR, "Documents","themes")
            
    config.set('Directory','directory_path',theme_dir_path)
    with open(rc_file, 'w') as fp:
        config.write(fp)
    os.system(f'bd setup ""{theme_dir_path}""')


def date_time_string():
    """Return the current time formatted for logging."""
    import time
    now = time.time()
    year, month, day, hh, mm, ss, x, y, z = time.localtime(now)
    s = "%02d/%02d/%04d %02d:%02d:%02d" % (
            day, month, year, hh, mm, ss)
    return s


def setup_logger(level=logging.DEBUG, logfile=None):
        
    class FilterClass(logging.Filter):
        """
        This is a filter to modify message printed.
        """

        def filter(self, record):
            if 'GET' in record.args: 
                # import pdb; pdb.set_trace()
                record.msg = '\r[%s] "%s %s" %s -'
                record.args = (date_time_string(), record.args[3],record.args[4],record.args[6])
                return True
            return False        
 
    log = logging.getLogger('urllib3')
    log.setLevel(level)
    log.handlers = []
    logFormatter = logging.Formatter(fmt='%(message)s')
    logFilter = FilterClass()

    # console logger
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    consoleHandler.addFilter(logFilter)
    log.addHandler(consoleHandler)
    
    # file logger
    if logfile: 
        fh = logging.FileHandler(logfile)
        log.addHandler(fh)
    
    log.propagate = True
    return log
    


def get_blended_directory_path():
    """
    :return:
    """
    config = configparser.ConfigParser()
    rc_file = resource_path(user_rc_file)
    config.read(rc_file)
    try:
        directory_path = config.get('Directory', 'directory_path')
    except (configparser.NoSectionError, configparser.NoOptionError):
        directory_path = blended_dir
    return directory_path

def get_ip_address():
    """
    :return:
    """
    config = configparser.ConfigParser()
    rc_file = resource_path(user_rc_file)
    config.read(rc_file)

    def get_host():
        try:
            host = config.get('Address', 'host')
        except (configparser.NoSectionError, configparser.NoOptionError) as exc:
            host = DOMAIN
        return host

    def get_port():

        try:
            port = config.get('Address', 'port')
        except (configparser.NoSectionError, configparser.NoOptionError) as exc:
            port = PORT
        return int(port)

    return get_host, get_port


def read_blendedrc():
    config = configparser.ConfigParser()
    working_dir = blended_dir
    rc_file_path = os.path.join(working_dir, blended_rc_file)
    try:
        config.read(rc_file_path)
        package_id = config.get('Package', 'pk')
    except (configparser.NoSectionError, configparser.NoOptionError, OSError, IOError):
        raise BlendedException("Not A valid package")
    return package_id


def check_package_name(package_name, package_id):
    """
    checks the package name is givenm from command line or and
    returns package name by reading from blendedrc or by prompt to user.
    """
    if package_name and package_id:
        return {'package_name': package_name, 'package_id': package_id}
    elif not package_name and not package_id:
        try:
            package_id = read_blendedrc()
        except BlendedException:
            package_name = input("Please Enter a valid Package Name: ")
        return {'package_name': package_name, 'package_id': package_id}
    elif package_name:
        return {'package_name': package_name}
    elif package_id and not package_name:
        return {'package_id': package_id}


def check_package_in_directory(new_name=None, package_name=None):
    """
    """
    current_dir = blended_dir
    if package_name:
        print("the given package name %s is already exist in directory" % (package_name))
        new_name = input("Enter New Name for the Package: ")
    elif not new_name and not package_name:
        new_name = input("Please Enter a Name for the Package: ")
    elif new_name and new_name in os.listdir(current_dir):
        print("the given new package name %s is already exist in directory" % (new_name))
        new_name = input("Please Re-Enter New Name for the Package: ")
    else:
        return new_name
    return check_package_in_directory(new_name)


def choice(token_choice=None):
    """
    """
    if not token_choice:
        token_choice = input('Would you like to enter the token key you get on email to activate the account [Y/N]: ').lower()
    if token_choice in yes:
        pass
    elif token_choice in no:
        pass
    else:
        token_choice = input('Please Enter y/ye/yes for YES OR /no/n for NO: ').lower()
        token_choice = choice(token_choice)
    return token_choice


def read_credentials(username, password):
    """
    read user credential from rc file
    """
    config = configparser.ConfigParser()
    user_rc_path = resource_path(user_rc_file)
    if(username == None):
        try:
            config.read(user_rc_path)
            username = config.get('USER', 'username')
        except (configparser.NoSectionError, configparser.NoOptionError, OSError, IOError):
            username = input('Enter UserName: ')
            username = account_name_validation(username)
    if(password == None):
        try:
            config.read(user_rc_path)
            username = config.get('USER', 'password')
        except (configparser.NoSectionError, configparser.NoOptionError):
            password = getpass('Enter Password: ')

    return username, password


def check_package_credentials(package_name, package_id):
    """
    """
    package_attr = check_package_name(package_name, package_id)
    package_name = package_attr.get('package_name')
    package_id = package_attr.get('package_id')
    return package_name, package_id


def get_current_account(network, user_slug):
    """
    """
    config = configparser.ConfigParser()
    rc_file = resource_path(user_rc_file)
    config.read(rc_file)
    try:
        current_account = config.get('Account', 'current_account')
    except (configparser.NoOptionError, configparser.NoSectionError):
        if user_slug:
            current_account = network.get_current_account(user_slug).slug
        else:
            current_account = 'anonymous'
        try:
            config.add_section('Account')
            config.set('Account', 'current_account', current_account)
        except configparser.DuplicateSectionError:
            config.set('Account', 'current_account', current_account)
        with open(rc_file, 'w') as file_user:
            config.write(file_user)
    return current_account


def get_current_account_old(network, user_slug):
    """
    """
    config = configparser.ConfigParser()
    rc_file = resource_path(user_rc_file)
    config.read(rc_file)
    try:
        current_account = network.get_current_account(user_slug).slug
    except Exception as e:
        try:
            if e.args[0]["status_code"] == 5113:
                current_account = user_slug
                print('\nAlert: Current Account Reset\n')
                print(e.args[0]['message'])
                try:
                    config.add_section('Account')
                    config.set('Account', 'current_account', current_account)
                except configparser.DuplicateSectionError:
                    config.set('Account', 'current_account', current_account)
                with open(rc_file, 'w') as file_user:
                    config.write(file_user)
                sys.exit(0)
        except Exception:
            pass
    try:
        current_account = config.get('Account', 'current_account')
    except (configparser.NoOptionError, configparser.NoSectionError):
        try:
            current_account = network.get_current_account(user_slug).slug
            try:
                config.add_section('Account')
                config.set('Account', 'current_account', current_account)
            except configparser.DuplicateSectionError:
                config.set('Account', 'current_account', current_account)
        except Exception as e:
            current_account = 'anonymous'
        with open(rc_file, 'w') as file_user:
            config.write(file_user)
    return current_account


def get_current_account_from_network(network, user_slug):
    """
    """
    config = configparser.ConfigParser()
    rc_file = resource_path(user_rc_file)
    config.read(rc_file)
    do_exit = False
    try:
        current_account = network.get_current_account(user_slug).slug
        try:
            config.add_section('Account')
            config.set('Account', 'current_account', current_account)
        except configparser.DuplicateSectionError:
            config.set('Account', 'current_account', current_account)
    except Exception as e:
        try:
            if e.args[0]["status_code"] == 5113:
                current_account = user_slug
                print(e.args[0]['message'])
                do_exit = True
            else:
                current_account = 'anonymous'
                return current_account
        except Exception:
            current_account = 'anonymous'
            return current_account
    with open(rc_file, 'w') as file_user:
        config.write(file_user)
    if do_exit:
        sys.exit(0)
    return current_account


def get_logged_in_account():
    """
    """
    config = configparser.ConfigParser()
    rc_file = resource_path(user_rc_file)
    config.read(rc_file)
    try:
        logged_in_account = config.get('Account', 'logged_in_account')
    except (configparser.NoOptionError, configparser.NoSectionError):
        logged_in_account = None
    return logged_in_account


def set_logged_in_user(username, **kwargs):
    """
    :param account:
    :param kwargs:
    :return:
    """
    config = configparser.ConfigParser()
    rc_file = resource_path(user_rc_file)
    config.read(rc_file)
    try:
        config.add_section('Account')
        config.set('Account', 'logged_in_account', username)
    except configparser.DuplicateSectionError:
        config.set('Account', 'logged_in_account', username)
    with open(rc_file, 'w') as file_user:
        config.write(file_user)


def set_current_account(account, **kwargs):
    """
    :param account:
    :param kwargs:
    :return:
    """
    config = configparser.ConfigParser()
    rc_file = resource_path(user_rc_file)
    config.read(rc_file)
    try:
        config.add_section('Account')
        config.set('Account', 'current_account', account)
    except configparser.DuplicateSectionError:
        config.set('Account', 'current_account', account)
    with open(rc_file, 'w') as file_user:
        config.write(file_user)


def check_password(password):
    password_check = password
    if password:
        password_check = password.strip()
    if not password_check:
        print("Error: Password is required. It may not be blank. Please try again.")
        sys.exit(1)
    return password


def login(username, password, network, signup=False):
    """
    Login method
    """
    current_user = get_current_account(network, None)  # for anonymous user
    logged_in_user = get_logged_in_account()
    if username == logged_in_user:
        active_user = current_user
    else:
        active_user = username
    username, password = read_credentials(username, password)
    blended_dir = get_blended_directory_path()
    count = 0
    while True:
        try:
            username = account_name_validation(username)
            password = check_password(password)
            response = network.login(username, password, active_user)
            break
        except AccountActivationException as exc:
            raise AccountActivationException(exc)
        except BlendedException as exc:
            try:
                if exc.args[0]['status_code'] == 5016:
                    print("Error: User does not exist.")
                    username = input("Enter Username: ").strip()
                    username = account_name_validation(username)
                    password = getpass('Enter Password: ')
                elif exc.args[0]['status_code'] == 5001:
                    count += 1
                    if count == 3:
                        print("Error: You have exceeded maximum number of incorrect password attempts. Please try again.")
                        sys.exit(1)
                    print('Error: Incorrect Password.')
                    password = getpass('Enter Password: ')
                else:
                    raise BlendedException(exc.args[0])
            except BlendedException:
                raise BlendedException(exc)

    session_key = response.session_key
    user_pk = response.slug
    network.set_sessionkey(session_key, user_pk)
    try:
        current_account = network.get_current_account(user_pk).slug
    except BlendedException as exc:
        raise BlendedException(exc)

    set_current_account(current_account)
    set_logged_in_user(username)
    current_dir = os.path.join(blended_dir, current_account)
    backend = FileSystemBackend(
            current_dir, blended_dir=blended_dir,
            current_account=current_account, blended_directory_path=blended_dir)
    backend.create_account()

    try:
        if signup:
            logged_in_user = get_logged_in_account()
            if not logged_in_user:
                logged_in_user = user_slug
            print("Hi %s, you are logged in now!" % (logged_in_user))
            controller = Controller(network, backend)
            LIST_OF_DIFF_PACKAGES = controller.copy_anonymous_to_login_user('anonymous', current_account)
            if LIST_OF_DIFF_PACKAGES:
                print("\nAlert: Conflict With This Package")
                if len(LIST_OF_DIFF_PACKAGES) > 1:
                    print("Your packages %s contains conflict. "
                          "You need to pull or push in order to sync up with the Hub."
                          % ", ".join(repr(e) for e in LIST_OF_DIFF_PACKAGES))
                else:
                    print("Your package %s contains conflict. "
                          "You need to pull or push in order to sync up with the Hub."
                          % LIST_OF_DIFF_PACKAGES[0])
    except Exception as e:
        print(e)
    return session_key, user_pk


def manage_session_key(username, password, network):
    """
    """
    if (username != None) or (password != None):
        flag = True
    else:
        flag = False

    if flag:
        # assert username != None
        # assert password != None
        try:
            session_key, user_pk = login(username, password, network)
        except AccountActivationException as exc:
            raise AccountActivationException(exc)
        except BlendedException as exc:
            print(exc)
            sys.exit(0)
    else:
        try:
            session_key, user_pk = network.get_sessionkey()
        except BlendedException:
            try:
                session_key, user_pk = login(username, password, network)
            except AccountActivationException as exc:
                raise AccountActivationException(exc)
            except BlendedException as exc:
                print(exc)
                sys.exit(0)
    # network.session_key = session_key
    return network, user_pk


def backend_initializer(current_dir):
    """
    """
    working_dir = current_dir.rsplit(os.sep, 1)
    new_dir, package_name = working_dir[0], working_dir[1]
    backend = FileSystemBackend(new_dir)
    return backend, package_name


def read_package_name_from_directory(**kwargs):
    """
    """
    current_dir = kwargs.get('current_dir')
    current_account = kwargs.get('current_account')
    blended_dir = kwargs.get('blended_dir')
    relative_package_path = kwargs.get('relative_package_path')
    preview = kwargs.get('preview', False)
    working_dir = os.getcwd()
    src_path = os.path.join(current_dir, SRC)
    if preview:
        try:
            assert os.path.exists(os.path.join(working_dir, PROJECT_JSON)) == True
            relative_package_path = working_dir.split(blended_dir)[1].split(current_account, 1)[1][1:].split(os.sep, 1)
        except AssertionError:
            # print("Either package is invalid or you are running this command from somewhere else " \
            #      "instead of package that is kept in:\n%s'%s'" % (' '*3, working_dir))
            raise AssertionError
    else:
        try:
            assert (src_path in working_dir) == True
            assert os.path.exists(os.path.join(working_dir, PROJECT_JSON)) == True
            relative_package_path = working_dir.split(blended_dir)[1].split(current_account, 1)[1][1:].split(os.sep, 1)
        except AssertionError:
            # print("Either package is invalid or you are running this command from somewhere else " \
            #       "instead of package that is kept in:\n%s'%s'" % (' '*3, src_path))
            raise AssertionError

    return relative_package_path


def create_account(username, name, password, email=None, no_login=None):
    """
    """
    backend = FileSystemBackend()
    network = Network()
    controller = Controller(network, backend)
    if email:
        kwargs = {'user_name': username, 'email': email,
                  'password': password, 'name': name
                  }
    else:
        kwargs = {'user_name': username, 'password': password, 'name': name}
    try:
        response = controller.create_account(**kwargs)
    except BlendedException as exc:
        try:
            print()
            if exc.args[0].args[0]['status_code'] == 5012:
                print("Error: User already exists.")
                sys.exit(0)
            elif exc.args[0].args[0]['status_code'] == 4035:
                error = exc.args[0].args[0]['errors']
                if 'email' in error.keys():
                    print("Error: Please enter a valid email address.")
                elif 'password' in error.keys():
                    print("Error: Password is required. It may not be blank. Please try again.")
                elif 'user_name' in error.keys():
                    print("Error: Username is required. It may not be blank. Please try again.")
                else:
                    print(error)
                sys.exit(0)
            else:
                raise BlendedException(exc)
        except Exception:
            raise BlendedException(exc)

    user_pk = response.slug
    if not no_login:
        network.set_user_pk(user_pk)
    challenge = response.to_dict().get('activationchallenge')
    try:
        solution = controller.activation_solution(challenge)
    except BlendedException as exc:
        raise BlendedException(exc)
    try:
        response = controller.update_account(username, activation_solution=solution)
    except BlendedException as exc:
        raise BlendedException(exc)

    if(no_login):
        print("Account \"%s\" is created successfully!" % (username))
    elif(no_login == False):
        response = login(username, password, network, signup=True)


def account_name_validation(account_name, action=None):
    """
    """
    user_name = account_name
    if account_name:
        user_name = account_name.strip()
    while not user_name:
        if action:
            print("Error: Account name is required. It may not be blank. Please try again.")
            sys.exit(0)
        else:
            print("Error: Username is required. It may not be blank. Please try again.")
            sys.exit(0)
        user_name = account_name
    if account_name and account_name.strip():
        if (' ' in account_name.strip()):
            print("Error: White space is not allowed in the Account Name. "
                  "Please enter a valid Account Name and try again.")
            sys.exit(0)
        account_name = account_name.strip()
    else:
        account_name = ''
        return account_name.lower()

    if not re.match(r'^([0-9]*[a-z]*[A-Z]*[-]*[_]*)*$', account_name):
        print("Error: You've entered an invalid Account Name. "
              "Accepted Account Name include alphanumeric, underscore(_) and/or dash(-).")
        sys.exit(0)
    if re.search('^\s*[0-9]', account_name) and not action:
        print('Error: Account Name should not start with a number.')
        sys.exit(0)
    return account_name.lower()


def sessionNotAllowed():
    """
    """
    print("Your session has expired. Please log in to continue or create a new account.")
    option = (input("\nDo you want to Log In? Yes/No: ")).lower()
    if option in ['y', 'yes']:
        loginAccountSessionExpired()
    else:
        option = (input("\nDo you want to create a new Account? Yes/No: ")).lower()
        if option in ['y', 'yes']:
            createAccountSessionExpired()
        else:
            sys.exit(0)


def createAccountSessionExpired(username=None, name=None, email=None, password=None, no_login=False):
    username = input('Enter UserName: ').strip()
    if not username:
        print("Error: Username is required. It may not be blank. Please try again.")
        sys.exit(0)
    username = account_name_validation(username)
    if not name:
        name = input('Enter Name: ')
    if not email:
        email = input('Enter Email: ')
    if not password:
        password = getpass('Enter Password: ')
        re_password = getpass('Enter Confirm Password: ')
        if re_password != password:
            print("Error: Confirm Password entry does not match Password.")
            sys.exit(0)
    if username.lower() == 'anonymous':
        print("Error: anonymous is not permitted as an account name.")
        sys.exit(0)
    create_account(username, name, password, email=email, no_login=no_login)


def loginAccountSessionExpired(username=None, password=None):
    if not username:
        username = input("Enter Username: ")
    if not password:
        password = getpass("Enter Password: ")

    network = Network()
    try:
        network, user_slug = manage_session_key(username, password, network)
    except KeyError:
        pass
    logged_in_user = get_logged_in_account()
    if not logged_in_user:
        logged_in_user = user_slug
    print("Hi %s, you are logged in now!" % (logged_in_user))
