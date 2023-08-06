from __future__ import absolute_import, unicode_literals
import os
import sys
import re
import json
import shutil
from getpass import getpass
if sys.version_info[0] < 3:
    from __builtin__ import raw_input as input
else:
    from builtins import input

import beautifultable
from beautifultable import BeautifulTable

from colorama import init, Fore
init()

from cliff.command import Command
from blendedUx.blended_hostlib.initializer import Route
from blendedUx.blended_hostlib.backend import FileSystemBackend
from blendedUx.blended_hostlib.network import Network
from blendedUx.blended_hostlib.controller import Controller
from blendedUx.blended_hostlib.exceptions import BlendedException, PackageNameExistsException

from blendedUx.blendedcli.spinner import Spinner
from blendedUx.blendedcli.args_setter import PackageInfo, AccountInfo
from blendedUx.blendedcli.theme_preview import theme_app, extra_files
from blendedUx.blendedcli.helpers import *
import blendedUx.blendedcli.blendedUrls as blended_urls
from blendedUx.blendedcli.blendedUrls import init as url_init

from .textcolors import *

CACHE_DIR = IMAGE_CACHE_DIR
blended_dir = BLENDED_DIR
domain_address = DOMAIN
FILE_NOT_FOUND = "file not found "
LICENSE_TYPE = ['MIT', 'BCL', 'GPL', 'BEL']
UPGRADE_TYPES = ["perpetual", "one year", None]


def convert_to_numeric_monkey_patched(item, precision):
    """
    Helper method to convert a string to float or int if possible.

    """
    return item


class StreamType(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        try:
            description = ''
            for information in values.readlines():
                description = description + information
            # print(values.readlines())
            setattr(namespace, self.dest, description)
        except AttributeError:
            setattr(namespace, self.dest, values)


def permissionNotAllowed():
    """
    """
    print("\nAlert: Operation Not Permitted")
    print('\nYou are not permitted to perform this action because you '
          'do not have the proper organizational permissions.\nIf you wish, '
          'please speak to the organization to grant you the proper permissions.')


def clonePermissionNotAllowed(package_name, title):
    """
    """
    print("\nAlert: Operation Not Permitted")
    print('\nPackage "%s"(%s) has been added to your My Designs, '
          'but has not been sent to the Hub.\nIn order to sync to the Hub, '
          'please speak to your organization to grant you the proper permissions.\n'
          'Once you get proper permissions, '
          'simply push the package to complete the clone process.' % (title, package_name))


class PackageCreate(Command):
    """
    Cammand to Create Package.
    """
    def get_parser(self, prog_name, **kwargs):
        parser = super(PackageCreate, self).get_parser(prog_name)
        parser.add_argument('package_name', nargs='?', default=None, help="Needed package name that need to be created")
        parser.add_argument('--login', nargs='?', default=None)
        parser.add_argument('--password', nargs='?', default=None)
        parser.add_argument('--type', nargs='?', default=None)
        parser.add_argument('--primary-category', nargs='?', default=None)
        parser.add_argument('--secondary-category', nargs='?', default=None)
        parser.add_argument('--description', nargs='?', const=sys.stdin, action=StreamType, default=None)
        parser.add_argument('--title', nargs='?', const=sys.stdin, action=StreamType, default=None)
        return parser

    def take_action(self, parsed_args):
        blended_dir = get_blended_directory_path()
        package_name = parsed_args.package_name
        package_title = parsed_args.title
        package_type = parsed_args.type
        primary_category = parsed_args.primary_category
        secondary_category = parsed_args.secondary_category
        error_list = []
        if not package_name:
            network, user_slug = manage_session_key(parsed_args.login, parsed_args.password, Network())
            current_account = get_current_account(network, user_slug)
            last_active = get_logged_in_account()
            current_dir = os.path.join(blended_dir, current_account)
            try:
                relative_package_path = read_package_name_from_directory(current_account=current_account,
                                                                         current_dir=current_dir,
                                                                         blended_dir=blended_dir)
                package_name = relative_package_path[1].replace(os.sep, "/")
            except AssertionError:
                package_name = input("Package Name: ")
        package_name = package_name_validation(package_name)
        if not package_title:
            package_title = input("Package Title: ")
            if not package_title:
                print("Error: Title is required. It cannot be left blank. Please try again.")
                sys.exit(0)
        if not package_type:
            print("\nPlease enter a package type or index from below list.")
            for index, items in enumerate(PACKAGES_TYPE):
                print('%s. %s' % (str(index + 1), items.capitalize()))
                #print("             %s" % items.capitalize())
            package_type = (input("Package Type: ").lower()).strip()
            try:
                if package_type not in PACKAGES_TYPE:
                    package_type = int(package_type)
                    if package_type == 0:
                        print('Error: Package Type is Invalid. Please enter a valid option.')
                        sys.exit(0)
                    package_type = PACKAGES_TYPE[package_type - 1]       
            except (ValueError, IndexError):
                print('Error: Package Type is Invalid. Please enter a valid option.')
                sys.exit(0)
        package_type = (package_type.lower()).strip()
        if package_type not in PACKAGES_TYPE:
            print('Error: Please enter a valid package type from below list:')
            for index, items in enumerate(PACKAGES_TYPE):
                print('%s. %s' % (str(index + 1), items.capitalize()))
            sys.exit(0)
        response = ""
        if (package_type in ['layout', 'other']) and (primary_category or secondary_category):
            print('Error: Layout and Other type can not have category.')
            sys.exit(0)
        error_message = "Error: Please choose a valid package category from the available set of options."
        check = True
        if package_type and package_type.lower()=='theme':
            if not primary_category:
                check = False
                print("\nFollowing are valid package categories. Please select any of these by entering the corresponding number.\n")
                for index, items in enumerate(PACKAGE_CATEGORIES):
                    print('%s. %s' % (str(index + 1), items.capitalize()))
                primary_category = (input("Primary package category: ").lower()).strip()
                try:
                    if primary_category not in PACKAGE_CATEGORIES:
                        primary_category = int(primary_category)
                        if primary_category == 0:
                            return "Error: Primary Category is Invalid. Please enter a valid option."
                        primary_category = PACKAGE_CATEGORIES[primary_category - 1]       
                except (ValueError, IndexError):
                    return "Error: Primary Category is Invalid. Please enter a valid option."
            elif primary_category.lower() not in PACKAGE_CATEGORIES:
                print('Error: Primary Category is Invalid. Please enter a valid option from below list:')
                for index, items in enumerate(PACKAGE_CATEGORIES):
                    print('%s. %s' % (str(index + 1), items.capitalize())) 
                sys.exit(0)    
            if not secondary_category:
                if check: 
                    print("\nFollowing are valid package categories. Please select any of these by entering the corresponding number.")
                    for index, items in enumerate(PACKAGE_CATEGORIES):
                        print('%s. %s' % (str(index + 1), items.capitalize()))
                secondary_category = (input("Secondary Package Category (Optional): ").lower()).strip()
                try:
                    if secondary_category and secondary_category not in PACKAGE_CATEGORIES:
                        secondary_category = int(secondary_category)
                        if secondary_category == 0:
                            return "Error: Secondary Category is Invalid. Please enter a valid option."
                        secondary_category = PACKAGE_CATEGORIES[secondary_category - 1]       
                except (ValueError, IndexError):
                    return "Error: Secondary Category is Invalid. Please enter a valid option."
            elif secondary_category.lower() not in PACKAGE_CATEGORIES:
                print('Error: Secondary Category is Invalid. Please enter a valid option from below list:')
                for index, items in enumerate(PACKAGE_CATEGORIES):
                    print('%s. %s' % (str(index + 1), items.capitalize())) 
                sys.exit(0)
            secondary_category = (secondary_category.lower()).strip()
            primary_category = (primary_category.lower()).strip()
        if parsed_args.package_name:
            network, user_slug = manage_session_key(parsed_args.login, parsed_args.password, Network())
            current_account = get_current_account(network, user_slug)
            last_active = get_logged_in_account()
            current_dir = os.path.join(blended_dir, current_account)
        package = PackageInfo(package_name=package_name,
                              package_description=parsed_args.description,
                              package_type_name=package_type,
                              package_title=package_title,
                              secondary_category=secondary_category,
                              primary_category=primary_category,
                              )
        account = AccountInfo(blended_dir=blended_dir,
                              current_dir=current_dir,
                              current_account=current_account,
                              last_active=last_active,
                              user_slug=user_slug,
                              )
        route_obj = Route(account, package)
        spinner = Spinner()
        spinner.start()
        try:
            response, error_list = route_obj.create_package(account, package)
        except BlendedException as exc:
            spinner.stop()
            try:
                if exc.args[0]['status_code'] == 5011:
                    res = exc.args[0]['msg']
                    fileErros(route_obj, res, current_account, package_name)
                    sys.exit(0)
            except Exception:
                pass
            try:
                if exc.args[1]:
                    print(exc.args[0])
                    sys.exit(0)
                else:
                    raise BlendedException(exc)
            except Exception:
                try:
                    if exc.args[0].args[0]['status_code'] == 5059:
                        print('Package with given name "%s" already exists in account "%s".' % (package_name, current_account))
                        sys.exit(0)
                    elif exc.args[0].args[0]['status_code'] == 5092:
                        print('You can not create package twice with the same name. Package "%s" is already transferred to someone.'
                              % package_name)
                        sys.exit(0)
                    elif exc.args[0].args[0]['status_code'] == 1001:
                        permissionNotAllowed()
                    elif exc.args[0].args[0]['status_code'] == 5002:
                        sessionNotAllowed()
                    elif exc.args[0].args[0]['status_code']:
                        print(exc.args[0].args[0]['message'])
                        sys.exit(0)
                    else:
                        raise BlendedException(exc)
                except Exception:
                    print(exc)
                    sys.exit(0)
        if error_list:
            for image_name in error_list:
                print("Some error in uploading image %s.\n" % (image_name))
        if response:
            spinner.stop()
            print("Package \"%s\" is created successfully." % (response))


class PackageList(Command):
    """
    Cammand to get list of Package.
    """
    def get_parser(self, prog_name, **kwargs):
        parser = super(PackageList, self).get_parser(prog_name)
        parser.add_argument('package_name', nargs='?', default=None, help="Needed package name")
        parser.add_argument('--login', nargs='?', default=None)
        parser.add_argument('--password', nargs='?', default=None)
        parser.add_argument('--account', nargs='?', default=None)
        parser.add_argument('--package-id', nargs='?', default=None)
        parser.add_argument('--share', nargs='?', default=None, const=True)
        parser.add_argument('--sent', nargs='?', default=None, const=True)
        parser.add_argument('--received', nargs='?', default=None, const=True)
        parser.add_argument('--transfer', nargs='?', default=None, const=True)
        parser.add_argument('--organizations', nargs='?', default=None, const=True)
        parser.add_argument('--published', nargs='?', default=None, const=True)
        parser.add_argument('--purchased', nargs='?', default=None, const=True)
        return parser

    def take_action(self, parsed_args):
        
        account_name = parsed_args.account
        package_name = parsed_args.package_name
        share = parsed_args.share
        transfer_by_me = parsed_args.sent
        transfer_to_me = parsed_args.received
        pending = parsed_args.transfer
        organization = parsed_args.organizations
        purchased = parsed_args.purchased
        published = parsed_args.published
        if pending:
            if (published or transfer_by_me or transfer_to_me or share or purchased or organization):
                print("Error: You can not pass multiple arguments. Please try again.")
                sys.exit(0)
        if published:
            if (transfer_by_me or transfer_to_me or share or purchased or organization):
                print("Error: You can not pass multiple arguments. Please try again.")
                sys.exit(0)
        if purchased:
            if (transfer_by_me or transfer_to_me or share or organization):
                print("Error: You can not pass multiple arguments. Please try again.")
                sys.exit(0)
        if organization:
            if (transfer_by_me or transfer_to_me or share):
                print("Error: You can not pass multiple arguments. Please try again.")
                sys.exit(0)
            print("Note: You will be getting a list of all your organization's packages having at least one snapshot version.")
        elif share and not (transfer_by_me or transfer_to_me):
            share = '1'
        elif transfer_to_me and not (transfer_by_me or share):
            transfer_to_me = '1'
        elif transfer_by_me and not (transfer_to_me or share):
            transfer_by_me = '1'
        elif (transfer_by_me or transfer_to_me or share):
            print("Error: You can not pass multiple arguments. Please try again.")
            sys.exit(0)
        if package_name:
            package_name = package_name_validation(package_name)

        spinner = Spinner()
        blended_dir = get_blended_directory_path()
        try:
            tmp_dir = sys._MEIPASS
            is_exists = verify_theme_dir()
            if not is_exists :
                create_theme_dir()
                blended_dir = get_blended_directory_path()            
        except:
            pass
        network, user_slug = manage_session_key(parsed_args.login, parsed_args.password, Network())
        current_account = get_current_account(network, user_slug)
        last_active = get_logged_in_account()
        current_dir = os.path.join(blended_dir, current_account)

        package = PackageInfo(package_name=package_name,
                              package_id=parsed_args.package_id,
                              share=share,
                              transfer_by_me=transfer_by_me,
                              transfer_to_me=transfer_to_me,
                              organization=organization,
                              published=published,
                              purchased=purchased,
                              )
        account = AccountInfo(blended_dir=blended_dir,
                              current_dir=current_dir,
                              current_account=current_account,
                              last_active=last_active,
                              user_slug=user_slug,
                              account_name=account_name
                              )
        route_obj = Route(account, package)
        transfer_result = []
        if pending:
            package.transfer_to_me = '1'
        try:
            spinner.start()
            response = route_obj.packages_list(account, package)
            if published:
                package.published = None
                package.transfer_by_me = '1'
                transfer_result = route_obj.packages_list(account, package)
            if pending:
                package.transfer_to_me = None
                package.transfer_by_me = '1'
                transfer_by_me = route_obj.packages_list(account, package)
            spinner.stop()
        except BlendedException as exc:
            spinner.stop()
            try:
                try:
                    code = exc.args[0].args[0].args[0].get('status_code', None)
                    if code == 5002:
                        sessionNotAllowed()
                        sys.exit(0)
                except Exception:
                    pass
                if exc.args[0].args[0]['status_code'] == 5014:
                    print("User is not a member of the account \"%s\"." % (account_name))
                    sys.exit(0)
                elif exc.args[0].args[0]['status_code']:
                    print(exc.args[0].args[0]['message'])
                    sys.exit(0)
                else:
                    raise BlendedException(exc)
            except Exception:
                print(exc)
                sys.exit(0)
        if current_account == 'anonymous':
            print("Package list for Account \"%s\"." % current_account)
            print(response)
            sys.exit(0)

        for transfer_item in transfer_result:
            for item in response:
                if item.name == transfer_item.name:
                    response.remove(item)

        package_list = BeautifulTable()

        if package_name:
            package_list.column_headers = ['Package_Id', 'Account']
            for item in response:
                package_list.append_row([item.pk, item.slug])
        elif pending:
            print("\nTransferred to me:")
            package_list.column_headers = ['Title', ' Package Name', 'Package Type', 'Transferred By']
            for item in response:
                package_list.append_row([item.title, item.slug, item.type, item.account])
            if package_list:
                print(package_list)
            else:
                print("There are currently no packages transferred to you.")
            package_list1 = BeautifulTable()
            print("\nMy Transfers to Other Accounts:")
            package_list1.column_headers = ['Title', ' Package Name', 'Package Type', 'Transferred To']
            for item in transfer_by_me:
                package_list1.append_row([item.title, item.slug, item.type, item.recipient])
            if package_list1:
                print(package_list1)
            else:
                print("You currently do not have any pending transfers to other accounts.")
            sys.exit(0)
        elif transfer_by_me:
            print("\nMy Transfers to Other Accounts:")
            package_list.column_headers = ['Title', ' Package Name', 'Package Type', 'Transferred To']
            for item in response:
                package_list.append_row([item.title, item.slug, item.type, item.recipient])
            if package_list:
                print(package_list)
            else:
                print("You currently do not have any pending transfers to other accounts.")
            sys.exit(0)
        elif transfer_to_me:
            print("\nTransferred to me:")
            package_list.column_headers = ['Title', ' Package Name', 'Package Type', 'Transferred By']
            for item in response:
                package_list.append_row([item.title, item.slug, item.type, item.account])
            if package_list:
                print(package_list)
            else:
                print("There are currently no packages transferred to you.")
            sys.exit(0)
        elif share:
            package_list.column_headers = ['Title', ' Package Name', 'Package Type', 'Shared By']
            for item in response:
                package_list.append_row([item.title, item.slug, item.type, item.account])
        elif organization or published or purchased:
            package_list.column_headers = ['Title', ' Package Name', 'Package Type', 'Author']
            for item in response:
                package_list.append_row([item.title, item.slug, item.type, item.account])
        else:
            package_list.column_headers = ['Title', ' Package Name', 'Package Type', 'Author']
            for item in response:
                package_list.append_row([item.title, item.slug, item.type, item.user])
        if response:
            print(package_list)
        elif organization:
            print("Error: Your organizations do not have any package which has at least one snapshot version.")
        else:
            print("\nNo Records Found.")


class GetPackage(Command):
    """
    Adds a package in library of current account.
    Also pass new name for the package by --new_name
    if the package name already exist in library.
    """
    def get_parser(self, prog_name, **kwargs):
        parser = super(GetPackage, self).get_parser(prog_name)
        parser.add_argument('package_name', nargs='?', default=None, help="Needed package name")
        parser.add_argument('--login', nargs='?', default=None)
        parser.add_argument('--password', nargs='?', default=None)
        parser.add_argument('--package-id', nargs='?', default=None)
        parser.add_argument('--license', nargs='?', default=None)
        parser.add_argument('--new-name', nargs='?', default=None)
        parser.add_argument('--label', nargs='?', default=None)
        return parser

    def take_action(self, parsed_args):
        blended_dir = get_blended_directory_path()
        package_name = parsed_args.package_name
        package_id = parsed_args.package_id
        label = parsed_args.label
        license_name = parsed_args.license
        if not package_name:
            network, user_slug = manage_session_key(parsed_args.login, parsed_args.password, Network())
            current_account = get_current_account(network, user_slug)
            last_active = get_logged_in_account()
            current_dir = os.path.join(blended_dir, current_account)
            try:
                relative_package_path = read_package_name_from_directory(
                                        current_account=current_account,
                                        current_dir=current_dir,
                                        blended_dir=blended_dir)
                package_name = relative_package_path[1].replace(os.sep, "/")
            except AssertionError:
                package_name = input("Please Enter Package Name: ")
        package_name = package_name_validation(package_name)
        if not label:
            label = input("Please enter the published version label of the package: ")
        if parsed_args.package_name:
            network, user_slug = manage_session_key(parsed_args.login, parsed_args.password, Network())
            current_account = get_current_account(network, user_slug)
            last_active = get_logged_in_account()
            current_dir = os.path.join(blended_dir, current_account)
        if current_account == 'anonymous':
            print("You are not logged in. Please log in or create an account.")
            sys.exit(0)
        package = PackageInfo(package_name=package_name,
                              package_id=parsed_args.package_id,
                              license_name=parsed_args.license,
                              new_name=parsed_args.new_name,
                              label=label
                              )
        account = AccountInfo(blended_dir=blended_dir,
                              current_dir=current_dir,
                              current_account=current_account,
                              last_active=last_active,
                              user_slug=user_slug,
                              )
        response = ""
        route_obj = Route(account, package)
        if (package_name) and (not package_id):
            try:
                response = route_obj.get_package_acquisition(account, package)
            except PackageNameExistsException:
                print('Given package name already exists in account\n')
                new_name = input('Please Enter a new-name for package:')
                package.new_name = new_name
                try:
                    response = route_obj.get_package_acquisition(account, package)
                except BlendedException as exc:
                    raise BlendedException(exc)
            except BlendedException as exc:
                try:
                    if exc.args[0].args[0]['status_code'] == 9999:
                        print("Version does not exists. Please enter a valid version.")
                        sys.exit(0)
                    elif exc.args[0].args[0]['status_code'] == 5040:
                        print('You can not get unpublished package.')
                        sys.exit(0)
                    elif exc.args[0].args[0]['status_code'] == 1001:
                        permissionNotAllowed()
                        sys.exit(0)
                    elif exc.args[0].args[0]['status_code'] == 5002:
                        sessionNotAllowed()
                        sys.exit(0)
                    elif exc.args[0].args[0]['status_code']:
                        print(exc.args[0].args[0]['message'])
                        sys.exit(0)
                    else:
                        raise BlendedException(exc)
                except Exception:
                    raise BlendedException(exc)
        elif package_id:
            print("TO-DO, Please try without package-id.")
            sys.exit(0)

        if (response) and (response.data == None):
            print('Package version %s for published license %s is Acquired successfully.' %
                  (label, license_name))
        elif response:
            print(response)


class ClonePackage(Command):
    """
    Clone a package to the filesystem.
    """
    def get_parser(self, prog_name, **kwargs):
        parser = super(ClonePackage, self).get_parser(prog_name)
        parser.add_argument('package_name', nargs='?', default=None, help="Needed package name")
        parser.add_argument('new_package_name', nargs='?', default=None, help="Needed new package name")
        parser.add_argument('--login', nargs='?', default=None)
        parser.add_argument('--password', nargs='?', default=None)
        parser.add_argument('--package-id', nargs='?', default=None)
        parser.add_argument('--new-name', nargs='?', default=None)
        parser.add_argument('--label', nargs='?', default=None)
        parser.add_argument('--description', nargs='?', default=None)
        parser.add_argument('--draft', nargs='?', default=False, const=True)
        parser.add_argument('--canonical', nargs='?', default=None, const=True)
        parser.add_argument('--no-download', nargs='?', default=False, const=True)
        parser.add_argument('--new-title', nargs='?', default=None)
        parser.add_argument('--primary-category', nargs='?', default=None)
        parser.add_argument('--secondary-category', nargs='?', default=None)
        return parser

    def take_action(self, parsed_args):
        primary_category = parsed_args.primary_category
        secondary_category = parsed_args.secondary_category
        blended_dir = get_blended_directory_path()
        package_name = parsed_args.package_name
        new_package_name = parsed_args.new_package_name
        package_id = parsed_args.package_id
        package_title = parsed_args.new_title
        new_name = parsed_args.new_name
        label = parsed_args.label
        if parsed_args.canonical:
            label = 'canonical'
        response = ""
        if label and (label.lower() == 'draft'):
            print("Version does not exist")
            sys.exit(0)
        if new_package_name and new_name:
            print("Either pass new package name with \"--new-name\" flag or "
                  "pass it after \"package name\" without \"--new-name\" flag.")
            sys.exit(0)
        elif new_package_name:
            new_name = new_package_name
        if not package_name:
            network, user_slug = manage_session_key(parsed_args.login, parsed_args.password, Network())
            current_account = get_current_account(network, user_slug)
            last_active = get_logged_in_account()
            current_dir = os.path.join(blended_dir, current_account)
            try:
                relative_package_path = read_package_name_from_directory(
                                        current_account=current_account,
                                        current_dir=current_dir,
                                        blended_dir=blended_dir)
                package_name = relative_package_path[1].replace(os.sep, "/")
            except AssertionError:
                package_name = input("Please Enter Package Name: ")
        package_name = package_name_validation(package_name)
        if not new_name:
            new_name = input('Please Enter New Package Name: ').strip()
        new_name = package_name_validation(new_name, action='clone')
        if not package_title:
            package_title = input("Please Enter New Package Title: ").strip()
            if not package_title:
                print("Error: Title is required. It cannot be left blank. Please try again.")
                sys.exit(0)

        if  parsed_args.package_name:
            network, user_slug = manage_session_key(parsed_args.login, parsed_args.password, Network())
            current_account = get_current_account(network, user_slug)
            last_active = get_logged_in_account()
            current_dir = os.path.join(blended_dir, current_account)

        package = PackageInfo(package_name=package_name,
                              package_id=package_id,
                              new_name=new_name,
                              no_download=parsed_args.no_download,
                              label=label,
                              package_description=parsed_args.description,
                              draft=parsed_args.draft,
                              package_title=package_title,
                              primary_category=primary_category,
                              cloned_package_name=None
                              )
        account = AccountInfo(blended_dir=blended_dir,
                              current_dir=current_dir,
                              current_account=current_account,
                              last_active=last_active,
                              user_slug=user_slug,
                              )
        route_obj = Route(account, package)
        package_type = route_obj.package_type(package_name, label, parsed_args.draft)
        if (package_type in ['layout', 'other']) and (primary_category or secondary_category):
            print('Error: Layout and Other type can not have category.')
            sys.exit(0)
        check = True
        if package_type and package_type.lower()=='theme':
            if not primary_category:
                check = False
                print("\nFollowing are valid package categories. Please select any of these by entering the corresponding number.\n")
                for index, items in enumerate(PACKAGE_CATEGORIES):
                    print('%s. %s' % (str(index + 1), items.capitalize()))
                primary_category = (input("Primary package category: ").lower()).strip()
                try:
                    if primary_category not in PACKAGE_CATEGORIES:
                        primary_category = int(primary_category)
                        if primary_category == 0:
                            return "Error: Primary Category is Invalid. Please enter a valid option."
                        primary_category = PACKAGE_CATEGORIES[primary_category - 1]       
                except (ValueError, IndexError):
                    return "Error: Primary Category is Invalid. Please enter a valid option."
            elif primary_category.lower() not in PACKAGE_CATEGORIES:
                print('Error: Primary Category is Invalid. Please enter a valid option from below list:')
                for index, items in enumerate(PACKAGE_CATEGORIES):
                    print('%s. %s' % (str(index + 1), items.capitalize())) 
                sys.exit(0)
                
            if not secondary_category:
                if check: 
                    print("\nFollowing are valid package categories. Please select any of these by entering the corresponding number.")
                    for index, items in enumerate(PACKAGE_CATEGORIES):
                        print('%s. %s' % (str(index + 1), items.capitalize()))
                secondary_category = (input("Secondary Package Category (Optional): ").lower()).strip()
                try:
                    if secondary_category and secondary_category not in PACKAGE_CATEGORIES:
                        secondary_category = int(secondary_category)
                        if secondary_category == 0:
                            return "Error: Secondary Category is Invalid. Please enter a valid option."
                        secondary_category = PACKAGE_CATEGORIES[secondary_category - 1]       
                except (ValueError, IndexError):
                    return "Error: Secondary Category is Invalid. Please enter a valid option."
            elif secondary_category.lower() not in PACKAGE_CATEGORIES:
                print('Error: Secondary Category is Invalid. Please enter a valid option from below list:')
                for index, items in enumerate(PACKAGE_CATEGORIES):
                    print('%s. %s' % (str(index + 1), items.capitalize())) 
                sys.exit(0)
            secondary_category = (secondary_category.lower()).strip()
            primary_category = (primary_category.lower()).strip()
        package.primary_category =  primary_category
        package.secondary_category =  secondary_category
        spinner = Spinner()
        if (package_name) and (not package_id):
            try:
                print("Please wait a moment while we clone your package.")
                spinner.start()
                response = route_obj.package_clone(account, package)
                spinner.stop()
            except BlendedException as exc:
                spinner.stop()
                try:
                    if exc.args[0].args[0].args[0].args[0].args[0]['status_code'] == 5011:
                        res = exc.args[0].args[0].args[0].args[0].args[0]['msg']
                        fileErros(route_obj, res, current_account, package_name)
                        sys.exit(0)
                    if exc.args[0].args[0].args[0].args[0].args[0]['status_code'] == 1001:
                        clonePermissionNotAllowed(new_name, package_title)
                        sys.exit(0)
                    else:
                        raise BlendedException(exc)
                except Exception:
                    pass
                try:
                    if exc.args[0].args[0].args[0].args[0].args[0].args[0]['status_code'] == 1001:
                        clonePermissionNotAllowed(new_name, package_title)
                        sys.exit(0)
                    elif exc.args[0].args[0].args[0].args[0].args[0].args[0]['status_code'] == 5120:
                        print(exc.args[0].args[0].args[0].args[0].args[0].args[0]['message'])
                        sys.exit(0)
                    else:
                        raise BlendedException(exc)
                except Exception:
                    pass
                try:
                    if exc.args[0].args[0].args[0].args[0]['status_code'] == 5002:
                        sessionNotAllowed()
                        sys.exit(0)
                    elif exc.args[0].args[0].args[0].args[0]['status_code']:
                        print(exc.args[0].args[0].args[0].args[0]['message'])
                        sys.exit(0)
                    else:
                        raise BlendedException(exc)
                except Exception:
                    print(exc)
                    sys.exit(0)
            except OSError as e:
                spinner.stop()
                print("Package with this name already exists.\n ")
                option = input("If you want to clone it with new name Press Y/N : ")
                if option == "y" or option == "Y":
                    new_name = input("Please Enter Package Name: ")
                    try:
                        package.new_name = package_name_validation(new_name, action='clone')
                        spinner.start()
                        response = route_obj.package_clone(account, package)
                        spinner.stop()
                    except BlendedException as exc:
                        spinner.stop()
                        try:
                            if exc.args[0].args[0].args[0].args[0].args[0]['status_code'] == 5011:
                                res = exc.args[0].args[0].args[0].args[0].args[0]['msg']
                                fileErros(route_obj, res, current_account, package_name)
                                sys.exit(0)
                            elif exc.args[0].args[0].args[0].args[0].args[0]['status_code'] == 1001:
                                clonePermissionNotAllowed(new_name, package_title)
                                sys.exit(0)
                            else:
                                raise BlendedException(exc)
                        except Exception:
                            pass
                        try:
                            if exc.args[0].args[0].args[0].args[0].args[0].args[0]['status_code'] == 5002:
                                sessionNotAllowed()
                                sys.exit(0)
                            elif exc.args[0].args[0].args[0].args[0].args[0].args[0]['status_code'] == 1001:
                                clonePermissionNotAllowed(new_name, package_title)
                                sys.exit(0)
                            else:
                                raise BlendedException(exc)
                        except Exception:
                            pass
                        print(exc)
                        sys.exit(0)
                    except OSError as exc:
                        spinner.stop()
                        print(exc)
                        sys.exit(0)
                else:
                    sys.exit(0)
        elif package_id:
            print("TO-DO, Please try without package-id.")
            sys.exit(0)
        else:
            print("Error: Please enter valid package name and try again.")
            sys.exit(0)
        message = "Package \"%s\" is cloned as \"%s\" and downloaded successfully." % (package_name, response)
        print(message)


class PackageExtend(Command):
    """
    Save a package to the Hub.
    """
    def get_parser(self, prog_name, **kwargs):
        parser = super(PackageExtend, self).get_parser(prog_name)
        parser.add_argument('package_name', nargs='?', default=None, help="Needed package name")
        parser.add_argument('--login', nargs='?', default=None)
        parser.add_argument('--password', nargs='?', default=None)
        parser.add_argument('--package-id', nargs='?', default=None)
        parser.add_argument('--new-name', nargs='?', default=None)
        parser.add_argument('--label', nargs='?', default=None)
        parser.add_argument('--type', nargs='?', default='theme')
        parser.add_argument('--description', nargs='?', default=None)
        parser.add_argument('--draft', nargs='?', default=False, const=True)
        parser.add_argument('--title', nargs='?', const=sys.stdin, action=StreamType, default=None)
        return parser

    def take_action(self, parsed_args):
        package_name = parsed_args.package_name
        new_name = parsed_args.new_name
        package_id = parsed_args.package_id
        package_type = (parsed_args.type).lower()
        package_title = parsed_args.title
        blended_dir = get_blended_directory_path()
        if not package_name:
            network, user_slug = manage_session_key(parsed_args.login, parsed_args.password, Network())
            current_account = get_current_account(network, user_slug)
            last_active = get_logged_in_account()
            current_dir = os.path.join(blended_dir, current_account)
            try:
                relative_package_path = read_package_name_from_directory(
                                        current_account=current_account,
                                        current_dir=current_dir,
                                        blended_dir=blended_dir)
                package_name = relative_package_path[1].replace(os.sep, "/")
            except AssertionError:
                package_name = input("Please Enter Package Name: ")
        package_name = package_name_validation(package_name)
        if not new_name:
            new_name = input("Please Enter New Package Name for the extended package: ")
        new_name = package_name_validation(new_name, action='extend')
        if package_name == new_name:
            print("A package cannot extend self. Please try with the new name.")
            sys.exit(0)
        if not new_name:
            print("Please Enter New Package Name for the extended package. "
                  "Try \"--new-name extended_package_name\".")
            sys.exit(0)
        if not package_title:
            package_title = input("Please Enter Package Title: ")
            if not package_title:
                print("Can't leave the field blank. You need to provide title of package.")
                sys.exit(0)
            package_title = package_title
        if package_type not in ('theme', 'layout'):
            print('Please enter valid package type either \"theme\" or \"layout\".')
            sys.exit(0)
        spinner = Spinner()
        spinner.start()
        if parsed_args.package_name:
            network, user_slug = manage_session_key(parsed_args.login, parsed_args.password, Network())
            current_account = get_current_account(network, user_slug)
            last_active = get_logged_in_account()
            current_dir = os.path.join(blended_dir, current_account)
        package = PackageInfo(package_name=package_name,
                              package_id=package_id,
                              new_name=new_name,
                              label=parsed_args.label,
                              package_description=parsed_args.description,
                              draft=parsed_args.draft,
                              package_type=package_type,
                              package_title=package_title,
                              )
        account = AccountInfo(blended_dir=blended_dir,
                              current_dir=current_dir,
                              current_account=current_account,
                              last_active=last_active,
                              user_slug=user_slug,
                              )
        route_obj = Route(account, package)
        response = ""
        if (package_name) and (not package_id):
            try:
                response = route_obj.package_extend(account, package)
                spinner.stop()
            except BlendedException as exc:
                spinner.stop()
                try:
                    if exc.args[0].args[0]['status_code']==5002:
                        sessionNotAllowed()
                        sys.exit(0)
                    elif exc.args[0].args[0]['status_code']:
                        print(exc.args[0].args[0]['message'])
                        sys.exit(0)
                    else:
                        raise BlendedException(exc)
                except Exception:
                    raise BlendedException(exc)
            except ValueError:
                spinner.stop()
                print("You are not logged in. Please log in or create an account.")
                sys.exit(0)
        elif package_id:
            print("TO-DO, Please try without package-id.")
            sys.exit(0)
        else:
            print("Please enter package name which you want to extend")
            sys.exit(0)
        if response:
            try:
                title1 = route_obj.get_title(current_account, package_name)
            except BlendedException as e:
                print(e.args[0]['message'])
                sys.exit(0)
            print('You have successfully extended "%s" (%s). It has been '
                  'added to your working directory.' % (title1, package_name))


class PackageSave(Command):
    """
    Save a package to the Hub.
    """
    def get_parser(self, prog_name, **kwargs):
        parser = super(PackageSave, self).get_parser(prog_name)
        parser.add_argument('package_name', nargs='?', default=None, help="Needed package name")
        parser.add_argument('--login', nargs='?', default=None)
        parser.add_argument('--password', nargs='?', default=None)
        parser.add_argument('--package-id', nargs='?', default=None)
        parser.add_argument('--force', nargs='?', default=False, const=True)
        parser.add_argument('--files', nargs='+', default=False)
        return parser

    def take_action(self, parsed_args):
        blended_dir = get_blended_directory_path()
        files = parsed_args.files
        package_name = parsed_args.package_name
        package_id = parsed_args.package_id
        if files:
            files = route_obj.sync_file_path(files)
        if not package_name:
            network, user_slug = manage_session_key(parsed_args.login, parsed_args.password, Network())
            current_account = get_current_account(network, user_slug)
            last_active = get_logged_in_account()
            current_dir = os.path.join(blended_dir, current_account)
            try:
                relative_package_path = read_package_name_from_directory(current_account=current_account,
                                                                         current_dir=current_dir,
                                                                         blended_dir=blended_dir)
                package_name = relative_package_path[1].replace(os.sep, "/")
            except AssertionError:
                package_name = input("Please Enter Package Name: ")
        package_name = package_name_validation(package_name)
        
        if parsed_args.package_name:
            network, user_slug = manage_session_key(parsed_args.login, parsed_args.password, Network())
            current_account = get_current_account(network, user_slug)
            last_active = get_logged_in_account()
            current_dir = os.path.join(blended_dir, current_account)
        if current_account == 'anonymous':
            print("You are not logged in. Please log in or create an account.")
            sys.exit(0)
        package = PackageInfo(
                    package_name=package_name,
                    package_id=package_id,
                    force=False,
                    files=files,
                    replace_from_hub_list=None
                    )
        account = AccountInfo(blended_dir=blended_dir,
                              current_dir=current_dir,
                              current_account=current_account,
                              last_active=last_active,
                              user_slug=user_slug,
                              )
        route_obj = Route(account, package)
        if (package_name) and (not package_id):
            print("Uploading Package...")
            spinner = Spinner()
            spinner.start()
            try:
                result = route_obj.push_package(account, package)
                diff_list = []
                diff_status = False
                if isinstance(result, list):
                    if files:
                        if len(result) > 1:
                            if result[0] == True:
                                spinner.stop()
                                print("incorrect file name : %s" % result[1])
                                sys.exit(0)
                            elif result[0] == 'False_flag':
                                spinner.stop()
                                print("Package has been changed. Please pull it first.")
                                sys.exit(0)
                            else:
                                package.replace_from_hub_list = result[0]
                                pack = result[1]
                                result = route_obj.push_package(account, package, pack=pack)
                    else:
                        action = result[0][0]
                        response = result[0][1]
                        pack = result[1]
                        if action == 'force' or parsed_args.force:
                            package.replace_from_hub_list = response
                            result = route_obj.push_package(account, package, pack=pack)
                        elif action == 'overwrite':
                            spinner.stop()
                            for item in response:
                                for key, value in item.items():
                                    if key == 'removed':
                                        print("These files are added on hub:%s " % [el.location for el in value])
                                    if key == 'added':
                                        print("These files are removed from hub:%s " % [el.location for el in value])
                                    if key == 'update':
                                        print("These files are updated:%s " % [el.location for el in value])
                                    if key == 'total':
                                        print("Total file differences are : %s " % [el.name for el in value])
                            package.replace_from_hub_list = response
                            option = input("\nWould you like to Push it? Press Y/N ")
                            if option == 'y' or option == 'Y':
                                spinner.start()
                                package.force = True
                                result = route_obj.push_package(account, package, pack=pack)
                            else:
                                sys.exit(0)
                        else:
                            spinner.stop()
                            for item in response:
                                for key, value in item.items():
                                    if key == 'removed':
                                        pass
                                    if key == 'added':
                                        pass
                                    if key == 'update':
                                        pass
                                    if key == 'total':
                                        print("Total file differences are : %s " % [el.name for el in value])
                            package.replace_from_hub_list = response
                            option = input("\nWould you like to Push it? Press Y/N ")
                            if option == 'y' or option == 'Y':
                                spinner.start()
                                package.force = True
                                result = route_obj.push_package(account, package, pack=pack)
                            else:
                                sys.exit(0)
                elif (parsed_args.force) or (result == "package_create"):
                    spinner.stop()
                    print("Package \"%s\" is pushed successfully." % (package_name))
                    sys.exit(0)
                else:
                    spinner.stop()
                    print("Package \"%s\" is already in sync. No push is necessary." % (package_name))
                    sys.exit()
            except BlendedException as exc:
                spinner.stop()
                try:
                    if exc.args[0].args[1]:
                        print(exc.args[0].args[0])
                        sys.exit(0)
                    else:
                        raise BlendedException(exc)
                except Exception:
                    try:
                        code = exc.args[0].args[0].args[0].args[0].get('status_code', None)
                        if code == 1001:
                            permissionNotAllowed()
                            sys.exit(0)
                    except Exception:
                        pass
                    try:
                        if exc.args[0].args[0].args[0]['status_code'] == 5011:
                            res = exc.args[0].args[0].args[0]['msg']
                            fileErros(route_obj, res, current_account, package_name)
                        elif exc.args[0].args[0].args[0]['status_code'] == 5002:
                            sessionNotAllowed()
                            sys.exit(0)
                        elif exc.args[0].args[0].args[0]['status_code'] == 1001:
                            permissionNotAllowed()
                            sys.exit(0)
                    except Exception:
                        try:
                            if exc.args[0].args[0]['status_code'] == 4036:
                                print("Package \"%s\" has been changed. Please pull it." % package_name)
                                sys.exit(0)
                            elif exc.args[0].args[0]['status_code'] == 7777:
                                print("\nAlert: Error(s) Found With Dependency Of Package\n")
                                print("Please specify name, version and unique alias in every dependency package. Please correct it in _package.json and try again.\n")
                                print(exc.args[0].args[0]['msg'])
                                sys.exit(0)
                            elif exc.args[0].args[0]['status_code'] == 5111:
                                print("\nAlert: Error(s) Found With File _package.json\n")
                                print('The following keys in file "_package.json" are required and immutable, '
                                      'therefore they cannot be deleted or modified: account, slug, type, name and user.\n'
                                      'Their expected values are as follows:\n')
                                data = exc.args[0].args[0]['packageDetailData']
                                print('account = %s\nslug = %s\nname = %s\ntype= %s\nuser = %s\n'
                                      % (data['account'], data['slug'], data['name'], data['type'], data['user']))
                                print('Please correct these in your _package.json file and try again.')
                                sys.exit(0)
                            elif exc.args[0].args[0]['status_code'] == 1001:
                                permissionNotAllowed()
                                sys.exit(0)
                            elif exc.args[0].args[0]['status_code'] == 6000:
                                 errors = exc.args[0].args[0]['message']
                                 DuplicateFileFolderError(errors, package_name)
                                 sys.exit(0)
                            elif exc.args[0].args[0]['status_code']:
                                print(exc.args[0].args[0]['message'])
                                sys.exit(0)
                            else:
                                raise BlendedException(exc)
                        except Exception:
                            try:
                                if exc.args[0]:
                                    print(exc.args[0])
                                    sys.exit(0)
                                else:
                                    raise BlendedException(exc)
                            except Exception:
                                raise BlendedException(exc)
        elif package_id:
            print("TO-DO, Please try without package-id.")
            sys.exit(0)
        else:
            print("Error: Please enter valid package name and try again.")
            sys.exit(0)
        if result:
            spinner.stop()
            if files:
                print("Files are uploaded successfully.")
            else:
                print("Package \"%s\" is pushed successfully." % (package_name))


def DuplicateFileFolderError(res, package_name):
    """
    """
    print("Alert: Inside a folder, all files and directories names are expected to be unique.\n")
    for item in res:
        print('Found "%s" duplicate in path "%s".' % (item['name'], item['path']))


def fileErros(route_obj, res, current_account, package_name):
    table = BeautifulTable()
    table.column_headers = ['File/Directory Name', 'Error']
    for item in res:
        table.append_row([item['file'], item['error']])
    try:
        title = route_obj.get_title(current_account, package_name)
    except BlendedException as e:
        print(e.args[0]['message'])
        sys.exit(0)
    print("\nError: Invalid File/Directory Found \n")
    print('Your package "%s" (%s) contains invalid '
          'file/directory. Please validate and try again.\n' % (title, package_name))
    print(table)


class DownloadPackage(Command):
    """
    Download a package to the filesystem.
    """
    def get_parser(self, prog_name, **kwargs):
        parser = super(DownloadPackage, self).get_parser(prog_name)
        parser.add_argument('package_name', nargs='?', default=None, help="Needed package name")
        parser.add_argument('--login', nargs='?', default=None)
        parser.add_argument('--password', nargs='?', default=None)
        parser.add_argument('--package-id', nargs='?', default=None)
        parser.add_argument('--label', nargs='?', default=None)
        parser.add_argument('--canonical', nargs='?', default=False, const=True)
        parser.add_argument('--update', nargs='?', default=None)
        parser.add_argument('--force', nargs='?', default=False, const=True)
        parser.add_argument('--files', nargs='+', default=False)
        return parser

    def take_action(self, parsed_args):
        setup_logger()
        blended_dir = get_blended_directory_path()
        package_name = parsed_args.package_name
        package_id = parsed_args.package_id
        canonical = parsed_args.canonical
        label = parsed_args.label
        update = parsed_args.update
        files = parsed_args.files
        if label and canonical:
            print("Please pass one flag among these two!")
            sys.exit(0)
        elif canonical:
            label = 'canonical'
        if update:
            print("TODO")
            sys.exit(0)
        
        if files:
            files = route_obj.sync_file_path(files)
        if not package_name:
            network, user_slug = manage_session_key(parsed_args.login, parsed_args.password, Network())
            current_account = get_current_account(network, user_slug)
            last_active = get_logged_in_account()
            current_dir = os.path.join(blended_dir, current_account)
            try:
                relative_package_path = read_package_name_from_directory(current_account=current_account,
                                                                         current_dir=current_dir,
                                                                         blended_dir=blended_dir)
                package_name = relative_package_path[1].replace(os.sep, "/")
            except AssertionError:
                package_name = input("Please Enter Package Name: ")
        package_name = package_name_validation(package_name)
        
        if parsed_args.package_name: 
            network, user_slug = manage_session_key(parsed_args.login, parsed_args.password, Network())
            current_account = get_current_account(network, user_slug)
            last_active = get_logged_in_account()
            current_dir = os.path.join(blended_dir, current_account)
        if current_account == 'anonymous':
            print("You are not logged in. Please log in or create an account.")
            sys.exit(0)
        response = ""
        package = PackageInfo(
                    package_name=package_name,
                    package_id=package_id,
                    draft=True,
                    label=label,
                    update=parsed_args.update,
                    force=parsed_args.force,
                    files=files,
                    replace_from_local_list=None
                    )
        account = AccountInfo(blended_dir=blended_dir,
                              current_dir=current_dir,
                              current_account=current_account,
                              last_active=last_active,
                              user_slug=user_slug,
                              )
        route_obj = Route(account, package)
        if (package_name) and (not package_id):
            print("Downloading Package ...")
            spinner = Spinner()
            spinner.start()
            try:
                result = route_obj.pull_package(account, package)
                if label:
                    spinner.stop()
                    print("Package \"%s\" is downloaded successfully with version label \"%s\"." % (package_name, result))
                    sys.exit(0)
                if FILE_NOT_FOUND == result:
                    spinner.stop()
                    print("Package \"%s\" is downloaded successfully." % (package_name))
                    sys.exit(0)
                diff_list = []
                diff_status = False
                if isinstance(result, list):
                    if not result:
                        spinner.stop()
                        if files:
                            print("Files are downloaded successfully.")
                        else:
                            print("Package \"%s\" is downloaded successfully." % (package_name))
                        sys.exit(0)
                    elif result[0][0] == 'force':
                        response = result[0][1]
                        pack = result[1]
                        for item in response:
                            for key, value in item.items():
                                if key == 'removed':
                                    for rem_item in value:
                                        try:
                                            os.remove(rem_item.location)
                                        except:
                                            try:
                                                # will delete a directory and all its contents
                                                shutil.rmtree(rem_item.location)
                                            except:
                                                pass
                                if key == 'added':
                                    diff_list.extend(value)
                                if key == 'update':
                                    diff_list.extend(value)
                        package.replace_from_local_list = diff_list
                        result = route_obj.pull_package(account, package, pack=pack)
                    else:
                        action = result[0][0]
                        response = result[0][1]
                        pack = result[1]
                        remove_file = []
                        local_added_files = []
                        spinner.stop()
                        for item in response:
                            for key, value in item.items():
                                if key == 'removed':
                                    remove_file = value
                                    local_added_files = value
                                    if action == 'overwrite':
                                        print("These changes are added on local:%s " % [el.location for el in value])
                                    if action != 'overwrite':
                                        for rem_item in value:
                                            try:
                                                os.remove(rem_item.location)
                                            except:
                                                try:
                                                    # will delete a directory and all its contents
                                                    shutil.rmtree(rem_item.location)
                                                except:
                                                    pass
                                if key == 'added':
                                    diff_list.extend(value)
                                    if action == 'overwrite':
                                        print("These changes are removed from local:%s " % [el.location for el in value])
                                if key == 'update':
                                    if action == 'overwrite':
                                        print("These files are updated:%s " % [el.location for el in value])
                                    diff_list.extend(value)
                        package.replace_from_local_list = diff_list
                        if remove_file:
                            remove_file.extend(diff_list)
                        else:
                            remove_file = diff_list
                        print("Total file differences are : %s " % [el.name for el in remove_file])
                        option = input("\nWould you like to Pull it? Press Y/N ")
                        if option == 'y' or option == 'Y':
                            spinner.start()
                            if action == 'overwrite':
                                for rem_item in local_added_files:
                                    try:
                                        os.remove(rem_item.location)
                                    except:
                                        try:
                                            # will delete a directory and all its contents
                                            shutil.rmtree(rem_item.location)
                                        except:
                                            pass
                            result = route_obj.pull_package(account, package, pack=pack)
                        else:
                            sys.exit(0)
                else:
                    spinner.stop()
                    print("Package \"%s\" is already in sync. No pull is necessary." % (package_name))
                    sys.exit(0)
            except BlendedException as exc:
                spinner.stop()
                try:
                    if exc.args[1] == 5012:
                        print(exc.args[0])
                except (IndexError, AttributeError):
                    try:
                        if exc.args[0].args[1] == 5012:
                            print(exc.args[0].args[0])
                    except (IndexError, AttributeError):
                        try:
                            if exc.args[0].args[0]['status_code'] == 5008:
                                print("Before pulling a package, please Push package \"%s\"." % (package_name))
                                sys.exit(0)
                            elif exc.args[0].args[0]['status_code'] == 1001:
                                permissionNotAllowed()
                                sys.exit(0)
                                # print("You are not allowed to download draft version of package \"%s\"." % (package_name))
                            elif exc.args[0].args[0]['status_code'] == 5002:
                                sessionNotAllowed()
                                sys.exit(0)
                            if exc.args[0].args[0]['status_code']:
                                print(exc.args[0].args[0]['message'])
                                sys.exit(0)
                            else:
                                raise BlendedException(exc)
                        except Exception:
                            print(exc)
                sys.exit(0)
            spinner.stop()
            print("Package \"%s\" is downloaded successfully." % (package_name))
        elif package_id:
            print("TO-DO, Please try without package-id.")
            sys.exit(0)
        else:
            print("Error: Please enter valid package name and try again.")
            sys.exit(0)
        if response:
            pass  # print(response)


class InstallPackage(Command):
    """
    Install Package in lib Directory
    """
    def get_parser(self, prog_name, **kwargs):
        parser = super(InstallPackage, self).get_parser(prog_name)
        parser.add_argument('package_name', nargs='?', default=None, help="Needed package name")
        parser.add_argument('--login', nargs='?', default=None)
        parser.add_argument('--password', nargs='?', default=None)
        parser.add_argument('--package-id', nargs='?', default=None)
        parser.add_argument('--label', nargs='?', default=None)
        return parser

    def take_action(self, parsed_args):
        package_name = parsed_args.package_name
        package_id = parsed_args.package_id
        if not package_name:
            package_name = input("Please Enter Fully Qualified Package Name: ")
        if package_name:
            length = len(package_name.rsplit("/"))
            if length != 2:
                print("Please enter the fully qualified name of the package \"account_name/package_name\".")
                sys.exit(0)
        package_name = package_name_validation(package_name)
        blended_dir = get_blended_directory_path()
        network, user_slug = manage_session_key(parsed_args.login, parsed_args.password, Network())
        current_account = get_current_account(network, user_slug)
        last_active = get_logged_in_account()
        current_dir = os.path.join(blended_dir, current_account)
        package = PackageInfo(package_name=package_name, package_id=package_id, label=parsed_args.label)
        account = AccountInfo(blended_dir=blended_dir,
                              current_dir=current_dir,
                              current_account=current_account,
                              last_active=last_active,
                              user_slug=user_slug,
                              )
        route_obj = Route(account, package)
        response = ""
        if (package_name) and (not package_id):
            print("Installing Package...")
            spinner = Spinner()
            spinner.start()
            try:
                response = route_obj.install_package(account, package)
            except BlendedException as exc:
                spinner.stop()
                try:
                    if exc.args[0].args[0]['status_code'] == 5002:
                        sessionNotAllowed()
                        sys.exit(0)
                    elif exc.args[0].args[0]['status_code']:
                        print(exc.args[0].args[0]['message'])
                        sys.exit(0)
                    else:
                        raise BlendedException(exc)
                except Exception:
                    raise BlendedException(exc)
            spinner.stop()
            print("Package \"%s\" is installed successfully." % (package_name))
        elif package_id:
            print("TO-DO, Please try without package-id.")
            sys.exit(0)
        else:
            print("Error: Please enter valid package name and try again.")
            sys.exit(0)
        if response:
            print(response)


class PackageUpdate(Command):
    """
    Update a package to the Hub.
    """
    def get_parser(self, prog_name, **kwargs):
        parser = super(PackageUpdate, self).get_parser(prog_name)
        parser.add_argument('package_name', nargs='?', default=None, help="Needed package name")
        parser.add_argument('source_package_name', nargs='?', default=None, help="Needed source package name")
        parser.add_argument('--login', nargs='?', default=None)
        parser.add_argument('--password', nargs='?', default=None)
        parser.add_argument('--package-id', nargs='?', default=None)
        parser.add_argument('--from', nargs='?', default=None)
        parser.add_argument('--label', nargs='?', default=None)
        parser.add_argument('--force', nargs='?', default=False, const=True)
        return parser

    def take_action(self, parsed_args):
        package_id = parsed_args.package_id
        blended_dir = get_blended_directory_path()
        package_name = parsed_args.package_name
        source_package_name = parsed_args.source_package_name
        source_package = getattr(parsed_args, 'from', None)
        if source_package_name and source_package:
            print("Either pass new package name with \"--from\" flag or "
                  "pass it after \"package name\" without \"--from\" flag.")
            sys.exit(0)
        elif source_package_name:
            source_package = source_package_name
        network, user_slug = manage_session_key(parsed_args.login, parsed_args.password, Network())
        current_account = get_current_account(network, user_slug)
        last_active = get_logged_in_account()
        current_dir = os.path.join(blended_dir, current_account)
        package = PackageInfo(package_name=package_name,
                              package_id=package_id,
                              force=parsed_args.force,
                              label=parsed_args.label,
                              source_package=source_package)
        account = AccountInfo(blended_dir=blended_dir,
                              current_dir=current_dir,
                              current_account=current_account,
                              last_active=last_active,
                              user_slug=user_slug,
                              )
        route_obj = Route(account, package)
        if not package_name:
            try:
                relative_package_path = read_package_name_from_directory(current_account=current_account,
                                                                         current_dir=current_dir,
                                                                         blended_dir=blended_dir)
                package_name = relative_package_path[1].replace(os.sep, "/")
            except AssertionError:
                package_name = input("Please Enter Package Name: ")
        package.package_name = package_name_validation(package_name)
        package_name = package.package_name

        if not source_package:
            source_package = input("Please Enter Source Package Name : ")
        package.source_package = package_name_validation(source_package)
        source_package = package.source_package

        response = ""
        spinner = Spinner()
        if package_name:
            if not source_package:
                print("please enter source_package!")
                sys.exit(0)
            try:
                spinner.start()
                response = route_obj.update_package(account, package)
                spinner.stop()
            except BlendedException as exc:
                spinner.stop()
                try:
                    if exc.args[0].args[0].args[0]['status_code'] == 4035:
                        print(exc.args[0].args[0].args[0]['errors'])
                        sys.exit(0)
                    elif exc.args[0].args[0].args[0]['status_code'] == 5011:
                        res = exc.args[0].args[0].args[0]['msg']
                        fileErros(route_obj, res, current_account, package_name)
                        sys.exit(0)
                    elif exc.args[0].args[0].args[0]['status_code'] == 5002:
                        sessionNotAllowed()
                        sys.exit(0)
                    elif exc.args[0].args[0].args[0]['status_code']:
                        print(exc.args[0].args[0].args[0]['message'])
                        sys.exit(0)
                    else:
                        raise BlendedException(exc)
                except Exception:
                    raise BlendedException(exc)
            except ValueError as exc:
                spinner.stop()
                raise ValueError(exc)
        elif package_id:
            print("TO-DO, Please try without package-id.")
            sys.exit(0)
        else:
            print("Error: Please enter valid package name and try again.")
            sys.exit(0)
        if response:
            print("Package \"%s\" is updated successfully." % (response))
        else:
            print("Both package \"%s\" and  \"%s\" are identical." % (package_name, source_package))


class PackageCompare(Command):
    """
    """
    def get_parser(self, prog_name, **kwargs):
        parser = super(PackageCompare, self).get_parser(prog_name)
        parser.add_argument('package_name', nargs='?', default=None, help="Needed package name")
        parser.add_argument('--login', nargs='?', default=None)
        parser.add_argument('--password', nargs='?', default=None)
        parser.add_argument('--package-id', nargs='?', default=None)
        parser.add_argument('--label', nargs='?', default=None)
        parser.add_argument('--files', nargs='?', default=None)
        return parser

    def take_action(self, parsed_args):
        blended_dir = get_blended_directory_path()
        package_name = parsed_args.package_name
        package_id = parsed_args.package_id
        network, user_slug = manage_session_key(parsed_args.login, parsed_args.password, Network())
        current_account = get_current_account(network, user_slug)
        last_active = get_logged_in_account()
        current_dir = os.path.join(blended_dir, current_account)
        package = PackageInfo(
                    package_name=package_name,
                    package_id=package_id,
                    label=parsed_args.label,
                    files=parsed_args.files
                    )
        account = AccountInfo(blended_dir=blended_dir,
                              current_dir=current_dir,
                              current_account=current_account,
                              last_active=last_active,
                              user_slug=user_slug,
                              )
        route_obj = Route(account, package)
        if not package_name:
            try:
                relative_package_path = read_package_name_from_directory(current_account=current_account,
                                                                         current_dir=current_dir,
                                                                         blended_dir=blended_dir)
                package_name = relative_package_path[1].replace(os.sep, "/")
            except AssertionError:
                package_name = input("Please Enter Package Name: ")
        package.package_name = package_name_validation(package_name)
        package_name = package.package_name
        if current_account == 'anonymous':
            print("You are not logged in. Please log in or create an account.")
            sys.exit(0)
        if (package_name) and (not package_id):
            try:
                result = route_obj.compare_package(account, package)
                diff_list = []
                if result:
                    change_flag = result[0]
                    response = result[1]
                    if change_flag == 'local':
                        print("\nChanges in the local package :\n")
                        for item in response:
                            for key, value in item.items():
                                if key == 'removed':
                                    print("These files are removed:%s " % [el.location for el in value])
                                if key == 'added':
                                    print("These files are added:%s " % [el.location for el in value])
                                if key == 'update':
                                    print("These files are updated:%s " % [el.location for el in value])
                                if key == 'total':
                                    print("Total file differences are : %s \n" % [el.name for el in value])
                    elif change_flag == 'hub':
                        print("\nChanges on the hub package :\n")
                        for item in response:
                            for key, value in item.items():
                                if key == 'removed':
                                    print("These files are removed:%s " % [el.location for el in value])
                                if key == 'added':
                                    print("These files are added:%s " % [el.location for el in value])
                                if key == 'update':
                                    print("These files are updated:%s " % [el.location for el in value])
                                if key == 'total':
                                    print("Total file differences are : %s \n " % [el.name for el in value])
                    else:
                        print("Package has been changed. Please SYNC it.")
                else:
                    print("Everything upto-date.")
            except BlendedException as exc:
                try:
                    if exc.args[0].args[0]['status_code'] == 5008:
                        print("Before comparing a package, please Push package \"%s\"." % (package_name))
                        sys.exit(0)
                    elif exc.args[0].args[0]['status_code'] == 5002:
                        sessionNotAllowed()
                        sys.exit(0)
                    elif exc.args[0].args[0]['status_code']:
                        print(exc.args[0].args[0]['message'])
                        sys.exit(0)
                    else:
                        raise BlendedException(exc)
                except Exception:
                    raise BlendedException(exc)
            except OSError as exc:
                print(exc)
                sys.exit(0)
        elif package_id:
            print("TO-DO, Please try without package-id.")
            sys.exit(0)
        else:
            print("Error: Please enter valid package name and try again.")
            sys.exit(0)


class PackageValidate(Command):
    """
    """
    def get_parser(self, prog_name, **kwargs):
        parser = super(PackageValidate, self).get_parser(prog_name)
        parser.add_argument('package_name', nargs='?', default=None, help="Needed package name")
        parser.add_argument('--login', nargs='?', default=None)
        parser.add_argument('--password', nargs='?', default=None)
        parser.add_argument('--package-id', nargs='?', default=None)
        parser.add_argument('--label', nargs='?', default=None)
        return parser

    def print_result(self, errors, warningOrError):

        def getCursor(position):
            return (position-1) * '-' + '^'
        indent = '  '
        for error in errors:
            location = error.get('location', {})
            if warningOrError == 'error':
                warningOrError = Fore.RED + warningOrError + Fore.RESET
            else:
                warningOrError = Fore.YELLOW + warningOrError + Fore.RESET

            print("'%s':%s:%s: %s %s: %s" % (location.get('templatePath', 'theme'), location.get('line', 0), location.get('column', 0), error.get('type', ''), warningOrError,  error.get('message', '')))
            print(location.get('lineTxt', ''))
            print(getCursor(location.get('column', 0)))

            if error.get('references', {}):
                print(2*indent + 'References:')
                for key in error.get('references', {}):
                    location = error['references'][key].get('location', {})
                    message = error['references'][key].get('message', '')
                    print(4*indent + "(%s): '%s':%s:%s: %s" % (key, location.get('templatePath', 'theme'), location.get('line', 0), location.get('column', 0), message))
                    print(4*indent + location.get('lineTxt', ''))
                    print(4*indent + getCursor(location.get('column', 0)))
            print()

    def take_action(self, parsed_args):
        package_name = parsed_args.package_name
        package_id = parsed_args.package_id
        blended_dir = get_blended_directory_path()
        if not package_name:
            network, user_slug = manage_session_key(parsed_args.login, parsed_args.password, Network())
            current_account = get_current_account(network, user_slug)
            last_active = get_logged_in_account()
            current_dir = os.path.join(blended_dir, current_account)
            try:
                relative_package_path = read_package_name_from_directory(current_account=current_account,
                                                                         current_dir=current_dir,
                                                                         blended_dir=blended_dir)
                package_name = relative_package_path[1].replace(os.sep, "/")
            except AssertionError:
                package_name = input("Please Enter Package Name: ")
        package_name = package_name_validation(package_name)
        spinner = Spinner()
        spinner.start()
        if parsed_args.package_name:
            network, user_slug = manage_session_key(parsed_args.login, parsed_args.password, Network())
            current_account = get_current_account(network, user_slug)
            last_active = get_logged_in_account()
            current_dir = os.path.join(blended_dir, current_account)
        package = PackageInfo(package_name=package_name,
                              package_id=package_id,
                              label=parsed_args.label,
                              )
        account = AccountInfo(blended_dir=blended_dir,
                              current_dir=current_dir,
                              current_account=current_account,
                              last_active=last_active,
                              user_slug=user_slug,
                              )
        route_obj = Route(account, package)
        title = ''
        try:
            title = route_obj.get_title(current_account, package_name)
        except BlendedException as e:
            pass
        error_flag = warning_flag = False
        if (package_name) and (not package_id):
            try:
                output = route_obj.package_validate(account, package)
                spinner.stop()
                if 'error' in output:
                    print(output['error']['message'])
                    return
                results = output['results']
                
                for key in results:
                    # print("Result by validator '" + key + "':")
                    result = results[key]

                    if len(result['errors']) > 0:
                        error_flag = True
                        print(Fore.RED + 'Validation failed' + Fore.RESET)
                        print(Fore.RED + 'Errors:' + Fore.RESET)
                        self.print_result(result['errors'], 'error')
                    
                    if len(result['warnings']) > 0:
                        warning_flag = True
                        print(Fore.YELLOW + 'Warnings:' + Fore.RESET)
                        self.print_result(result['warnings'], 'warning')
                    
            except BlendedException as exc:
                spinner.stop()
                if exc.args[0]['status_code']:
                    print(exc.args[0]['message'])
            except Exception as exc:
                spinner.stop()
                print(exc)
                sys.exit(0)
        elif package_id:
            print("TO-DO, Please try without package-id.")
            sys.exit(0)
        else:
            print("Error: Please enter valid package name and try again.")
            sys.exit(0)

        if not error_flag and not warning_flag:
            print('Congratulations! Your package "%s" (%s) has successfully passed validation!' % (title, package_name))        
            return    
        return {'errors': error_flag, 'warnings': warning_flag}        
class PackageSnapshot(Command):
    """
    """
    def get_parser(self, prog_name, **kwargs):
        parser = super(PackageSnapshot, self).get_parser(prog_name)
        parser.add_argument('package_name', nargs='?', default=None, help="Needed package name")
        parser.add_argument('--login', nargs='?', default=None)
        parser.add_argument('--password', nargs='?', default=None)
        parser.add_argument('--package-id', nargs='?', default=None)
        parser.add_argument('--label', nargs='?', default=None)
        parser.add_argument('--force', default=None, action='store_true')
        return parser

    def take_action(self, parsed_args):
        blended_dir = get_blended_directory_path()
        package_name = parsed_args.package_name
        package_id = parsed_args.package_id
        label = parsed_args.label
        skip_validation = parsed_args.force

        if not package_name:
            network, user_slug = manage_session_key(parsed_args.login, parsed_args.password, Network())
            current_account = get_current_account(network, user_slug)
            last_active = get_logged_in_account()
            current_dir = os.path.join(blended_dir, current_account)
            try:
                relative_package_path = read_package_name_from_directory(
                                        current_account=current_account,
                                        current_dir=current_dir,
                                        blended_dir=blended_dir)
                package_name = relative_package_path[1].replace(os.sep, "/")
            except AssertionError:
                package_name = input("Please Enter Package Name: ")
        package_name = package_name_validation(package_name)
        if not label:
            label = input("Please enter the snapshot version label of the package: ")
        if label.lower() == 'draft':
            print("You are not allowed to use \"Draft\" as a version label for a snapshot.")
            sys.exit(0)
        elif label.lower() == 'canonical':
            print("You are not allowed to use \"Canonical\" as a version label for a snapshot.")
            sys.exit(0)
        if not re.match(r'^([0-9]*[a-z]*[A-Z]*[.]*[_]*)*$', label):
            print("Error: You've entered an invalid label. "
                  "Accepted label values include alphanumeric, dot(.) and/or underscore(_).")
            sys.exit(0)
        if parsed_args.package_name:
            network, user_slug = manage_session_key(parsed_args.login, parsed_args.password, Network())
            current_account = get_current_account(network, user_slug)
            last_active = get_logged_in_account()
            current_dir = os.path.join(blended_dir, current_account)
        package = PackageInfo(package_name=package_name,
                              package_id=package_id,
                              label=label,
                              skip_validation=skip_validation)
        account = AccountInfo(blended_dir=blended_dir,
                              current_dir=current_dir,
                              current_account=current_account,
                              last_active=last_active,
                              user_slug=user_slug,
                              )
        route_obj = Route(account, package)
        if current_account == 'anonymous':
            print("You are not logged in. Please log in or create an account.")
            sys.exit(0)
            
        while True: 
            skip_validation = input("Do you want to skip package validation? Yes/No. (No): ").upper()
            if skip_validation in ["", "NO", "FALSE", "NONE"]: 
                skip_validation = False
                break
            elif skip_validation in ['YES', 'Y', 'TRUE']: 
                skip_validation = True
                break            
            else: 
                print("Error: Please provide your input only with Yes/No.")

        if not skip_validation :
            print("Validating %s ..."%package_name)          
            from blendedUx.blendedcli.blendedcli import main
            cmd = f'bd package validate {package_name}'
            flags = main(argv=cmd.split()[1:],subcommand=True)
            if flags['errors']: 
                sys.exit(0)
            elif flags['warnings']:
                print("You may continue creating snapshot despite warnings.")
                while True: 
                    flag = input("Do you want to continue creating snapshot ? Yes/No. (Yes): ").upper()
                    if flag in ["", "NO", "FALSE", "NONE"]: 
                        flag = False
                        sys.exit(0)
                    elif flag in ['YES', 'Y', 'TRUE']: 
                        flag = True
                        break            
                    else: 
                        print("Error: Please provide your input only with Yes/No.")                 
        print("Creating Snapshot ...")
        snapshot(route_obj, package, account)


class PackageCanonical(Command):
    """
    """
    def get_parser(self, prog_name, **kwargs):
        parser = super(PackageCanonical, self).get_parser(prog_name)
        parser.add_argument('package_name', nargs='?', default=None, help="Needed package name")
        parser.add_argument('--login', nargs='?', default=None)
        parser.add_argument('--password', nargs='?', default=None)
        parser.add_argument('--package-id', nargs='?', default=None)
        parser.add_argument('--label', nargs='?', default=None)
        return parser

    def take_action(self, parsed_args):
        blended_dir = get_blended_directory_path()
        package_name = parsed_args.package_name
        password = parsed_args.password
        username = parsed_args.login
        package_id = parsed_args.package_id
        label = parsed_args.label
        if not package_name:
            network, user_slug = manage_session_key(parsed_args.login, parsed_args.password, Network())
            current_account = get_current_account(network, user_slug)
            last_active = get_logged_in_account()
            current_dir = os.path.join(blended_dir, current_account)
            try:
                relative_package_path = read_package_name_from_directory(
                                        current_account=current_account,
                                        current_dir=current_dir,
                                        blended_dir=blended_dir)
                package_name = relative_package_path[1].replace(os.sep, "/")
            except AssertionError:
                package_name = input("Please Enter Package Name: ")
        package_name = package_name_validation(package_name)
        if not label and package_name:
            label = input("Please enter the canonical version label of the package: ")
        if parsed_args.package_name:
            network, user_slug = manage_session_key(parsed_args.login, parsed_args.password, Network())
            current_account = get_current_account(network, user_slug)
            last_active = get_logged_in_account()
            current_dir = os.path.join(blended_dir, current_account)
        package = PackageInfo(package_name=package_name,
                              package_id=package_id,
                              label=label,
                              )
        account = AccountInfo(blended_dir=blended_dir,
                              current_dir=current_dir,
                              current_account=current_account,
                              last_active=last_active,
                              user_slug=user_slug,
                              )
        route_obj = Route(account, package)
        if current_account == 'anonymous':
            print("You are not logged in. Please log in or create an account.")
            sys.exit(0)
        response = ""
        if (package_name) and (not package_id):
            identifiers = package_name.split("/")
            if len(identifiers) > 1:
                if (current_account == identifiers[0]):
                    package_name = identifiers[1]
                    package.package_name = package_name
                else:
                    raise BlendedException('Account name \"%s\" is not Current account or valid account.' % identifiers[0])

            try:
                response = route_obj.package_canonical(account, package)
            except BlendedException as exc:
                try:
                    status = exc.args[0].args[0]['status_code']
                    if status == 4035:
                        error = exc.args[0].args[0]['errors']
                        if 'label' in error.keys():
                            print("Label is required. It cannot be left blank. Please try again.")
                        else:
                            print(error)
                        sys.exit(0)
                    elif status == 1001:
                        permissionNotAllowed()
                        sys.exit(0)
                    elif status == 5066:
                        print("\nWarning: Canonical Not Allowed")
                        print(exc.args[0].args[0]['message'])
                        sys.exit(0)
                    elif status == 5002:
                        sessionNotAllowed()
                        sys.exit(0)
                    elif status == 5800:
                        print("\nAlert: Operation Not Permitted\n")
                        print(exc.args[0].args[0]['message'])
                        sys.exit(0)
                    elif status:
                        print(exc.args[0].args[0]['message'])
                        sys.exit(0)
                    else:
                        raise BlendedException(exc)
                except Exception:
                    raise BlendedException(exc)
        elif package_id:
            print("TO-DO, Please try without package-id.")
            sys.exit(0)
        else:
            print("Error: Please enter valid package name and try again.")
            sys.exit(0)

        if response:
            print("Package \"%s\" has been canonized and created with version label \"%s\"." % (package_name, response))


def all_license(licenses):
    """
    """
    show_licenses(licenses)

    license_name = input("Please Enter A License name from the above: ")
    try:
        license_price = licenses[license_name]
    except KeyError:
        license_name, license_price = all_license(licenses)

    return license_name, license_price


class PackagePublish(Command):
    """
    """
    def get_parser(self, prog_name, **kwargs):
        parser = super(PackagePublish, self).get_parser(prog_name)
        parser.add_argument('package_name', nargs='?', default=None, help="Needed package name")
        parser.add_argument('--login', nargs='?', default=None)
        parser.add_argument('--password', nargs='?', default=None)
        parser.add_argument('--package-id', nargs='?', default=None)
        parser.add_argument('--label', action='append', help='<Required> Set flag', default=[])
        parser.add_argument('--license-name', nargs='?', default=None)
        parser.add_argument('--license-type', nargs='?', default=None)
        parser.add_argument('--no-listed', default=True, action='store_false')
        parser.add_argument('--no-bundled', default=True, action='store_false')
        parser.add_argument('--no-auto-add', default=True, action='store_false')
        parser.add_argument('--canonical', nargs='?', default=None)
        parser.add_argument('--upgrades', nargs='?', default=None)
        parser.add_argument('--validate', nargs='?', default=False, const=True)
        parser.add_argument('--no-upgrades', nargs='?', default=True, const=None)
        parser.add_argument('--get', nargs='?', default=False, const=True)
        parser.add_argument('--price', nargs='?', default=None)
        parser.add_argument('--default', nargs='?', default=False, const=True)
        return parser

    def take_action(self, parsed_args):
        blended_dir = get_blended_directory_path()
        package_name = parsed_args.package_name
        username = parsed_args.login
        password = parsed_args.password
        package_id = parsed_args.package_id
        label = parsed_args.label
        license_name = parsed_args.license_name
        license_type = parsed_args.license_type
        allow_listed = parsed_args.no_listed
        allow_bundled = parsed_args.no_bundled
        allow_auto_add = parsed_args.no_auto_add
        if label:
            allow_auto_add = False
        upgrades = parsed_args.upgrades
        no_upgrades = parsed_args.no_upgrades
        license_price = parsed_args.price
        canonical = parsed_args.canonical
        validate = parsed_args.validate
        get = parsed_args.get
        default_publish = parsed_args.default

        defaults = {
            'license_name':         'License1',
            'license_type':         'MIT',
            'price':                0.00,
            'upgrades':             'Perpetual',
            'listed':               True,
            'auto_add_snapshots':   True,
            'allow_bundled':        True,
        }
        if default_publish:
            # print("We are publishing your package with default setting.")
            label = []
            license_name = defaults['license_name']
            license_type = defaults['license_type']
            allow_listed = defaults['listed']
            license_price = defaults['price']
            upgrades = defaults['upgrades']
            allow_bundled = defaults['allow_bundled']
            allow_auto_add = defaults['auto_add_snapshots']

        network, user_slug = manage_session_key(parsed_args.login, parsed_args.password, Network())
        current_account = get_current_account(network, user_slug)
        last_active = get_logged_in_account()
        current_dir = os.path.join(blended_dir, current_account)
        package = PackageInfo(package_name=package_name,
                              package_id=package_id,
                              label=label,
                              license_name=license_name,
                              license_type=license_type,
                              allow_listed=allow_listed,
                              allow_bundled=allow_bundled,
                              allow_auto_add=allow_auto_add,
                              upgrades=upgrades,
                              license_price=license_price,
                              canonical=False,
                              validate=validate,
                              get=get,
                              )
        account = AccountInfo(blended_dir=blended_dir,
                              current_dir=current_dir,
                              current_account=current_account,
                              last_active=last_active,
                              user_slug=user_slug,
                              )
        route_obj = Route(account, package)
        if not package_name:
            try:
                relative_package_path = read_package_name_from_directory(
                                        current_account=current_account,
                                        current_dir=current_dir,
                                        blended_dir=blended_dir)
                package_name = relative_package_path[1].replace(os.sep, "/")
            except AssertionError:
                package_name = input("Please Enter Package Name: ")
        if current_account == 'anonymous':
            print("You are not logged in. Please log in or create an account.")
            sys.exit(0)
        package.package_name = package_name_validation(package_name)
        package_name = package.package_name
        package_name, package_id = check_package_credentials(package_name, package_id)
        spinner = Spinner()
        try:
            route_obj.check_package(current_account, package_name)
        except Exception as e:
            raise e
        if (package_name) and (get):
            spinner.start()
            try:
                response = route_obj.package_publish(account, package, publication={})
                try:
                    print(json.dumps(response, indent=4, sort_keys=True))
                    spinner.stop()
                except Exception:
                    spinner.stop()
                    print(response)
                sys.exit(0)
            except BlendedException as exc:
                spinner.stop()
                raise BlendedException(exc)
        elif not package_name:
            print("Error: Please enter valid package name and try again.")
            sys.exit(0)

        package_version = []
        try:
            spinner.start()
            package_version = route_obj.get_versions_list(account, package)
            spinner.stop()
        except Exception as exc:
            spinner.stop()
            try:
                if exc.args[0].args[0]['status_code'] == 5002:
                    sessionNotAllowed()
                    sys.exit(0)
                else:
                    print(exc.args[0].args[0]['message'])
                    sys.exit(0)
            except Exception:
                pass

        if len(package_version)<2:
            # no snapshot it will return draft otherwise exception so we are checking length
            spinner.stop()
            print("\nWarning: No Snapshot in Package\n")
            print("Error: You cannot publish a package until a snapshot has been created. To do so, simply proceed with snapshot operation and take a snapshot of the package you wish to publish.")
            sys.exit(0)

        if not default_publish:
            print(COLORS.BOLDDIM + '\nLeave blank for setting default values shown in parenthesis.\nPress CTRL+C at any time to quit.\n')
            if not license_name:
                license_name = input("License Name (%s): " % defaults['license_name']).strip()
                if license_name == "":
                    license_name = defaults['license_name']
                while not license_name.isalnum():
                    print(COLORS.BOLDDIM + "Error: License name should be an alphanumeric string.")
                    license_name = input("License Name (%s): " % defaults['license_name']).strip()
                    if license_name == "":
                        license_name = defaults['license_name']
                        break
                package.license_name = license_name

            if (not license_type) or (license_type.strip().upper() not in LICENSE_TYPE):
                if license_type and license_type.strip().upper() not in LICENSE_TYPE:
                    print(COLORS.BOLDDIM + 'Error: Allowed license types are "MIT", "GPL", "BCL" and "BEL". Please choose any one of these to proceed.')
                elif license_type=="":
                    print(COLORS.BOLDDIM + 'Error: Allowed license types are "MIT", "GPL", "BCL" and "BEL". Please choose any one of these to proceed.')
                license_type = (input("License Type (%s): " % defaults['license_type']).strip()).upper()
                while True:
                    if license_type == "":
                        license_type = "MIT"
                        break
                    elif license_type in ['MIT', 'BCL', 'GPL', 'BEL']:
                        break
                    elif license_type not in LICENSE_TYPE:
                        print(COLORS.BOLDDIM + 'Error: Allowed license types are "MIT", "GPL", "BCL" and "BEL". Please choose any one of these to proceed.')
                        license_type = (input("License Type (%s): " % defaults['license_type']).strip()).upper()
                package.license_type = license_type

            if allow_listed:
                listed = (input("Allow to be listed, making it show in searches? Yes/No. (Yes): ")).upper()
                while True:
                    if listed in ['NO', 'N', 'FALSE', 'NONE']:
                        print(COLORS.BOLDDIM + 'Alert: If your license is not listed in search, the "Allow free upgrades over this time period" setting would be automatically marked as "No Upgrades".')
                        listed = False
                        break
                    elif listed in ["", 'YES', 'Y', 'TRUE']:
                        listed = True
                        break
                    else:
                        print(COLORS.BOLDDIM + 'Error: Please provide your input only with Yes/No.')
                        listed = (input("Allow to be listed, making it show in searches? Yes/No. (Yes): ")).upper()
                allow_listed = listed
                package.allow_listed = listed
            int_price = license_price
            try:
                if license_price is None:
                    price_OK = False
                else:
                    license_price = float(license_price)
                    parts = int_price.split(".")
                    parts1 = ''
                    if len(parts)>1:
                        parts1 = parts[1]
                    if (len(parts[0])>8) or (len(parts1)>2):
                        raise BlendedException()
                    price_OK = True
                    package.license_price = license_price
            except (ValueError, TypeError):
                print(COLORS.BOLDDIM + 'Error: Ensure that there are no more than 10 digits including 2 decimal places in the license price.' + COLORS.ENDC)
                price_OK = False
            except BlendedException:
                print("Error: Ensure that there are no more than 10 digits including 2 decimal places in the license price.")
                price_OK = False

            if not price_OK:
                price = input("License Price ($0.00): ")
                while True:
                    try:
                        int_price = price
                        if price == "":
                            price = 0
                        price = float(price)
                        parts = int_price.split(".")
                        parts1 = ''
                        if len(parts)>1:
                            parts1 = parts[1]
                        if (len(parts[0])>8) or (len(parts1)>2):
                            raise BlendedException()
                        break
                    except (ValueError, TypeError):
                        print(COLORS.BOLDDIM + 'Error: Ensure that there are no more than 10 digits including 2 decimal places in the license price.' + COLORS.ENDC)
                        price = input("License Price ($0.00): ")
                    except BlendedException:
                        print("Error: Ensure that there are no more than 10 digits including 2 decimal places in the license price.")
                        price = input("License Price ($0.00): ")
                license_price = price
                package.license_price = price

            if allow_auto_add:
                auto_add_snapshots = (input('Allow "Automatically publish all Snapshots for this package, including any new ones created in the future?" Yes/No. (Yes):').strip()).upper()
                while True:
                    if auto_add_snapshots in ['NO', 'N', 'FALSE', 'NONE']:
                        label_entered = input('Please enter which existing Snapshot Labels you want to publish (if listing more than one, simply separate each label with a space):')
                        label = label_entered.split()
                        if not label:
                            print("Error: Snapshot Label is required. It cannot be left blank.")
                        else:
                            auto_add_snapshots = False
                            break
                    elif auto_add_snapshots in ["", 'YES', 'Y', 'TRUE']:
                        auto_add_snapshots = True
                        break
                    else:
                        print(COLORS.BOLDDIM + "ERROR: Please provide your input with Yes or No.")
                        auto_add_snapshots = (input('Allow "Automatically publish all Snapshots for this package, including any new ones created in the future?" Yes/No. (Yes):').strip()).upper()
                allow_auto_add = auto_add_snapshots
                package.allow_auto_add = auto_add_snapshots

            if not package.allow_listed or not no_upgrades:
                package.upgrades = None
            elif not package.upgrades or (package.upgrades not in UPGRADE_TYPES):
                if not package.allow_listed:
                    package.upgrades = None
                else:
                    if upgrades not in UPGRADE_TYPES:
                        print(COLORS.BOLDDIM + 'Error: Please provide your input only with Perpetual/One Year/No Upgrades.')
                    upgrades = (input("Allow free upgrades over this time period? Perpetual/One Year/No Upgrades. (%s): " % defaults['upgrades']).strip()).upper()
                    while True:
                        if upgrades == "" or upgrades == 'PERPETUAL':
                            upgrades = 'perpetual'
                            break
                        elif upgrades == 'ONE YEAR':
                            upgrades = 'one year'
                            break
                        elif upgrades == 'NO UPGRADES':
                            upgrades = None
                            break
                        else:
                            print(COLORS.BOLDDIM + 'Error: Please provide your input only with Perpetual/One Year/No Upgrades.' + COLORS.ENDC)
                            upgrades = (input("Allow free upgrades over this time period? Perpetual/One Year/No Upgrades. (%s): " % defaults['upgrades']).strip()).upper()
                    package.upgrades = upgrades

            if allow_bundled:
                bundle_with_others = (input("Allow to be bundled with other published licenses? Yes/No. (Yes): ")).strip().upper()
                while True:
                    if bundle_with_others in ["", "TRUE", "YES", "Y"]:
                        allow_bundled = True
                        break
                    elif bundle_with_others in ["NONE", "FALSE", "NO", "N"]:
                        allow_bundled = False
                        break
                    else:
                        print(COLORS.BOLDDIM + "ERROR: Please provide your input with Yes or No.")
                        bundle_with_others = (input("Allow to be bundled with other published licenses? Yes/No. (Yes): ")).strip().upper()
                package.allow_bundled = allow_bundled
        else:
            print("Press CTRL+C at any time to quit.")
            # print(COLORS.BOLDDIM + '** NOTE: Your package will be published with default values. **')
            title = ''
            try:
                title = route_obj.get_title(current_account, package_name)
            except BlendedException as e:
                pass
            print('Note: Your package "%s" (%s) will be published '
                  'with default settings.' % (title, package_name))
        versions_l = []
        list_1 = []
        try:
            package.canonical = canonical
            if not label:
                canonical = False
            if canonical and canonical in label:
                versions_l.append({'canonical': True, 'label': canonical})
            elif canonical:
                print("canonical should be in your list selected version list")
                sys.exit(0)
            elif label:
                for item in package_version:
                    if item['canonical'] and item['version'] in label:
                        canonical = item['version']
                        versions_l.append({'canonical': True, 'label': canonical})
            for item in label:
                if item!=canonical:
                    versions_l.append({'canonical': False, 'label': item})
            for item in package_version:
                if item['version']!='draft':
                    list_1.append(item['version'])
        except Exception as exc:
            pass

        label_not_found = [item for item in label if item not in list_1]
        if label_not_found:
            spinner.stop()
            print("\nWarning: No Snapshot in Package with label \"%s\".\n" % (label_not_found))
            print("Please try with correct snapshot version.")
            sys.exit(0)

        versions = []
        publish_body = [{"license_name": license_name,
                         "license_type": license_type,
                         "price": license_price,
                         "allow_listed": allow_listed,
                         "allow_bundled": allow_bundled,
                         "allow_auto_add": allow_auto_add,
                         "upgrades": upgrades,
                         }]

        publication = {"publication": publish_body}
        if (package_name) and (license_name) and (not package_id):
            try:
                if label:
                    versions = versions_l
                    package.canonical = False
                else:
                    for item in package_version:
                        if item['version']!='draft':
                            versions.append({'canonical': item['canonical'], 'label': item['version']})
            except BlendedException as exc:
                raise BlendedException(exc)
            publish_body[0].update({'versions': versions})
        elif not license_name:
            print("Please enter valid license name and try again.")
            sys.exit(0)
        elif not label:
            print("Label is required. It cannot be left blank. Please try again.")
            sys.exit(0)
        elif package_id:
            print("TO-DO, Please try without package-id.")
            sys.exit(0)

        try:
            spinner.start()
            response = route_obj.package_publish(account, package, publication=publication)
            spinner.stop()
        except BlendedException as exc:
            spinner.stop()
            try:
                if exc.args[0].args[0]['status_code'] == 4035:
                    print(exc.args[0].args[0]['errors'])
                    sys.exit(0)
                elif exc.args[0].args[0]['status_code'] == 1001:
                    permissionNotAllowed()
                    sys.exit(0)
                elif exc.args[0].args[0]['status_code'] == 5104:
                    print("\nError: Ensure that there are no more than 10 digits including 2 decimal places in the license price.\n")
                    sys.exit(0)
                elif exc.args[0].args[0]['status_code']:
                    print(exc.args[0].args[0]['message'])
                    sys.exit(0)
                else:
                    raise BlendedException(exc)
            except Exception:
                raise BlendedException(exc)
        er = True
        val_table = BeautifulTable()
        val_table.column_headers = ["Label", 'Validation Status', 'Canonical']
        if isinstance(response, list):
            for error in response:
                try:
                    if error.get("license_type", None):
                        er = False
                        print("\nAlert: Error(s) Found in License - %s %s\n" % (license_type, license_name))
                        print(error["license_type"])
                    elif error.get("label", None):
                        print("\nWarning: No Snapshot in Package with label \"%s\".\n" % (label))
                        print("Please try with correct snapshot version.")
                    elif error.get("upgrades", None):
                        print("Package should be published with no upgrades settings and Allow to be listed, making it show in searches settings would be marked as NO.")
                    elif error.get("allow_listed", None):
                        print("\nAlert: Error(s) Found in License - %s %s\n" % (license_type, license_name))
                        print("Allow to be listed, making it show in searches: One version should be selected as canonical if this setting is set ON.")
                    elif error.get("license_name", None):
                        print("\nAlert: License Name Already Exists\n")
                        print(error["license_name"])
                    elif error.get("publication_license_does_not_exist_error", None):
                        print("\nAlert: Error(s) Found in License - %s %s\n" % (license_type, license_name))
                        print(error["publication_license_does_not_exist_error"])
                    elif error.get("license_compatibility_error", None):
                        print("\nAlert: Error(s) Found in License - %s %s\n" % (license_type, license_name))
                        for item in error["license_compatibility_error"]:
                            print(item)
                    elif error.get("downstream_publication_license_error", None):
                        print("\nAlert: Error(s) Found in License - %s %s\n" % (license_type, license_name))
                        print(error["downstream_publication_license_error"])
                    elif error.get("version_validation_status_error", None):
                        error = error["version_validation_status_error"]
                        val_table.append_row([error["label"], error["validation_status"], error["canonical"]])
                    else:
                        print(error)
                except Exception:
                    if er and error == "More than one listed license contents same settings for 'license type', 'upgrades' and 'allow listed'.":
                        pass
                    else:
                        print(error)
        elif validate and not response:
            print("The package is successfully validated.")
        else:
            print(response)

        if val_table:
            print("\nAlert: Error(s) Found in License - %s %s" % (license_type, license_name))
            print('Snapshot versions with validation status such as "FULL_PASS" or "PARTIAL_PASS" only, '
                  'are allowed to be published in a license with allow_listed as ON. License can be published with '
                  'allow listed OFF and then the license will not be listed publically.')
            print(val_table)


class PackageRetract(Command):
    """
    """
    def get_parser(self, prog_name, **kwargs):
        parser = super(PackageRetract, self).get_parser(prog_name)
        parser.add_argument('package_name', nargs='?', default=None, help="Needed package name")
        parser.add_argument('--login', nargs='?', default=None)
        parser.add_argument('--password', nargs='?', default=None)
        parser.add_argument('--package-id', nargs='?', default=None)
        parser.add_argument('--label', nargs='?', default=None)
        parser.add_argument('--license', nargs='?', default=None)
        return parser

    def take_action(self, parsed_args):
        blended_dir = get_blended_directory_path()
        package_name = parsed_args.package_name
        password = parsed_args.password
        username = parsed_args.login
        package_id = parsed_args.package_id
        label = parsed_args.label
        license_name = parsed_args.license

        if not package_name:
            package_name = input("Please Enter Package Name: ")

        network = Network()
        network, user_pk = manage_session_key(username, password, network)
        current_account = get_current_account(network, user_pk)
        current_dir = os.path.join(blended_dir, current_account)
        # if os.path.isfile(os.path.join(current_dir, blended_rc_file)):
        #    backend, package_name = backend_initializer(current_dir)
        # else:
        backend = FileSystemBackend(
            current_dir, blended_dir=blended_dir,
            current_account=current_account, blended_directory_path=blended_dir)
        controller = Controller(network, backend)
        package_name, package_id = check_package_credentials(package_name, package_id)

        if (package_name) and (not package_id):
            try:
                package_id = controller.read_package_pk(package_name)
            except BlendedException:
                response = controller.packages_list()
                package_id = controller.read_package_pk(package_name)
            try:
                response = controller.package_deletelicense(package_id, license_name)
            except BlendedException as exc:
                raise BlendedException(exc)
        elif package_id:
            print("TO-DO, Please try without package-id.")
            sys.exit(0)
        else:
            print("Error: Please enter valid package name and try again.")
            sys.exit(0)
        if response:
            print(response)


class PackageShare(Command):
    """
    """
    def get_parser(self, prog_name, **kwargs):
        parser = super(PackageShare, self).get_parser(prog_name)
        parser.add_argument('package_name', nargs='?', default=None, help="Needed package name")
        parser.add_argument('--login', nargs='?', default=None)
        parser.add_argument('--password', nargs='?', default=None)
        parser.add_argument('--package-id', nargs='?', default=None)
        parser.add_argument('--email', nargs='?', default=None)
        parser.add_argument('--with', nargs='?', default=None)
        parser.add_argument('--get', nargs='?', default=False, const=True)
        return parser

    def take_action(self, parsed_args):
        blended_dir = get_blended_directory_path()
        package_name = parsed_args.package_name
        package_id = parsed_args.package_id
        email = parsed_args.email
        get = parsed_args.get
        account_name = getattr(parsed_args, 'with', None)
        if not package_name:
            network, user_slug = manage_session_key(parsed_args.login, parsed_args.password, Network())
            current_account = get_current_account(network, user_slug)
            last_active = get_logged_in_account()
            current_dir = os.path.join(blended_dir, current_account)
            try:
                relative_package_path = read_package_name_from_directory(current_account=current_account,
                                                                         current_dir=current_dir,
                                                                         blended_dir=blended_dir)
                package_name = relative_package_path[1].replace(os.sep, "/")
            except AssertionError:
                package_name = input("Please Enter Package Name: ")
        package_name = package_name_validation(package_name)
        if not (get or account_name or email):
            account_name = input("Please enter name of the account you want to share this package with: ")
        if parsed_args.package_name:
            network, user_slug = manage_session_key(parsed_args.login, parsed_args.password, Network())
            current_account = get_current_account(network, user_slug)
            last_active = get_logged_in_account()
            current_dir = os.path.join(blended_dir, current_account)
        package = PackageInfo(package_name=package_name, package_id=package_id, get=get)
        account = AccountInfo(blended_dir=blended_dir,
                              current_dir=current_dir,
                              current_account=current_account,
                              last_active=last_active,
                              user_slug=user_slug,
                              email=email,
                              account_name=account_name,
                              )
        route_obj = Route(account, package)
        if current_account == 'anonymous':
            print("You are not logged in. Please log in or create an account.")
            sys.exit(0)
        share(route_obj, package, account)


class PackageTransfer(Command):
    """
    """
    def get_parser(self, prog_name, **kwargs):
        parser = super(PackageTransfer, self).get_parser(prog_name)
        parser.add_argument('package_name', nargs='?', default=None, help="Needed package name")
        parser.add_argument('--login', nargs='?', default=None)
        parser.add_argument('--password', nargs='?', default=None)
        parser.add_argument('--package-id', nargs='?', default=None)
        parser.add_argument('--to', nargs='?', default=None)
        parser.add_argument('--email', nargs='?', default=None)
        return parser

    def take_action(self, parsed_args):
        blended_dir = get_blended_directory_path()
        package_name = parsed_args.package_name
        package_id = parsed_args.package_id
        account_name = parsed_args.to
        email = parsed_args.email
        count = 0
        if not package_name:
            network, user_slug = manage_session_key(parsed_args.login, parsed_args.password, Network())
            current_account = get_current_account(network, user_slug)
            last_active = get_logged_in_account()
            current_dir = os.path.join(blended_dir, current_account)
            try:
                relative_package_path = read_package_name_from_directory(current_account=current_account,
                                                                         current_dir=current_dir,
                                                                         blended_dir=blended_dir)
                package_name = relative_package_path[1].replace(os.sep, "/")
            except AssertionError:
                package_name = input("Please Enter Package Name: ")
        package_name = package_name_validation(package_name)
        if (not account_name) and (not email) and package_name:
            account_name = input("Please enter name of the account you want to transfer this package to: ")
        if parsed_args.package_name:
            network, user_slug = manage_session_key(parsed_args.login, parsed_args.password, Network())
            current_account = get_current_account(network, user_slug)
            last_active = get_logged_in_account()
            current_dir = os.path.join(blended_dir, current_account)
        if current_account == 'anonymous':
            print("You are not logged in. Please log in or create an account.")
            sys.exit(0)
        package = PackageInfo(package_name=package_name,
                              package_id=package_id,
                              )
        account = AccountInfo(blended_dir=blended_dir,
                              current_dir=current_dir,
                              current_account=current_account,
                              last_active=last_active,
                              user_slug=user_slug,
                              email=email,
                              account_name=account_name,
                              )
        route_obj = Route(account, package)
        if (package_name) and (not package_id):
            try:
                response = route_obj.package_transfer(account, package)
            except BlendedException as exc:
                try:
                    if exc.args[0].args[0]['status_code'] == 4035:
                        error = exc.args[0].args[0]['errors']
                        if 'account_slug' in error.keys():
                            print("Account name is required. It cannot be left blank. Please try again.")
                        elif 'email' in error.keys():
                            print("Enter a valid email address.")
                        else:
                            print(error)
                        sys.exit(0)
                    elif exc.args[0].args[0]['status_code'] == 1001:
                        permissionNotAllowed()
                        sys.exit(0)
                    elif exc.args[0].args[0]['status_code'] == 5008:
                        print("Before transferring a package, please Push package \"%s\"." % (package_name))
                        sys.exit(0)
                    elif exc.args[0].args[0]['status_code'] == 5045:
                        print("\nError: You cannot transfer a package until your account \"%s\" has been verified. "
                              "To do so, simply verify your account and proceed to transfer.\n" % (current_account))
                        option = input("Do you want to verify your account? Yes/No: ")
                        if option in ['y', 'Y', 'YES', 'yes', 'Yes']:
                            email = input("\nPlease Enter Your Email : ")
                            try:
                                response = route_obj.account_email_verification(email)
                            except BlendedException as exc:
                                print(exc)
                                sys.exit(0)
                            except AccountActivationException as exc:
                                print(exc)
                                sys.exit(0)
                            if response:
                                print(response)
                            print("\nA verification link has been sent to your email \"%s\". Please verify your account and proceed with the rest of the HUB operations." % (email))
                        sys.exit(0)
                    elif exc.args[0].args[0]['status_code'] == 5002:
                        sessionNotAllowed()
                        sys.exit(0)
                    elif exc.args[0].args[0]['status_code'] == 4050:
                        error = exc.args[0].args[0]['error']
                        title = error[0]['title_dependency_of_package']
                        package_name = error[0]['dependency_of_package']
                        table, auto_share_packages = beatifyError(error, "share", package_list=[])
                        if table:
                            print("\nError: Private 3rd Party Dependencies")
                            print("Package \"%s\" (%s) depends on 3rd party packages, that your transferee, \"%s\", does not have access to.\n" % (title, package_name, account_name))
                            print(table)
                            print("\nAction(s) needed:")
                            print("You can either remove these dependencies from your package, or contact the 3rd party about publishing them or sharing them directly with account \"%s\"." % (account_name))
                            sys.exit(0)
                        table, auto_share_packages, count = beatifyError(error, "private", package_list=[])
                        if table:
                            print("\nWarning: Private Dependencies")
                            print("Before package \"%s\" (%s) can be transferred to \"%s\", you must share the following private dependencies:\n" % (title, package_name, account_name))
                            print(table)
                            print("\nAction(s) needed:")
                            print("You have to share all listed upstream dependencies with the account \"%s\" first and then you can transfer this package to the account \"%s\".\n" % (account_name, account_name))
                            option = input("Do you want to Share & Transfer? Press Yes/No: ")
                            if option not in ['y', 'Y', 'YES', 'yes', 'Yes']:
                                sys.exit(0)
                        table, purchase_packages = beatifyError(error, "purchase", package_list=[])
                        while True:
                            if purchase_packages:
                                print("\nWarning: 3rd Party Published Dependencies")
                                print("Package \"%s\" (%s) has the following paid published dependencies that the transferee, \"%s\", will have to purchase in order to accept this transfer. The transferee will be prompted at the transfer acceptance stage.\n" % (title, package_name, account_name))
                                print(table)
                                print("\nAction(s) needed:")
                                print("You can proceed with the transfer.\n")
                                option = input("Do you want to Transfer & Continue? Press Yes/No: ")
                                if option not in ['y', 'Y', 'YES', 'yes', 'Yes']:
                                    if not auto_share_packages:
                                        sys.exit(0)
                                    options = input("Canceling his transfer operation now will also cancel your previously approved actions.: Yes/No: ")
                                    if options in ['y', 'Y', 'YES', 'yes', 'Yes']:
                                        sys.exit(0)
                                else:
                                    break
                            else:
                                break
                        response = route_obj.package_transfer(account, package,
                                                              auto_share_packages=auto_share_packages,
                                                              purchase_packages=purchase_packages)
                    elif exc.args[0].args[0]['status_code']:
                        print(exc.args[0].args[0]['message'])
                        sys.exit(0)
                    else:
                        raise BlendedException(exc)
                except Exception:
                    raise BlendedException(exc)
        elif package_id:
            print("TO-DO, Please try without package-id.")
            sys.exit(0)
        else:
            print("Error: Please enter valid package name and try again.")
            sys.exit(0)
        if count and account_name:
            print("You have shared %s private upstream dependencies packages and also transferred package \"%s\" successfully to the account \"%s\"." % (count, package_name, account_name))
        elif account_name:
            print("You have transferred package \"%s\" successfully to the account \"%s\"." % (package_name, account_name))
        else:
            print("You have transferred package \"%s\" successfully to the email \"%s\"." % (package_name, email))


class PackageVersion(Command):
    """
    """
    def get_parser(self, prog_name, **kwargs):
        parser = super(PackageVersion, self).get_parser(prog_name)
        parser.add_argument('package_name', nargs='?', default=None, help="Needed package name")
        parser.add_argument('--login', nargs='?', default=None)
        parser.add_argument('--password', nargs='?', default=None)
        parser.add_argument('--package-id', nargs='?', default=None)
        parser.add_argument('--canonical', nargs='?', default=False, const=True)
        return parser

    def take_action(self, parsed_args):
        blended_dir = get_blended_directory_path()
        canonical = parsed_args.canonical
        package_name = parsed_args.package_name
        package_id = parsed_args.package_id
        if not package_name:
            network, user_slug = manage_session_key(parsed_args.login, parsed_args.password, Network())
            current_account = get_current_account(network, user_slug)
            last_active = get_logged_in_account()
            current_dir = os.path.join(blended_dir, current_account)
            try:
                relative_package_path = read_package_name_from_directory(current_account=current_account,
                                                                         current_dir=current_dir,
                                                                         blended_dir=blended_dir)
                package_name = relative_package_path[1].replace(os.sep, "/")
            except AssertionError:
                package_name = input("Please Enter Package Name: ")
        package_name = package_name_validation(package_name)
        if parsed_args.package_name:        
            network, user_slug = manage_session_key(parsed_args.login, parsed_args.password, Network())
            current_account = get_current_account(network, user_slug)
            last_active = get_logged_in_account()
            current_dir = os.path.join(blended_dir, current_account)
        if current_account == 'anonymous':
            print("You are not logged in. Please log in or create an account.")
            sys.exit(0)
        package = PackageInfo(package_name=package_name, package_id=package_id, canonical=canonical)
        account = AccountInfo(blended_dir=blended_dir,
                              current_dir=current_dir,
                              current_account=current_account,
                              last_active=last_active,
                              user_slug=user_slug,
                              )
        route_obj = Route(account, package)
        if (package_name) and (not package_id):
            try:
                response = route_obj.get_versions_list(account, package)
            except BlendedException as exc:
                try:
                    if exc.args[0].args[0]['status_code'] == 4035:
                        print(exc.args[0].args[0]['errors'])
                        sys.exit(0)
                    elif exc.args[0].args[0]['status_code'] == 5002:
                        sessionNotAllowed()
                        sys.exit(0)
                    elif exc.args[0].args[0]['status_code']:
                        print(exc.args[0].args[0]['message'])
                        sys.exit(0)
                    else:
                        raise BlendedException(exc)
                except Exception:
                    raise BlendedException(exc)
        elif package_id:
            print("TO-DO, Please try without package-id.")
            sys.exit(0)
        else:
            print("Error: Please enter valid package name and try again.")
            sys.exit(0)
        if response:
            if canonical:
                for item in response:
                    print("Canonical version of Package \"%s\" is \"%s\"." % (package_name, item['canonical_version']))
                sys.exit(0)
            else:
                print("Version list of Package \"%s\" : " % package_name)
            beautifultable.rows.convert_to_numeric = convert_to_numeric_monkey_patched
            table = BeautifulTable()
            table.column_headers = ['Version', 'Created date']
            for item in response:
                if item['canonical'] and item['is_set_canonical']:
                    item['version'] = item['version']+" (Canonical)"
                elif item['canonical']:
                    item['version'] = item['version']+" (Most Recent)"

                table.append_row([item['version'], item['date']])
            table.column_alignments['Version'] = BeautifulTable.ALIGN_LEFT
            print(table)
        else:
            print("Package \"%s\" does not have any snapshot version." % package_name)


class PackageRevoke(Command):
    """
    """
    def get_parser(self, prog_name, **kwargs):
        parser = super(PackageRevoke, self).get_parser(prog_name)
        parser.add_argument('package_name', nargs='?', default=None, help="Needed package name")
        parser.add_argument('--login', nargs='?', default=None)
        parser.add_argument('--password', nargs='?', default=None)
        parser.add_argument('--package-id', nargs='?', default=None)
        #parser.add_argument('--share', nargs='?', default=False, const=True)
        parser.add_argument('--share', default=False, action='store_true')
        parser.add_argument('--transfer', default=False, action='store_true')
        parser.add_argument('--account', nargs='?', default=None, const=True)
        parser.add_argument('--email',  nargs='?', default=None, const=True)
        return parser

    def take_action(self, parsed_args):
        blended_dir = get_blended_directory_path()
        package_name = parsed_args.package_name
        password = parsed_args.password
        username = parsed_args.login
        package_id = parsed_args.package_id
        account_name = parsed_args.account
        share = parsed_args.share
        transfer = parsed_args.transfer
        email = parsed_args.email
        if not package_name:
            network, user_slug = manage_session_key(parsed_args.login, parsed_args.password, Network())
            current_account = get_current_account(network, user_slug)
            last_active = get_logged_in_account()
            current_dir = os.path.join(blended_dir, current_account)
            try:
                relative_package_path = read_package_name_from_directory(current_account=current_account,
                                                                         current_dir=current_dir,
                                                                         blended_dir=blended_dir)
                package_name = relative_package_path[1].replace(os.sep, "/")
            except AssertionError:
                package_name = input("Please Enter Package Name: ")
        package_name = package_name_validation(package_name)
        if not (share or transfer):
            revoke_type = input('Please enter revoke type (Share/Transfer): ').strip()
            while True:
                if not revoke_type:
                    print("Error: Revoke type is required. It cannot be left blank. Please try again.")
                    sys.exit(0)
                if revoke_type == "share":
                    share = True
                    break
                elif revoke_type == "transfer":
                    transfer = True
                    break
                else:
                    print('Error: Please enter the revoke type either "Share" or "Transfer".')
                    revoke_type = input('Please enter revoke type (Share/Transfer): ').strip()

        if isinstance(email, bool) and isinstance(account_name, bool):
            print("Error: You can not use multiple flag --account/--email")
            sys.exit(0)
        elif isinstance(account_name, bool) and email:
            account_name = None
        elif account_name and isinstance(email, bool):
            email = None
        if email and account_name:
            print("Error: You can not use multiple flag --account/--email")
            sys.exit(0)

        check_flag = False
        if isinstance(account_name, bool):
            account_name = input("Please Enter Account Name : ")
            account_name = account_name_validation(account_name, action='revoke')
        elif isinstance(email, bool):
            email = input("Please Enter Email : ")
            check_flag = True

        if account_name:
            account_name = account_name_validation(account_name, action='revoke')
        elif share and not email:
            account_name = input("Please Enter Account Name : ")
            account_name = account_name_validation(account_name, action='revoke')

        if check_flag and not email:
            print("Error: Email is required. It may not be blank. Please try again.")
            sys.exit(0)
        if parsed_args.package_name:
            network, user_slug = manage_session_key(parsed_args.login, parsed_args.password, Network())
            current_account = get_current_account(network, user_slug)
            last_active = get_logged_in_account()
            current_dir = os.path.join(blended_dir, current_account)
        package = PackageInfo(package_name=package_name, package_id=package_id, share=share,
                              transfer=transfer)
        account = AccountInfo(blended_dir=blended_dir,
                              current_dir=current_dir,
                              current_account=current_account,
                              last_active=last_active,
                              user_slug=user_slug,
                              account_name=account_name,
                              email=email,
                              )
        if current_account == 'anonymous':
            print("You are not logged in. Please log in or create an account.")
            sys.exit(0)
        route_obj = Route(account, package)
        spinner = Spinner()
        spinner.start()
        try:
            response = route_obj.package_revoke(account, package)
            spinner.stop()
        except BlendedException as exc:
            spinner.stop()
            try:
                if exc.args[0]['status_code'] in (4035, 4036):
                    print(exc.args[0]['errors'])
                    sys.exit(0)
                elif exc.args[0]['status_code'] in (5083, 5013):
                    if account_name:
                        print('Error: The package "%s" is not shared with the account "%s".'
                              % (package_name, account_name))
                    else:
                        print('Error: The package "%s" is not shared with the email "%s".'
                              % (package_name, email))
                    sys.exit(0)
                elif exc.args[0]['status_code'] == 5093:
                    print('Error: The package "%s" is not listed in pending transfers to revoke.'
                          % (package_name))
                    sys.exit(0)
                elif exc.args[0]['status_code'] == 5008:
                    print("Error: This package cannot be found in your library. You may need to push before performing this operation. Please check and try again.")
                    sys.exit(0)
                elif exc.args[0]['status_code']:
                    print(exc.args[0]['message'])
                    sys.exit(0)
                else:
                    raise BlendedException(exc)
            except Exception:
                raise BlendedException(exc)
        response = response.to_dict()
        response = response['data']
        title = response["title"]
        account_name = response["revoked_for"]
        email_regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if share:
            if(re.search(email_regex, account_name)):
                print('Share revoke: You have successfully revoked share access of package "%s" (%s) to email "%s".' %
                      (title, package_name, account_name))
            else:
                print('Share revoke: You have successfully revoked share access of package "%s" (%s) to account "%s".' %
                      (title, package_name, account_name))
        else:
            if(re.search(email_regex, account_name)):
                print('Transfer revoke: You have successfully revoked transfer access of package "%s" (%s) to email "%s".' %
                      (title, package_name, account_name))
            else:
                print('Transfer revoke: You have successfully revoked transfer access of package "%s" (%s) to account "%s".' %
                      (title, package_name, account_name))


class PackageAccept(Command):
    """
    Command to accept inivitaion of Account.
    """
    def get_parser(self, prog_name, **kwargs):
        parser = super(PackageAccept, self).get_parser(prog_name)
        parser.add_argument('package_name', nargs='?', default=None, help="Needed package name")
        parser.add_argument('--login', nargs='?', default=None)
        parser.add_argument('--password', nargs='?', default=None)
        parser.add_argument('--package-id', nargs='?', default=None)
        return parser

    def take_action(self, parsed_args):
        blended_dir = get_blended_directory_path()
        package_name = parsed_args.package_name
        package_id = parsed_args.package_id
        if not package_name:
            package_name = input("Please Enter Fully Qualified Package Name: ")
        if package_name:
            identifiers = package_name.split("/")
            if len(identifiers) != 2:
                print("Error: Please enter the fully qualified name of the package \"account_name/package_name\".")
                sys.exit(0)
            package_name = package_name_validation(package_name)
            account_name = identifiers[0]
            package_name = identifiers[1]
        network, user_slug = manage_session_key(parsed_args.login, parsed_args.password, Network())
        current_account = get_current_account(network, user_slug)
        last_active = get_logged_in_account()
        current_dir = os.path.join(blended_dir, current_account)
        package = PackageInfo(package_name=package_name,
                              package_id=package_id,
                              new_name=None,
                              )
        account = AccountInfo(blended_dir=blended_dir,
                              current_dir=current_dir,
                              current_account=current_account,
                              last_active=last_active,
                              user_slug=user_slug,
                              account_name=account_name,
                              )
        route_obj = Route(account, package)
        if current_account == 'anonymous':
            print("You are not logged in. Please log in or create an account.")
            sys.exit(0)
        response = accept(route_obj, account, package)
        if response:
            response = response.to_dict()
            response = response['data']
            title = response["title"]
            slug = response["slug"]
            account_name = response["transferred_by"]
            print('Congratulations! You have successfully accepted transfer of'
                  ' "%s" (%s). It has been added to your My Designs.' %
                  (title, package_name))


def accept(route_obj, account, package):
    spinner = Spinner()
    spinner.start()
    try:
        response = route_obj.package_accept(account, package)
        spinner.stop()
    except BlendedException as exc:
        spinner.stop()
        try:
            if exc.args[0]['status_code'] in (4035, 4036):
                print(exc.args[0]['errors'])
                sys.exit(0)
            elif exc.args[0]['status_code'] == 5102:
                if package.new_name:
                    print('\nError: The package name is already in use. Please enter a different name.')
                else:
                    print('\nAlert: Package "%s" already exists in your My Designs. '
                          'Before this package transfer can be accepted, '
                          'you must first choose a new package name.' % (package.package_name))
                option = (input("Would you like to accept the transfer with a new package name? (Yes/No): ")).upper()
                if option in ['Y', 'YES']:
                    new_name = input("Please Enter New Package Name: ")
                    package.new_name = package_name_validation(new_name)
                    res = accept(route_obj, account, package)
                    return res
                else:
                    sys.exit(0)
            elif exc.args[0]['status_code'] == 5101:
                print("\nAlert: Package Purchase(s) Required: \n")
                table = BeautifulTable()
                table.column_headers = ['Title', 'Package Name', 'Author', 'Snapshot Label', 'price']
                data1 = exc.args[0]['error'][0]
                package = data1["dependency_of_package"]
                package_title = data1["title_dependency_of_package"]
                to_account = data1["to_account"]
                for item in exc.args[0]['error']:
                    data = item["dependency_package_details"]
                    title = data["title"]
                    price = data["license_price"]
                    label = data["label"]
                    identifiers = data["package"].split("/")
                    author = identifiers[0]
                    package_slug = identifiers[1]
                    table.append_row([title, package_slug, author, label, price])
                print('Package "%s" (%s) has the following 3rd party dependencies '
                      'that are required to be purchased before you can accept this '
                      'transfer from "%s".\n' % (package_title, package, to_account))
                print(table)
                print('\nPlease open this URL in your browser to Accept & Continue:')
                print('\nURL: "%s"' % exc.args[0]['redirect_url'])
                sys.exit(0)
            elif exc.args[0]['status_code']:
                print(exc.args[0]['message'])
                sys.exit(0)
            else:
                raise exc
        except Exception:
            raise BlendedException(exc)

    return response


class PackageReject(Command):
    """
    """
    def get_parser(self, prog_name, **kwargs):
        parser = super(PackageReject, self).get_parser(prog_name)
        parser.add_argument('package_name', nargs='?', default=None, help="Needed package name")
        parser.add_argument('--login', nargs='?', default=None)
        parser.add_argument('--password', nargs='?', default=None)
        parser.add_argument('--package-id', nargs='?', default=None)
        parser.add_argument('--share', nargs='?', default=False, const=True)
        parser.add_argument('--transfer', nargs='?', default=False, const=True)
        return parser

    def take_action(self, parsed_args):
        blended_dir = get_blended_directory_path()
        package_name = parsed_args.package_name
        password = parsed_args.password
        username = parsed_args.login
        package_id = parsed_args.package_id
        share = parsed_args.share
        transfer = parsed_args.transfer
        if not package_name:
            network, user_slug = manage_session_key(parsed_args.login, parsed_args.password, Network())
            current_account = get_current_account(network, user_slug)
            last_active = get_logged_in_account()
            current_dir = os.path.join(blended_dir, current_account)
            try:
                relative_package_path = read_package_name_from_directory(current_account=current_account,
                                                                         current_dir=current_dir,
                                                                         blended_dir=blended_dir)
                package_name = relative_package_path[1].replace(os.sep, "/")
                package_name = package_name +'/'+ current_account
            except AssertionError:
                package_name = input("Please Enter Fully Qualified Package Name: ")

        if package_name:
            identifiers = package_name.split("/")
            if len(identifiers) != 2:
                print("Error: Please enter the fully qualified name of the package \"account_name/package_name\".")
                sys.exit(0)
            package_name = package_name_validation(package_name)
            account_name = identifiers[0]
            package_name = identifiers[1]
        else:
            package_name = package_name_validation(package_name)
        if not (share or transfer):
            revoke_type = input('Please enter reject type (Share/Transfer): ').strip().lower()
            while True:
                if not revoke_type:
                    print("Error: Reject type is required. It cannot be left blank. Please try again.")
                    sys.exit(0)
                if revoke_type == "share":
                    share = True
                    break
                elif revoke_type == "transfer":
                    transfer = True
                    break
                else:
                    print('Error: Please enter the reject type either "Share" or "Transfer".')
                    revoke_type = input('Please enter reject type (Share/Transfer): ').strip().lower()

        if parsed_args.package_name:
            network, user_slug = manage_session_key(parsed_args.login, parsed_args.password, Network())
            current_account = get_current_account(network, user_slug)
            last_active = get_logged_in_account()
            current_dir = os.path.join(blended_dir, current_account)
        if current_account == 'anonymous':
            print("You are not logged in. Please log in or create an account.")
            sys.exit(0)
        package = PackageInfo(package_name=package_name, package_id=package_id, share=share,
                              transfer=transfer)
        account = AccountInfo(blended_dir=blended_dir,
                              current_dir=current_dir,
                              current_account=current_account,
                              last_active=last_active,
                              user_slug=user_slug,
                              account_name=account_name,
                              )
        route_obj = Route(account, package)
        spinner = Spinner()
        spinner.start()
        try:
            response = route_obj.package_reject(account, package)
            spinner.stop()
        except BlendedException as exc:
            spinner.stop()
            try:
                if exc.args[0]['status_code'] in (4035, 4036):
                    print(exc.args[0]['errors'])
                    sys.exit(0)
                elif exc.args[0]['status_code'] == 5008:
                    print("Error: This package cannot be found in your library. You may need to push before performing this operation. Please check and try again.")
                    sys.exit(0)
                elif exc.args[0]['status_code']:
                    print(exc.args[0]['message'])
                    sys.exit(0)
                else:
                    raise BlendedException(exc)
            except Exception:
                raise BlendedException(exc)
        if share:
            print('Share reject:  You have successfully rejected the share of package "%s" from "%s".' %
                  (package_name, account_name))
        else:
            print('Transfer reject: You have successfully rejected the transfer of package "%s" from "%s".' %
                  (package_name, account_name))


class PackagePreview(Command):
    """
    """
    def get_parser(self, prog_name, **kwargs):
        parser = super(PackagePreview, self).get_parser(prog_name)
        parser.add_argument('package_name', nargs='?', default=None, help="Needed package name")
        parser.add_argument('--login', nargs='?', default=None)
        parser.add_argument('--password', nargs='?', default=None)
        parser.add_argument('--package-id', nargs='?', default=None)
        parser.add_argument('--host', nargs='?', default=None)
        parser.add_argument('--port', nargs='?', type=int, default=None)
        parser.add_argument('--label', nargs='?', default=None)
        parser.add_argument('--tweak', nargs='?', default=None)
        parser.add_argument('--no-cache', nargs='?', default=False, const=True)
        return parser

    def print_result(self, errors, warningOrError):

        def getCursor(position):
            return (position-1) * '-' + '^'
        indent = '  '
        for error in errors:
            location = error.get('location', {})
            if warningOrError == 'error':
                warningOrError = Fore.RED + warningOrError + Fore.RESET
            else:
                warningOrError = Fore.YELLOW + warningOrError + Fore.RESET

            print("'%s':%s:%s: %s %s: %s" % (location.get('templatePath', 'theme'), location.get('line', 0), location.get('column', 0), error.get('type', ''), warningOrError,  error.get('message', '')))
            print(location.get('lineTxt', ''))
            print(getCursor(location.get('column', 0)))

            if error.get('references', {}):
                print(2*indent + 'References:')
                for key in error.get('references', {}):
                    location = error['references'][key].get('location', {})
                    message = error['references'][key].get('message', '')
                    print(4*indent + "(%s): '%s':%s:%s: %s" % (key, location.get('templatePath', 'theme'), location.get('line', 0), location.get('column', 0), message))
                    print(4*indent + location.get('lineTxt', ''))
                    print(4*indent + getCursor(location.get('column', 0)))
            print()

    def take_action(self, parsed_args):
        setup_logger()
        blended_dir = get_blended_directory_path()
        try:
            tmp_dir = sys._MEIPASS
            is_exists = verify_theme_dir()
            if not is_exists :
                create_theme_dir()
                blended_dir = get_blended_directory_path()            
        except:
            pass

        package_name = parsed_args.package_name
        password = parsed_args.password
        username = parsed_args.login
        package_id = parsed_args.package_id
        no_cache = parsed_args.no_cache
        label = parsed_args.label
        host = parsed_args.host
        port = parsed_args.port
        tweak_json = parsed_args.tweak
        network = Network()
        network, user_pk = manage_session_key(username, password, network)
        current_account = get_current_account(network, user_pk)
        current_dir = os.path.join(blended_dir, current_account)
        relative_package_path = []
        account = None
        if not package_name:
            try:
                relative_package_path = read_package_name_from_directory(current_account=current_account,
                                                                         current_dir=current_dir,
                                                                         blended_dir=blended_dir,
                                                                         preview=True)
                lib_or_src, package_name = relative_package_path[0], relative_package_path[1].replace(os.sep, "/")
            except AssertionError:
                package_name = input("Please Enter Package Name: ")
        package_name = package_name_validation(package_name)

        get_host, get_port = get_ip_address()
        if not host:
            host = get_host()

        if not port:
            port = get_port()

        spinner = Spinner()
        spinner.start()
        backend = FileSystemBackend(
            current_dir, blended_dir=blended_dir,
            current_account=current_account, blended_directory_path=blended_dir)

        if not os.path.exists(CACHE_DIR):
            os.makedirs(CACHE_DIR)
        identifiers = package_name.split("/")
        controller = Controller(network, backend)
        preview_flag = True  # to check already present in local
        try:
            if not label:
                if (len(identifiers) > 1) and (current_account != identifiers[0]):
                    pass
                else:
                    backend.check_lib_or_src(package_name, lib_check=False)
                    preview_flag = False
            elif label:
                if len(identifiers) == 1:
                    identifiers[0] = current_account
                    identifiers.append(package_name)
        except (OSError, IOError) as os_exc:
            try:
                if not label and (package_name == identifiers[0] or current_account == identifiers[0]):
                    print("Downloading Package ...")
                    response = controller.pull_package(package_name, True,
                                                       draft=True, user_slug=current_account,
                                                       label=label, current_account=current_account)
                    preview_flag = False
                else:
                    preview_flag = True
            except BlendedException as exc:
                spinner.stop()
                try:
                    if exc.args[0].args[0]['status_code'] == 5008:
                        print(os_exc)
                        sys.exit(0)
                    elif exc.args[0].args[0]['status_code'] == 5002:
                        sessionNotAllowed()
                        sys.exit(0)
                    elif exc.args[0].args[0]['status_code']:
                        print(exc.args[0].args[0]['message'])
                        sys.exit(0)
                    else:
                        raise BlendedException(exc)
                except Exception:
                    raise BlendedException(exc)
            except ValueError:
                print("You are not logged in. Please log in or create an account.")
                sys.exit(0)

        if len(identifiers) > 1:
            account = identifiers[0]
            package_slug = identifiers[1]
        else:
            package_slug = identifiers[0]

        # if package preview if it has draft/version i need to keep a thin line.
        # package is present in user src and he pass fully qulified name then there must be trouble so i need to resolve this
        # if (len(identifiers) > 1 and preview_flag) OR (label and preview_flag): Need to add this
        if len(identifiers) > 1 and preview_flag:
            if not label:
                try:
                    response = controller.install_package(package_name,
                                                          user_slug=account, label="",
                                                          current_account=current_account)
                    label = backend.get_canonical(identifiers[0], identifiers[1], current_account=current_account)
                except (BlendedException, ValueError) as exc:
                    if not label:
                        spinner.stop()
                        if current_account == "anonymous":
                            raise BlendedException("Sessionkey is required. Please login!")

                        try:
                            if exc.args[0].args[0]['status_code'] in [5008, 5003]:
                                print(exc.args[0].args[0]['message'])
                                sys.exit(0)
                        except (BlendedException, AttributeError, KeyError):
                            pass
                        raise BlendedException("Package does not have canonical version.Please specify version.")

            if (not os.path.exists(os.path.join(backend.directory_path, 'lib', account, package_slug, label, '_package.json'))):
                try:
                    response = controller.install_package(package_name, user_slug=account,
                                                          label=label, current_account=current_account)
                except BlendedException as exc:
                    spinner.stop()
                    try:
                        if exc.args[0].args[0]['status_code'] == 5008:
                            print('First, try with a proper fully qualified name. If \"%s\" is still not found '
                                  'in the filesystem, please download or install it first.' % (package_name))
                            sys.exit(0)
                        elif exc.args[0].args[0]['status_code']:
                            print(exc.args[0].args[0]['message'])
                            sys.exit(0)
                        else:
                            raise BlendedException(exc)
                    except Exception:
                        raise BlendedException(exc)
        elif preview_flag:
            if len(identifiers) > 1:
                account = identifiers[0]
                package_slug = identifiers[1]
            else:
                try:
                    account = backend.get_current_account()
                except BlendedException as exc:
                    spinner.stop()
                    raise BlendedException(exc)
                package_slug = identifiers[0]

        if relative_package_path:
            lib_or_src, package_name = relative_package_path[0], relative_package_path[1].replace(os.sep, "/")
            path = "/%s" % (lib_or_src)
            if path.endswith('lib'):
                label = package_name.split("/")[-1]
        else:
            if not label:
                backend.check_lib_or_src(package_name)
            else:
                backend.check_lib_or_src(package_name, version=label, src_check=False)
            path = backend.directory_path.split(current_dir)[1].replace(os.sep, "/")
        
        preview_package_name = package_slug
        if path.endswith('lib'):
            dir_path = os.path.join(backend.directory_path, account, package_slug, label)
            try:
                backend.check_lib_or_src(package_name, version=label, src_check=False)
            except (OSError, IOError):
                try:
                    response = controller.install_package(package_name,
                                                          user_slug=account,
                                                          label=label,
                                                          current_account=current_account)
                except BlendedException as exc:
                    spinner.stop()
                    raise BlendedException(exc)
            package_slug = '%s/%s/%s' % (account, package_slug, label)
            # package_slug = '%s/%s' % (account, package_slug)
        spinner.stop()
        if label:
            package_intermediary = controller.backend.get_package('/'.join(identifiers), version=label)
        else:
            package_intermediary = controller.backend.get_package(package_name)
        
        same_name_file_folder = controller.intermediary_check_dublicate(package_intermediary)
        if same_name_file_folder:
            DuplicateFileFolderError(same_name_file_folder, preview_package_name)
            sys.exit(0)
        for item in package_intermediary.content:
            if item.name == '_package.json':
                try:
                    package_dict = json.loads(item.content)
                    # for Now It will preview only theme!
                    if "theme" != (package_dict['type']).lower():
                        print("Error: Preview is allowed only for theme type packages. You cannot see preview of layout type packages.")
                        sys.exit(0)
                except Exception:
                    pass
                
        
        errors_context_building = {
            "syntax_errors" : [],
            "null_undefined_pointer_error": []
        }

        output = controller.pre_validation_check(current_account,preview_package_name,errors_context_building)
        
        if 'error' in output:
            print(output['error']['message'])
            return
        
        error_flag = False
        for key in errors_context_building:
            # print("Result by validator '" + key + "':")
            result = errors_context_building[key]

            if len(result) > 0:
                error_flag = True
                print(Fore.RED + 'Validation failed' + Fore.RESET)
                print(Fore.RED + 'Errors:' + Fore.RESET)
                self.print_result(result, 'error')
        
        if not error_flag :              
            print('''\ncopy and open this URL 'http://%s:%s/' in Your browser\n''' %
                (host, port))
            url_init()
            home_url = 'http://%s:%s/' % (host, port)
            if not account:
                account = current_account
            blended_urls.urlList.append(home_url)
            theme_app.client_info = {"package": preview_package_name,
                                    "account": account,
                                    "version": label,
                                    "no_caching": no_cache}
            
            from werkzeug.serving import WSGIRequestHandler as customHandler
            customHandler.timeout = 5
            theme_app.run(host=host, port=port, debug=False, use_reloader=False, extra_files=extra_files,request_handler=customHandler)

class PackageAsJson(Command):
    """
    """
    def get_parser(self, prog_name, **kwargs):
        parser = super(PackageAsJson, self).get_parser(prog_name)
        parser.add_argument('package_name', nargs='?', default=None, help="Needed package name")
        parser.add_argument('--login', nargs='?', default=None)
        parser.add_argument('--password', nargs='?', default=None)
        parser.add_argument('--package-id', nargs='?', default=None)
        parser.add_argument('--jptf', nargs='?', default=False, const=True)
        return parser

    def take_action(self, parsed_args):
        # import pdb; pdb.set_trace()
        blended_dir = get_blended_directory_path()
        package_name = parsed_args.package_name
        package_id = parsed_args.package_id
        if not package_name:
            network, user_slug = manage_session_key(parsed_args.login, parsed_args.password, Network())
            current_account = get_current_account(network, user_slug)
            last_active = get_logged_in_account()
            current_dir = os.path.join(blended_dir, current_account)
            try:
                relative_package_path = read_package_name_from_directory(current_account=current_account,
                                                                         current_dir=current_dir,
                                                                         blended_dir=blended_dir)
                package_name = relative_package_path[1].replace(os.sep, "/")
            except AssertionError:
                package_name = input("Please Enter Package Name: ")
        package_name = package_name_validation(package_name)
        if parsed_args.package_name:
            network, user_slug = manage_session_key(parsed_args.login, parsed_args.password, Network())
            current_account = get_current_account(network, user_slug)
            last_active = get_logged_in_account()
            current_dir = os.path.join(blended_dir, current_account)
        package = PackageInfo(package_name=package_name,
                              package_id=package_id,
                              tweak_json=parsed_args.jptf,
                              )
        account = AccountInfo(blended_dir=blended_dir,
                              current_dir=current_dir,
                              current_account=current_account,
                              last_active=last_active,
                              user_slug=user_slug
                              )
        route_obj = Route(account, package)
        if (package_name) and (not package_id):
            try:
                response = route_obj.package_as_json(account, package)
            except BlendedException as exc:
                raise BlendedException(exc)
        elif package_id:
            print("TO-DO, Please try without package-id.")
            sys.exit(0)
        else:
            print("Error: Please enter valid package name and try again.")
            sys.exit(0)
        if response:
            try:
                print(json.dumps(response, indent=4, sort_keys=True))
            except:
                print(response)
        else:
            pass  # print ("some massage")


class PackageDetail(Command):
    """
    """
    def get_parser(self, prog_name, **kwargs):
        parser = super(PackageDetail, self).get_parser(prog_name)
        parser.add_argument('package_name', nargs='?', default=None, help="Needed package name")
        parser.add_argument('--login', nargs='?', default=None)
        parser.add_argument('--password', nargs='?', default=None)
        parser.add_argument('--package-id', nargs='?', default=None)
        parser.add_argument('--description', nargs='?', default=False, const=True)
        parser.add_argument('--licenses', nargs='?', default=False, const=True)
        return parser

    def take_action(self, parsed_args):
        blended_dir = get_blended_directory_path()
        package_name = parsed_args.package_name
        package_id = parsed_args.package_id
        is_description = parsed_args.description
        is_licenses = parsed_args.licenses
        if not package_name:
            network, user_slug = manage_session_key(parsed_args.login, parsed_args.password, Network())
            current_account = get_current_account(network, user_slug)
            last_active = get_logged_in_account()
            current_dir = os.path.join(blended_dir, current_account)
            try:
                relative_package_path = read_package_name_from_directory(current_account=current_account,
                                                                         current_dir=current_dir,
                                                                         blended_dir=blended_dir)
                package_name = relative_package_path[1].replace(os.sep, "/")
            except AssertionError:
                package_name = input("Please Enter Package Name: ")
        package_name = package_name_validation(package_name)
        if parsed_args.package_name:
            network, user_slug = manage_session_key(parsed_args.login, parsed_args.password, Network())
            current_account = get_current_account(network, user_slug)
            last_active = get_logged_in_account()
            current_dir = os.path.join(blended_dir, current_account)
        package = PackageInfo(package_name=package_name,
                              package_id=package_id,
                              is_description=is_description,
                              is_licenses=is_licenses,
                              )
        account = AccountInfo(blended_dir=blended_dir,
                              current_dir=current_dir,
                              current_account=current_account,
                              last_active=last_active,
                              user_slug=user_slug,
                              )
        route_obj = Route(account, package)
        if current_account == 'anonymous':
            print("You are not logged in. Please log in or create an account.")
            sys.exit(0)
        if (package_name) and (not package_id):
            try:
                response = route_obj.package_detail(account, package)
            except BlendedException as exc:
                try:
                    if exc.args[0].args[0]['status_code'] == 5008:
                        print("Before getting the detail of a package, please Push package \"%s\"." % (package_name))
                        sys.exit(0)
                    elif exc.args[0].args[0]['status_code'] == 5002:
                        sessionNotAllowed()
                        sys.exit(0)
                    elif exc.args[0].args[0]['status_code']:
                        print(exc.args[0].args[0]['message'])
                        sys.exit(0)
                    else:
                        raise BlendedException(exc)
                except Exception:
                    raise BlendedException(exc)
        elif package_id:
            print("TO-DO, Please try without package-id.")
            sys.exit(0)
        else:
            print("Error: Please enter valid package name and try again.")
            sys.exit(0)
        if response:
            try:
                package_description = response.description
                package_licenses = None
                if response.licenses:
                    package_licenses = response.licenses.get('items')
                licenses = {}
                if package_licenses:
                    for license in package_licenses:
                        licenses.update({license.get('name'): license.get('price')})
                else:
                    licenses = {}
                if not package_description:
                    package_description = ''
                if is_licenses and is_description:
                    print("licenses:\n")
                    show_licenses(licenses)
                    print("\ndescription:\n")
                    print(package_description)
                elif is_licenses and not is_description:
                    print("licenses:\n")
                    show_licenses(licenses)
                elif is_description and not is_licenses:
                    print("description:\n")
                    print(package_description)
                else:
                    print(response)
            except BlendedException as exc:
                print(response)


def show_licenses(licenses):
    """
    """
    for name, price in licenses.items():
        print("     %s  %s" % (name, price))


def share(route_obj, package, account):
    """
    """
    response = ""
    package_name = package.package_name
    package_id = package.package_id
    account_name = account.account_name
    current_account, current_dir = account.current_account, account.current_dir
    email = account.email
    if (package_name) and (not package_id):
        try:
            response = route_obj.package_share(account, package)
        except BlendedException as exc:
            try:
                if exc.args[0].args[0]['status_code'] == 5009:
                    if account_name:
                        print("You have already shared package \"%s\" to Account: \"%s\"." % (package_name, account_name))
                    elif email:
                        print("You have already shared package \"%s\" to Email: \"%s\"." % (package_name, email))
                    sys.exit(0)
                elif exc.args[0].args[0]['status_code'] == 1001:
                    permissionNotAllowed()
                    sys.exit(0)
                elif exc.args[0].args[0]['status_code'] == 5002:
                    sessionNotAllowed()
                    sys.exit(0)
                elif exc.args[0].args[0]['status_code'] == 5029:
                    print("\nWarning: No Snapshot in Package\n")
                    print("You cannot share a package until a snapshot has been created. "
                          "To do so, simply proceed with snapshot operation and take a snapshot of the package you wish to share.")
                    label = None
                    option = input("\nDo you want to create a snapshot? Yes/No: ")
                    if option in ['y', 'Y', 'YES', 'yes', 'Yes']:
                        label = input("\nPlease enter the snapshot version label of the package: ")
                    else:
                        sys.exit(0)
                    if not label:
                        print("Error: Label is required. It cannot be left blank. Please try again.")
                        sys.exit(0)
                    if label.lower() == 'draft':
                        print("Error: You are not allowed to use \"Draft\" as a version label for a snapshot.")
                        sys.exit(0)
                    elif label.lower() == 'canonical':
                        print("Error: You are not allowed to use \"Canonical\" as a version label for a snapshot.")
                        sys.exit(0)
                    if not re.match(r'^([0-9]*[a-z]*[A-Z]*[.]*[_]*)*$', label):
                        print("Error: You've entered an invalid label. "
                              "Accepted label values include alphanumeric, dot(.) and/or underscore(_).")
                        sys.exit(0)
                    package.label = label
                    snapshot(route_obj, package, account)
                    share(route_obj, package, account)
                    sys.exit(0)
                elif exc.args[0].args[0]['status_code'] == 5075:
                    print("\nError: You cannot share a package until your account \"%s\" has been verified. "
                          "To do so, simply verify your account and proceed to share." % (current_account))
                    option = input("\nDo you want to verify your account? Yes/No: ")
                    if option in ['y', 'Y', 'YES', 'yes', 'Yes']:
                        email = input("\nPlease Enter Your Email : ")
                        try:
                            response = route_obj.account_email_verification(email)
                        except BlendedException as exc:
                            print(exc)
                            sys.exit(0)
                        except AccountActivationException as exc:
                            print(exc)
                            sys.exit(0)
                        if response:
                            print(response)
                        print("\nA verification link has been sent to your email \"%s\". Please verify your account and proceed with the rest of the HUB operations." % (email))
                    sys.exit(0)
                elif exc.args[0].args[0]['status_code'] == 5076:
                    print('Previous request to share package is not accepted or rejected yet.')
                    sys.exit(0)
                elif exc.args[0].args[0]['status_code'] == 4035:
                    error = exc.args[0].args[0]['errors']
                    if 'account_slug' in error.keys():
                        print("Account name is required. It cannot be left blank. Please try again.")
                    elif 'email' in error.keys():
                        print("Enter a valid email address.")
                    else:
                        print(error)
                    sys.exit(0)
                elif exc.args[0].args[0]['status_code'] == 4050:
                    error = exc.args[0].args[0]['error']
                    title = error[0]['title_dependency_of_package']
                    package_name = error[0]['dependency_of_package']
                    table, auto_share_packages = beatifyError(error, "share", package_list=[])
                    if table:
                        print("\nError: Private 3rd Party Dependencies")
                        print("Package \"%s\" (%s) depends on 3rd party packages, that your share recipient, \"%s\", does not have access to.\n" % (title, package_name, account_name))
                        print(table)
                        print("\nAction(s) needed:")
                        print("You can either remove these dependencies from your package, or contact the 3rd party about publishing them or sharing them directly with the account \"%s\"." % (account_name))
                        sys.exit(0)
                    table, auto_share_packages = beatifyError(error, "purchase", package_list=[])
                    if table:
                        print("\nError: 3rd Party Published Dependencies")
                        print("Package \"%s\" (%s) has the following paid published dependencies that your share recipient, \"%s\", does not have access to.\n" % (title, package_name, account_name))
                        print(table)
                        print("\nAction(s) needed:")
                        print("You can either remove these dependencies from your package, or contact the user you're sharing with about purchasing these packages.")
                        sys.exit(0)

                    table, auto_share_packages, count = beatifyError(error, "private", package_list=[])
                    if table:
                        print("\nWarning: Private Dependencies")
                        print("Before package \"%s\" (%s) can be shared with \"%s\", you must share the following private dependencies:\n" % (title, package_name, account_name))
                        print(table)
                        print("\nAction(s) needed:")
                        print("You can proceed with the share.\n")
                        option = input("Do you want to Share & Continue? Press Yes/No: ")
                        if option in ['y', 'Y', 'YES', 'yes', 'Yes']:
                            response = route_obj.package_share(account, package, auto_share_packages=auto_share_packages)
                            print("You have shared %s private upstream dependencies packages and also shared package \"%s\" successfully with the account \"%s\"." % (count, package_name, account_name))
                            sys.exit(0)
                        else:
                            sys.exit(0)
                elif exc.args[0].args[0]['status_code'] == 5008 and not package.get:
                    print("Before sharing a package, please Push package \"%s\"." % (package_name))
                    sys.exit(0)
                elif exc.args[0].args[0]['status_code']:
                    print(exc.args[0].args[0]['message'])
                    sys.exit(0)
                else:
                    raise BlendedException(exc)
            except Exception:
                raise BlendedException(exc)
    elif package_id:
        print("TO-DO, Please try without package-id.")
        sys.exit(0)
    else:
        print("Error: Please enter valid package name and try again.")
        sys.exit(0)

    if package.get:
        title = ""
        try:
            title = route_obj.get_title(current_account, package_name)
        except BlendedException as e:
            print(e.args[0]['message'])
            sys.exit(0)
        shared_package_table(package_name, title, response)

    if response:
        if account_name:
            print("Package \"%s\" is shared with account \"%s\"." % (package_name, account_name))
        else:
            print("Package \"%s\" is shared with email \"%s\"." % (package_name, email))


def snapshot(route_obj, package, account):
    """
    """
    response = ""
    current_account, current_dir = account.current_account, account.current_dir
    package_name = package.package_name
    package_id = package.package_id
    spinner = Spinner()
    if (package_name) and (not package_id):
        try:
            spinner.start()
            response = route_obj.package_snapshot(account, package)
            spinner.stop()
        except BlendedException as exc:
            spinner.stop()
            try:
                status = exc.args[0].args[0]['status_code']
                if status == 4035:
                    error = exc.args[0].args[0]['errors']
                    if 'label' in error.keys():
                        print("Label is required. It cannot be left blank. Please try again.")
                    else:
                        print(error)
                    sys.exit(0)
                elif status == 1001:
                    permissionNotAllowed()
                    sys.exit(0)
                elif status == 5803:
                    title = ''
                    try:
                        title = route_obj.get_title(current_account, package_name)
                    except BlendedException as e:
                        pass
                    print("\nAlert: Missing Validators")
                    for item in exc.args[0].args[0]['validator_sets_to_pass']:
                        print('\nYour Package "%s" (%s) will need to earn badge "%s". To earn the "%s", the packagge will need to include '
                              'the following validators.\n' % (title, package_name, item['badge_name'], item['badge_name']))
                        print("The validator detail are printed in following manner:")
                        print('("Validator Name", "Account Name", "Package Name", "Snapshot Version")\n')
                        list_validator = item['list_of_validator_sets']
                        for idx, obj in enumerate(list_validator):
                            if not idx and len(list_validator)>1:
                                print("EITHER\n")
                            t_list = []
                            for obj1 in obj:
                                t = (obj1['name'], obj1['account'], obj1['slug'], obj1["label"])
                                t_list.append(t)
                            for i in range(len(t_list)//2+1):
                                print(*t_list[i*2:(i+1)*2], sep=' AND ')
                            if (idx+1)<len(list_validator):
                                print("\nOR\n")
                    sys.exit(0)
                elif status == 5002:
                    sessionNotAllowed()
                    sys.exit(0)
                elif status == 5008:
                    print("Before making the snapshot of a package, please Push package \"%s\"." % (package_name))
                    sys.exit(0)
                elif status == 5059:
                    title = ''
                    try:
                        title = route_obj.get_title(current_account, package_name)
                    except BlendedException as e:
                            pass
                    error_msg = ('\nWarning: Package is out-of-sync\n'
                                 'Your local copy of Package "%s" (%s) is out-of-sync with the Hub. '
                                 'Before creating a snapshot, you need to pull or push in order to '
                                 'sync up with the Hub.' % (title, package_name))
                    print(error_msg)
                    sys.exit(0)
                elif status == 5041:
                    print("Version label exists with package.")
                    sys.exit(0)
                elif status == 4050:
                    error = exc.args[0].args[0]['error']
                    title = error[0]['title_dependency_of_package']
                    package_name = error[0]['dependency_of_package']
                    table, user_table = beatifySnapshotError(error, "share")
                    private_count = purchase_count = 0
                    if table:
                        print("\nError: Private 3rd Party Dependencies")
                        print("Package \"%s\" (%s) now depends on 3rd party packages, that your following share recipients does not have access to:\n" % (title, package_name))
                        print(user_table)
                        print("\nAction(s) needed:")
                        print("To create this snapshot version, you can either remove these dependencies from your package, or contact the 3rd party about publishing them or sharing them directly with the above users.\n")
                        print(table)
                        sys.exit(0)
                    table, user_table, auto_share_packages, private_count = beatifySnapshotError(error, "private")
                    if auto_share_packages:
                        print("\nWarning: Private Dependencies")
                        print("Before this snapshot version of package \"%s\" (%s) can be created, you must share the private dependencies listed below with the following shared users:\n" % (title, package_name))
                        print(user_table)
                        print("\nIf you do not wish to share these packages, you can also choose to revoke the share of package \"%s\" (%s) with the above users, or you can remove the following private dependencies from your package in order to complete the operation:\n" % (title, package_name))
                        print(table)
                        print("\nAction(s) needed:")
                        print("You can proceed with the snapshot.\n")
                        option = input("Do you want to Snapshot & Share? Press Yes/No: ")
                        if option not in ['y', 'Y', 'YES', 'yes', 'Yes']:
                            sys.exit(0)
                    table, user_table, purchase_packages, purchase_count = beatifySnapshotError(error, "purchase")
                    while True:
                        if purchase_packages:
                            print("\nWarning: 3rd Party Published Dependencies")
                            print("Package \"%s\" (%s) now depends on paid published packages, that the following shared users may not have access to:\n" % (title, package_name))
                            print(user_table)
                            print('\nIf they have not already, these users will have to purchase these packages before they can use your new snapshot. If you choose "Create Snapshot", a seperate email notification will be sent to these users regarding the need to purchase these dependencies packages.\n')
                            print(table)
                            print("\nAction(s) needed:")
                            print("You can proceed with the snapshot.\n")
                            option = input("Do you want to Create Snapshot Anyway? Press Yes/No: ")
                            if option not in ['y', 'Y', 'YES', 'yes', 'Yes']:
                                if not auto_share_packages:
                                    sys.exit(0)
                                options = input("Canceling his transfer operation now will also cancel your previously approved actions.: Yes/No: ")
                                if options in ['y', 'Y', 'YES', 'yes', 'Yes']:
                                    sys.exit(0)
                            else:
                                break
                        else:
                            break
                    response = route_obj.package_snapshot(account, package,
                                                          auto_share_packages=auto_share_packages,
                                                          purchase_packages=purchase_packages)
                    if private_count and purchase_count:
                        pass
                    elif private_count:
                        print("You have created a new snapshot version \"%s\" and also shared \"%s\" private upstream dependencies packages successfully with the above listed users." % (response, private_count))
                        sys.exit(0)
                    elif purchase_count:
                        print("You have created a new snapshot version \"%s\" and also shared \"%s\" public dependencies packages successfully with the above listed users." % (response, purchase_count))
                        sys.exit(0)
                elif status == 4052:
                    error = (json.loads(exc.args[0].args[0]['items']))[0]['error_list']
                    table = BeautifulTable()
                    table.column_headers = ['Title', 'Package Name', 'Author', 'Snapshot Label']
                    title = error[0]['title_dependency_of_package']
                    package_name = error[0]['dependency_of_package']
                    dictpy = error
                    flag = False
                    for item in dictpy:
                        if item["third_party"]:
                            flag = True
                            author = item['package'].split("/")[0]
                            dep_package = item['package'].split("/")[1]
                            table.append_row([item['title'], dep_package, author, item['label']])
                    if flag:
                        print("\nWarning: Error(s) Found With Dependencies")
                        # print("Package \"%s\" (%s) now depends on the 3rd party packages that some users who have purchased this package may not have access to:\n" % (title, package_name))
                        print("Package \"%s\" (%s) now dependeds on the following published packages which are either not allowed to be bundled with any package or they were published with a license type which is not compatible with the license type of your package.\n" % (title, package_name))
                        print(table)
                        print("\nAction(s) needed:")
                        print('You can either cancel this snapshot, remove these dependencies from your package or turn off the "publish all snapshots" option in publish modal and publish it again')
                        sys.exit(0)
                    auto_share_packages = []
                    for item in dictpy:
                        if item['dependency_of_package'] and (not item["third_party"]):
                            auto_share_packages.append(item['package'])
                            author = item['package'].split("/")[0]
                            dep_package = item['package'].split("/")[1]
                            table.append_row([item['title'], dep_package, author, item['label']])
                    if auto_share_packages:
                        print("\nError: Private Dependencies")
                        print("Package \"%s\" (%s) now depends on the following private packages that some users who have purchased this package may not have access to:\n" % (title, package_name))
                        print(table)
                        print("\nAction(s) needed:")
                        print('You can either cancel this snapshot, remove these dependencies from your package, turn off the "Publish all snapshots" option in publish, or you can publish the above dependencies.')
                        sys.exit(0)
                elif status == 4051:
                    error = exc.args[0].args[0]['data']
                    table = BeautifulTable()
                    package_name = error[0]['dependency_of_package']['package']
                    title = error[0]['dependency_of_package']['title']
                    table.column_headers = ['Title', 'Package Name', 'Author', 'Snapshot Label']
                    dictpy = error
                    flag = False
                    purchase_packages = []
                    for item in dictpy:
                        purchase_packages.append(item['package'])
                        author = item['package'].split("/")[0]
                        dep_package = item['package'].split("/")[1]
                        table.append_row([item['title'], dep_package, author, item['label']])
                    if purchase_packages:
                        print("\nWarning: 3rd Party Published Dependencies")
                        print("Package \"%s\" (%s) now depends on the following public packages that some users who have purchased this package may not have access to:\n" % (title, package_name))
                        print(table)
                        print("\nAction(s) needed:")
                        print("You can either remove these dependencies from your package, change the price to FREE (If you are the owner of the dependency), or simply continue as is.\n")
                        # print("You can proceed with the snapshot.\n")
                        option = input("Do you want to Create Snapshot Anyway? Press Yes/No: ")
                        if option not in ['y', 'Y', 'YES', 'yes', 'Yes']:
                            sys.exit(0)
                    response = route_obj.package_snapshot(account, package, purchase_packages=purchase_packages)
                    print("\nYou have created a new snapshot version \"%s\" and also published it successfully.\n" % (response))
                    sys.exit(0)
                elif status:
                    print(exc.args[0].args[0]['message'])
                    sys.exit(0)
                else:
                    raise BlendedException(exc)
            except Exception:
                try:
                    if exc.args[0]:
                        if exc.args[0].get('status_code', None) == 5002:
                            sessionNotAllowed()
                            sys.exit(0)
                        print(exc.args[0])
                        sys.exit(0)
                except Exception:
                    raise BlendedException(exc)
        except OSError as exc:
            spinner.stop()
            print(exc)
            sys.exit(0)
    elif package_id:
        print("TO-DO, Please try without package-id.")
        sys.exit(0)
    else:
        print("Error: Please enter valid package name and try again.")
        sys.exit(0)
    if response:
        print("Snapshot of package \"%s\" has been created with version label \"%s\"." % (package_name, response))


def package_name_validation(package_name, action=None):
    """
    validate package name
    white spaces
    """
    account = None
    if package_name and package_name.strip():
        if (' ' in package_name.strip()):
            print("White space is not allowed in the package name. "
                  "Please enter a valid package name and try again.")
            sys.exit(0)
        package_name = package_name.strip()
    else:
        package_name = ''
    if not package_name:
        print("Error: Package Name is required. It cannot be left blank. Please try again.")
        sys.exit(0)

    identifiers = package_name.rsplit("/")
    if len(identifiers) > 2:
        print('Multiple slashes "/" are not allowed in package name. '
              'If you want to create package in current account then you have to specify '
              'fully qualified name of the package as "account_name/package_name".')
        sys.exit(0)

    if (len(identifiers) > 1) and action:
        print("Fully qualified \"%s\" (account_name/package_name) is not required here. Please provide only package name." % package_name)
        sys.exit(0)

    if len(identifiers) > 1:
        account = identifiers[0]
        package_slug = identifiers[1]
        if not (account and package_slug):
            print("Error: Package Name is required. It cannot be left blank. Please try again.")
            sys.exit(0)
    else:
        package_slug = identifiers[0]

    if not re.match(r'^([0-9]*[a-z]*[A-Z]*[-]*[_]*)*$', package_slug):
        print("Error: You've entered an invalid Package name. "
              "Accepted Package name include alphanumeric, underscore(_) and/or dash(-).")
        sys.exit(0)
    if len(package_slug) > 31:
        print("Error: Input characters should not be exceeded by 31 characters.")
        sys.exit(0)

    if package_slug[0].isdigit():
        print("Error: Package name should not start with a number.")
        sys.exit(0)

    if account and (not re.match(r'^([0-9]*[a-z]*[A-Z]*[-]*[_]*)*$', account)):
        print("Error: You've entered an invalid Package name. "
              "Accepted Package name include alphanumeric, underscore(_) and/or dash(-).")
        sys.exit(0)
    return package_name.lower()


def shared_package_table(package_name, title, response):
    data = response.to_dict()["items"]
    table = BeautifulTable()
    table.column_headers = ['Account/Email', 'Date Shared', 'Shared via email']
    count = 0
    for item in data:
        shared_account = item["shared_account"]
        if not shared_account:
            shared_account = item["email"]
        share_via_email = item["share_via_email"]
        date = item.get("created_date", "")
        if date:
            date = date.strftime("%b %d %Y %H:%M:%S")
        count = count+1
        table.append_row([shared_account, date, share_via_email])
    if not data:
        print('Your package "%s" (%s) has not yet been shared with anyone.' % (title, package_name))
    else:
        print('\nSharing grants other Blended accounts "Read Only" access to this package. You will still control who gets access.\n')
        print('You have shared "%s" (%s) with %s people.\n' % (title, package_name, count))
        print(table)
    sys.exit(0)


def beatifyError(error, error_type, package_list=[]):
    """
    """
    table = BeautifulTable()
    table.column_headers = ['Title', 'Package Name', 'Author', 'Snapshot Label']
    dictpy = error
    flag = False
    if error_type == "share":
        for item in dictpy:
            if item["third_party"] and not item['get_or_purchased']:
                flag = True
                author = item['package'].split("/")[0]
                package = item['package'].split("/")[1]
                title = item['dependency_package_details']['title']
                label = item['dependency_package_details']['label']
                table.append_row([title, package, author, label])
        return table, package_list

    if error_type == "purchase":
        for item in dictpy:
            if item['get_or_purchased']:
                package_list.append(item['package'])
                author = item['package'].split("/")[0]
                package = item['package'].split("/")[1]
                title = item['dependency_package_details']['title']
                label = item['dependency_package_details']['label']
                table.append_row([title, package, author, label])
        return table, package_list

    if error_type == "private":
        count = 0
        for item in dictpy:
            if item['dependency_of_package'] and (not item['get_or_purchased']) and (not item["third_party"]):
                count += 1
                package_list.append(item['package'])
                author = item['package'].split("/")[0]
                package = item['package'].split("/")[1]
                title = item['dependency_package_details']['title']
                label = item['dependency_package_details']['label']
                table.append_row([title, package, author, label])
        return table, package_list, count


def beatifySnapshotError(error, error_type):
    """
    """
    table = BeautifulTable()
    table.column_headers = ['Title', 'Package Name', 'Author', 'Snapshot Label']
    user_table = BeautifulTable()
    user_table.column_headers = ['User']
    dictpy = error
    package_list = []
    account_list = []
    auto_share_purchase_packages = []

    if error_type == "share":
        for item in dictpy:
            if item["third_party"] and not item['get_or_purchased']:
                if item['to_account'] not in account_list:
                    account_list.append(item['to_account'])
                    user_table.append_row([item['to_account']])
                if item['package'] in package_list:
                    continue
                package_list.append(item['package'])
                author = item['package'].split("/")[0]
                package = item['package'].split("/")[1]
                title = item['dependency_package_details']['title']
                label = item['dependency_package_details']['label']
                table.append_row([title, package, author, label])
        return table, user_table

    if error_type == "purchase":
        count = 0
        for item in dictpy:
            if item['get_or_purchased']:
                auto_share_purchase_packages.append(item['package'])
                if item['to_account'] not in account_list:
                    account_list.append(item['to_account'])
                    user_table.append_row([item['to_account']])
                if item['package'] in package_list:
                    continue
                count += 1
                package_list.append(item['package'])
                author = item['package'].split("/")[0]
                package = item['package'].split("/")[1]
                title = item['dependency_package_details']['title']
                label = item['dependency_package_details']['label']
                table.append_row([title, package, author, label])
        return table, user_table, auto_share_purchase_packages, count

    if error_type == "private":
        count = 0
        for item in dictpy:
            if item['dependency_of_package'] and (not item['get_or_purchased']) and (not item["third_party"]):
                auto_share_purchase_packages.append(item['package'])
                if item['to_account'] not in account_list:
                    account_list.append(item['to_account'])
                    user_table.append_row([item['to_account']])
                if item['package'] in package_list:
                    continue
                count += 1
                package_list.append(item['package'])
                author = item['package'].split("/")[0]
                package = item['package'].split("/")[1]
                title = item['dependency_package_details']['title']
                label = item['dependency_package_details']['label']
                table.append_row([title, package, author, label])
        return table, user_table, auto_share_purchase_packages, count
