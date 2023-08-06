from __future__ import absolute_import
import os
import configparser
import shutil
import sys
from distutils.dir_util import copy_tree
from cliff.command import Command
from blendedUx.blendedcli.spinner import Spinner
from blendedUx.blended_hostlib.backend import FileSystemBackend
from blendedUx.blended_hostlib.network import Network
from blendedUx.blended_hostlib.controller import Controller

from blendedUx.blendedcli.helpers import *
from blendedUx.blendedcli.settings import *
from blendedUx.blendedcli.settings import USER_RC as user_rc_file

import sys
if sys.version_info[0] < 3:
    from __builtin__ import raw_input as input
else:
    from builtins import input


class SetUp(Command):
    """
    Setup blended directory and account and login.
    """
    def get_parser(self, prog_name, **kwargs):
        parser = super(SetUp, self).get_parser(prog_name)
        parser.add_argument('directory', nargs='+', default=None, help="Needed Directory name")
        parser.add_argument('--login', nargs='?', default=None)
        parser.add_argument('--password', nargs='?', default=None)
        parser.add_argument('--set-current', nargs='?', default=None)
        parser.add_argument('--host', nargs='?', default=None)
        parser.add_argument('--port', nargs='?', type=int, default=None)
        parser.add_argument('--force', nargs='?', default=False, const=True)
        return parser

    def take_action(self, parsed_args):
        config = configparser.ConfigParser()
        directory_path = ' '.join(parsed_args.directory).strip()
        password = parsed_args.password
        username = parsed_args.login
        account_name = parsed_args.set_current
        force = parsed_args.force
        host = parsed_args.host
        port = parsed_args.port
        rc_file = resource_path(user_rc_file)
        config.read(rc_file)
        get_host, get_port = get_ip_address()
        setup_exist = False
        
        try : 
            tmp_dir = sys._MEIPASS
            themes_root_dir = os.path.join(HOME_DIR,'Documents')
        except: 
            themes_root_dir = os.path.dirname(BLENDED_DIR)
        try : 
            if not os.path.exists( os.path.dirname(directory_path)):
                theme_path = os.path.join( themes_root_dir, directory_path or 'themes' )
            else : 
                theme_path = directory_path
        except:
            theme_path = os.path.join( themes_root_dir, 'themes')
        if not os.path.exists(theme_path):
            print('Setting %s as blended package directory ...'%(theme_path))
        directory_path = theme_path
        if not host:
            host = get_host()

        if not port:
            port = get_port()

        if not directory_path:
            directory_path = get_blended_directory_path()
        else:
            directory_path = os.path.abspath(directory_path)
        if directory_path and os.path.exists(directory_path) and force:
            try:
                shutil.rmtree(directory_path)
            except:
                pass
        elif directory_path and os.path.exists(directory_path):
            decision = input('Working directory "%s" already exists. Would you like to set it ' 
                             'as blended root directory ? [y/N]: ' % (theme_path)).lower()
            if decision in yes:
                try:
                    shutil.rmtree(directory_path)
                except:
                    pass
            elif decision in no:
                directory_path = input("Please enter a new directory name: ").lower()
                if directory_path:
                    theme_path = directory_path
                    directory_path = os.path.abspath(directory_path)
                else:
                    print("Can't leave the field blank. You need to provide new directory name.")
                    sys.exit(0)
            else:
                return "You passed invalid data instead of y/yes or n/no. Please try again with setup command"
        
        try:
            config.add_section('Directory')
            config.set('Directory', 'directory_path', directory_path)
        except configparser.DuplicateSectionError:
            config.set('Directory', 'directory_path', directory_path)

        try:
            config.add_section('Address')
            config.set('Address', 'host', host)
            config.set('Address', 'port', str(port))
        except configparser.DuplicateSectionError:
            config.set('Address', 'host', host)
            config.set('Address', 'port', str(port))

        with open(rc_file, 'w') as user_file:
            config.write(user_file)        
        
        anonymous_path = os.path.join(get_blended_directory_path(), ANONYMOUS, SRC)
        if not os.path.exists(directory_path):
            if os.path.exists(anonymous_path):
                setup_exist = True
            os.makedirs(directory_path)

        anonymous_user = get_current_account(Network(), None)
        spinner = Spinner()
        if not (username and password) and (anonymous_user == ANONYMOUS) and account_name:
            print("User is not a member of the account.")
            sys.exit(0)
        if True:  #not os.path.exists(anonymous_path):
            anonymous_user = 'anonymous'
            network = Network()
            network, user_pk = manage_session_key(username, password, network)
            if not os.path.exists(os.path.join(get_blended_directory_path(), anonymous_user)):
                try:
                    os.mkdir(os.path.join(get_blended_directory_path(), anonymous_user))
                except:
                    pass
            # backend = FileSystemBackend(blended_dir=os.path.join(get_blended_directory_path(),'anonymous'))
            # FileSystemBackend(blended_dir)
            current_dir = os.path.join(directory_path, anonymous_user)
            backend = FileSystemBackend(
                                        current_dir, blended_dir=blended_dir,
                                        current_account=anonymous_user, blended_directory_path=directory_path
                                        )
            backend.create_account()
            controller = Controller(network, backend)
            try:
                spinner.start()
                controller.install_initial_packages(anonymous_user, anonymous_path)
                sys.exit(1)
                spinner.stop()
            except Exception as e:
                spinner.stop()
                print(e)

        if (anonymous_user == ANONYMOUS) and (os.path.exists(anonymous_path)) and setup_exist:
            if os.path.exists(os.path.join(get_blended_directory_path(), ANONYMOUS, LIB)):
                try:
                    shutil.rmtree(os.path.join(get_blended_directory_path(), ANONYMOUS, LIB))
                except:
                    pass
            copy_tree(os.path.join(get_blended_directory_path(), ANONYMOUS), os.path.join(directory_path, ANONYMOUS))
            try:
                shutil.rmtree(os.path.join(get_blended_directory_path(), ANONYMOUS))
            except:
                pass

        login_decision = ""  # input("Would you like to login with an existing account ? [Y/n]: ").lower()

        if account_name:
            network = Network()
            network, user_pk = manage_session_key(username, password, network)
            backend = FileSystemBackend(directory_path)
            controller = Controller(network, backend)
            try:
                response = controller.set_current_account(account_name)
            except BlendedException as exc:
                try:
                    if exc.args[0].args[0]['status_code']:
                        print(exc.args[0].args[0]['message'])
                        sys.exit(0)
                    else:
                        raise BlendedException(exc)
                except Exception:
                    raise BlendedException(exc)
            else:
                set_current_account(account_name)
        print('Your working directory is set as "%s" successfully '
              'for your account "%s".' % (theme_path, get_current_account(Network(), None)))
              
