from __future__ import absolute_import
from cliff.command import Command as CliffCommand

from blendedUx.blended_hostlib.backend import FileSystemBackend
from blendedUx.blended_hostlib.network import Network
from blendedUx.blended_hostlib.controller import Controller
from blendedUx.blended_hostlib.exceptions import BlendedException


# Help Descriptions
spaces = (' ' * 5)

HELP_BLENDED_FLAG = "blended"
HELP_ACCOUNT_FLAG = "account"
HELP_PACKAGE_FLAG = "package"

HELP_BASIC_SETUP_COMMAND = [
                        "%s setup" % (HELP_BLENDED_FLAG)
                    ]
HELP_BASIC_SETUP_COMMAND_DESCRIPTION = [
                        "Initialize the path of directory where themes in their respective account stored in local filesystem"
                    ]
HELP_BASIC_ACCOUNT_COMMAND = [
                        "%s %s create" % (HELP_BLENDED_FLAG, HELP_ACCOUNT_FLAG),
                        # "%s %s confirm" % (HELP_BLENDED_FLAG, HELP_ACCOUNT_FLAG),
                        "%s %s login" % (HELP_BLENDED_FLAG, HELP_ACCOUNT_FLAG),
                        "%s %s add" % (HELP_BLENDED_FLAG, HELP_ACCOUNT_FLAG),
                        "%s %s accept" % (HELP_BLENDED_FLAG, HELP_ACCOUNT_FLAG),
                        "%s %s revoke" % (HELP_BLENDED_FLAG, HELP_ACCOUNT_FLAG),
                        "%s %s set-current" % (HELP_BLENDED_FLAG, HELP_ACCOUNT_FLAG),
                        "%s %s set" % (HELP_BLENDED_FLAG, HELP_ACCOUNT_FLAG),
                        "%s %s current" % (HELP_BLENDED_FLAG, HELP_ACCOUNT_FLAG),
                        "%s %s list" % (HELP_BLENDED_FLAG, HELP_ACCOUNT_FLAG),
                        # "%s %s email-verification" % (HELP_BLENDED_FLAG, HELP_ACCOUNT_FLAG)
                    ]
HELP_BASIC_ACCOUNT_COMMAND_DESCRIPTION = [
                        "Create an Account in the Hub",
                        # "Activates the created Account in the Hub",
                        "Login in an Account in the Hub",
                        "Invites a existing or new user to join an account",
                        "Invited User accepts the invitation to become a member",
                        "removes the member from an account",
                        "Set the current account i.e. active account for the logged in user",
                        "Alias for the set-current command",
                        "Display User's active account",
                        "Display all accounts in which logged-in User is a member and all Users " \
                        "who are member in current account",
                        # "Sends the verification link in the respective email to verify the account."
                    ]
HELP_BASIC_PACKAGE_COMMAND = [
                        "%s %s create" % (HELP_BLENDED_FLAG, HELP_PACKAGE_FLAG),
                        "%s %s clone" % (HELP_BLENDED_FLAG, HELP_PACKAGE_FLAG),
                        "%s %s push" % (HELP_BLENDED_FLAG, HELP_PACKAGE_FLAG),
                        "%s %s pull" % (HELP_BLENDED_FLAG, HELP_PACKAGE_FLAG),
                        "%s %s install" % (HELP_BLENDED_FLAG, HELP_PACKAGE_FLAG),
                        "%s %s snapshot" % (HELP_BLENDED_FLAG, HELP_PACKAGE_FLAG),
                        "%s %s publish" % (HELP_BLENDED_FLAG, HELP_PACKAGE_FLAG),
                        "%s %s canonize" % (HELP_BLENDED_FLAG, HELP_PACKAGE_FLAG),
                        "%s %s preview" % (HELP_BLENDED_FLAG, HELP_PACKAGE_FLAG),
                        "%s %s share" % (HELP_BLENDED_FLAG, HELP_PACKAGE_FLAG),
                        "%s %s transfer" % (HELP_BLENDED_FLAG, HELP_PACKAGE_FLAG),
                        "%s %s get" % (HELP_BLENDED_FLAG, HELP_PACKAGE_FLAG),
                        "%s %s extend" % (HELP_BLENDED_FLAG, HELP_PACKAGE_FLAG),
                        "%s %s list" % (HELP_BLENDED_FLAG, HELP_PACKAGE_FLAG),
                        "%s %s as-json" % (HELP_BLENDED_FLAG, HELP_PACKAGE_FLAG),
                        "%s %s compare" % (HELP_BLENDED_FLAG, HELP_PACKAGE_FLAG),
                        "%s %s detail" % (HELP_BLENDED_FLAG, HELP_PACKAGE_FLAG),
                        "%s %s update" % (HELP_BLENDED_FLAG, HELP_PACKAGE_FLAG),
                        "%s %s up" % (HELP_BLENDED_FLAG, HELP_PACKAGE_FLAG),
                        "%s %s version" % (HELP_BLENDED_FLAG, HELP_PACKAGE_FLAG)
                    ]
HELP_BASIC_PACKAGE_COMMAND_DESCRIPTION = [
                        "Create a Package in the Hub in the respective current account of logged in User",
                        "Clones an Package from the existing Hub account to logged in user's account",
                        "Save Package documents from local filesystem to the Hub",
                        "Downloads the Package documents from the Hub to the local filesystem",
                        "Downloads the Package documents in 'lib' directory of the respective account in filesystem",
                        "Creates a version for the Package",
                        "Make Package snapshot version publicly available",
                        "Create a canonical version of published Package",
                        "Runs a Preview server to view the created theme in the browser",
                        "Shares a Package with the specified account",
                        "Transfers a Package to the specified account",
                        "Get Acquisition of a published Package with free license",
                        "Extends a specified Package locally in filesystem",
                        "Displays list of Packages available in the current account or account specified",
                        "It prints the context version of the package in JSON format",
                        "Compare local filesystem package to the Hub",
                        "Displays the details of the package",
                        "Updates package with another package",
                        "Alias for the update command",
                        "Displays list of all snapshot version of a package"
                    ]
HELP_BASIC_COMMAND = HELP_BASIC_SETUP_COMMAND[:1] + HELP_BASIC_ACCOUNT_COMMAND[:3] + HELP_BASIC_PACKAGE_COMMAND[:4]
HELP_BASIC_COMMAND_DESCRIPTION = HELP_BASIC_SETUP_COMMAND_DESCRIPTION[:1] +\
                                 HELP_BASIC_ACCOUNT_COMMAND_DESCRIPTION[:3] +\
                                 HELP_BASIC_PACKAGE_COMMAND_DESCRIPTION[:4]


HELP_MORE_COMMAND = HELP_BASIC_SETUP_COMMAND + HELP_BASIC_ACCOUNT_COMMAND + HELP_BASIC_PACKAGE_COMMAND
HELP_MORE_COMMAND_DESCRIPTION = HELP_BASIC_SETUP_COMMAND_DESCRIPTION +\
                                HELP_BASIC_ACCOUNT_COMMAND_DESCRIPTION +\
                                HELP_BASIC_PACKAGE_COMMAND_DESCRIPTION


class Command(object):
    def __init__(self):
        """
        """
        self.spaces = spaces
        self.blended_command = ''
        self.required_arguments = []
        self.optional_arguments = []
        self.description = ''

    def print_help(self):
        """
        :return:
        """
        required_arguments = self.check_args(self.required_arguments)
        optional_arguments = self.check_args(self.optional_arguments)

        print('\nCommand:\n')
        print('%s%s' % (self.spaces, self.blended_command))
        print('\nRequired Arguments:\n')

        for required_args in required_arguments:
            self.print_help_details(required_args)
        print('\nOptional arguments:\n')
        for optional_args in optional_arguments:
            self.print_help_details(optional_args)
        print('\nDescription:\n')
        print('%s%s' % (self.spaces, self.description))

    def print_help_details(self, command_detail_dict):
        for key, value in command_detail_dict.items():
            print('{2:>5}{0:{width}1}{1}'.format(key, value, '', width=2))

    def check_args(self, args_list):
        if not args_list:
            args_list = [{"NIL": "NIL"}]
        return args_list


class Flags(object):
    def __init__(self):
        self.login = {"--login": "Uniquely identifying username should pass with this flag"}
        self.password = {"--password": "Password should pass with this flag"}
        self.account = "account"
        self.package = "package"
        self.package_id = {"--package-id": "Unique id of the package should pass with this flag"}
        self.label = {"--label": "Version of the package should pass with this flag"}
        self.draft = {"--draft": "Boolean flag, no value will pass with this flag"}
        self.email = {"--email": "Email address should pass with this flag"}
        self.account_flag = {"--account": "Specific account slug should pass with this flag"}
        self.license = {"--license": "License name should pass with this flag"}
        self.blended = 'blended'
        self.new_name = {"--new-name": "New package Slug for the package should pass with this flag"}
        self.description = {"--description": "Description of package"}

    def account_slug(self):
        return '<account_slug>'

    def package_slug(self):
        return '<package_slug>'

    def fully_qualified_name(self):
        return '<account/package>'

    def user_slug(self):
        return '<username>'

    def token(self):
        return '<token>'


class AccountCreate(Command):
    """
    """
    def __init__(self):
        super(AccountCreate, self).__init__()
        flags = Flags()
        user_slug = flags.user_slug()
        password = flags.password
        email = flags.email

        self.blended_command = "%s %s create %s --name %s %s --no-login" % (flags.blended, flags.account,
                                                                            user_slug,
                                                                            list(password.keys())[0],
                                                                            list(email.keys())[0])
        self.required_arguments = [{user_slug: "Username is uniquely identifying name of an account"}]
        self.optional_arguments = [password, email,
                                   {"--name": "Name of Account user"},
                                   {"--no-login": "Boolean flag, no value will pass in this flag"}
                                   ]
        self.description = "This command is use to create an account for user on the hub. By creating" \
                           " an account one can create and save their theme on hub"


class AccountConfirm(Command):
    def __init__(self):
        super(AccountConfirm, self).__init__()
        flags = Flags()
        login = flags.login
        password = flags.password
        token = flags.token()
        self.blended_command = "%s %s confirm %s %s %s --no-login" % (flags.blended, flags.account,
                                                                      token, list(login.keys())[0],
                                                                      list(password.keys())[0])
        self.required_arguments = [{token: "Account Activation Token received on email should pass here"}]
        self.optional_arguments = [login, password,
                                   {"--no-login": "boolean flag, no value will pass in this flag"}
                                   ]
        self.description = "This command verifies a user, confirmation command is used to activate "\
                           "the user account created. Nobody can use account until it is activated."


class AccountLogin(Command):
    def __init__(self):
        super(AccountLogin, self).__init__()
        flags = Flags()
        login = flags.login
        password = flags.password
        user_slug = flags.user_slug()
        self.blended_command = "%s %s login %s %s %s" % (flags.blended, flags.account,
                                                         user_slug, list(login.keys())[0],
                                                         list(password.keys())[0])
        self.required_arguments = []
        self.optional_arguments = [{user_slug: "Username should pass here"}, login, password]
        self.description = "This command is use to login in the user account"


class AccountAdd(Command):
    def __init__(self):
        super(AccountAdd, self).__init__()
        flags = Flags()
        login = flags.login
        password = flags.password
        email = list(flags.email.keys())[0]
        account = flags.account_flag
        account_slug = flags.account_slug()
        self.blended_command = "%s %s add %s %s %s %s %s [--admin | --read | --write]" % (
                                                        flags.blended, flags.account,
                                                        account_slug, list(login.keys())[0],
                                                        list(password.keys())[0],
                                                        email, list(account.keys())[0]
                                                        )
        self.required_arguments = [{account_slug: "Account slug of account that needs to be invited should pass here"}]
        self.optional_arguments = [login, password,
                                   {email: "email address of an account needs to be invited should pass with this flag"},
                                   account,
                                   {"--admin": "Boolean flag, no value will pass with the flag. "
                                               "Invites user with admin permissions in an account"},
                                   {"--read": "Boolean flag, no value will pass with the flag. "
                                              "Invites user with read only permissions in an account"},
                                   {"--write": "Boolean flag, no value will pass with the flag. "
                                               "Invites user with write permissions in an account"}
                                   ]
        self.description = "This command invites an account to join logged in user's account. "\
                           "Permissions [admin, read, write] are mutually exclusive. At a time,"\
                           " only one should be mentioned."


class AccountAccept(Command):
    def __init__(self):
        super(AccountAccept, self).__init__()
        flags = Flags()
        login = flags.login
        password = flags.password
        token = flags.token()
        self.blended_command = "%s %s accept %s %s %s" % (flags.blended, flags.account,
                                                          token, list(login.keys())[0],
                                                          list(password.keys())[0]
                                                          )
        self.required_arguments = [
                                    {token: "Token received on email when an user"
                                            " get invited from other account should pass here"
                                     }]
        self.optional_arguments = [login, password]
        self.description = "This command is to accepts the invitation from an account to join that account"\
                           " and becomes a collaborator in that account."


class AccountSetCurrent(Command):
    def __init__(self):
        super(AccountSetCurrent, self).__init__()
        self.flags = Flags()
        self.login = self.flags.login
        self.password = self.flags.password
        self.account_slug = self.flags.account_slug()
        self.blended_command = "%s %s set-current %s %s %s" % (self.flags.blended, self.flags.account,
                                                               self.account_slug, list(self.login.keys())[0],
                                                               list(self.password.keys())[0]
                                                               )
        self.required_arguments = [
            {self.account_slug: "Account slug of account needs to be set as current account should pass here"
             }]
        self.optional_arguments = [self.login, self.password]
        self.description = "This command set the active account."


class AccountSet(AccountSetCurrent):
    def __init__(self):
        super(AccountSet, self).__init__()
        self.blended_command = "%s %s set %s %s %s" % (self.flags.blended, self.flags.account,
                                                       self.account_slug, list(self.login.keys())[0],
                                                       list(self.password.keys())[0]
                                                       )
        self.description = "This command is an Alias of set-current command."\
                           " This works same as set-current, to set an active account"


class AccountList(Command):
    def __init__(self):
        super(AccountList, self).__init__()
        flags = Flags()
        login = flags.login
        password = flags.password
        account_slug = flags.account_slug()
        self.blended_command = "%s %s list %s %s %s" % (flags.blended, flags.account,
                                                        account_slug, list(login.keys())[0],
                                                        list(password.keys())[0]
                                                        )
        self.required_arguments = [
            ]
        self.optional_arguments = [
            {account_slug: "Account slug for a specific account should pass here"
             }, login, password]
        self.description = "This command is use to display list of collaborators on current or specified account"\
                           " and list of accounts on logged in user."


class AccountRevoke(Command):
    def __init__(self):
        super(AccountRevoke, self).__init__()
        self.blended_command = "Needs to be implement"


class AccountCurrent(Command):
    def __init__(self):
        super(AccountCurrent, self).__init__()
        flags = Flags()
        login = flags.login
        password = flags.password
        self.blended_command = "%s %s current %s %s" % (flags.blended, flags.account,
                                                        list(login.keys())[0],
                                                        list(password.keys())[0]
                                                        )
        self.required_arguments = []
        self.optional_arguments = [login, password]
        self.description = "This command is use to display the current active account of the logged in user."


class AccountEmailVerification(Command):
    """
    """
    def __init__(self):
        super(AccountEmailVerification, self).__init__()
        flags = Flags()
        login = flags.login
        password = flags.password
        self.blended_command = "%s %s email-verification <email address>" % (flags.blended, flags.account)
        self.required_arguments = [{"<email address>": "Valid email address of user."}]
        self.optional_arguments = [login, password]
        self.description = "This command is used to resend verification link to your email for the account ."


class PackageCreate(Command):
    def __init__(self):
        super(PackageCreate, self).__init__()
        flags = Flags()
        login = flags.login
        password = flags.password
        package_slug = flags.package_slug()
        self.blended_command = "%s %s create %s --type --description %s %s" % (flags.blended, flags.package,
                                                                               package_slug, list(login.keys())[0],
                                                                               list(password.keys())[0])
        self.required_arguments = [{package_slug: "Package slug should pass here"}]
        self.optional_arguments = [login, password,
                                   {"--type": "Number from list of Package Type"
                                              " of the package should pass with this flag"},
                                   {"--description": "Description of the package should pass with this flag"}]
        self.description = "This command creates a new package in the hub in logged in user's current active account."


class PackageClone(Command):
    def __init__(self):
        super(PackageClone, self).__init__()
        flags = Flags()
        login = flags.login
        password = flags.password
        label = flags.label
        new_name = flags.new_name
        draft = flags.draft
        package_slug = flags.fully_qualified_name()
        self.blended_command = "%s %s clone %s --type --description"\
                               " %s %s %s %s %s --no-download" % (flags.blended, flags.package,
                                                                  package_slug,
                                                                  list(login.keys())[0],
                                                                  list(password.keys())[0],
                                                                  list(label.keys())[0],
                                                                  list(draft.keys())[0],
                                                                  list(new_name.keys())[0])
        self.required_arguments = [{package_slug: "account/package_slug is fully qualified name of package,"
                                                  " that needs to be pass here"}]
        self.optional_arguments = [login, password,
                                   {"--type": "Type of the package should pass with this flag"},
                                   {"--description": "Description of the package should pass with this flag"},
                                   label, draft, new_name,
                                   {"--no-download": "Boolean flag, specify if don't want to download"
                                                     " package in local filesystem, no value will pass with this flag"}]
        self.description = "This command clone a package from hub into user's logged in account and  download's it in "\
                           "local file system if --no-download flag is not used"


class PackagePush(Command):
    def __init__(self):
        super(PackagePush, self).__init__()
        flags = Flags()
        login = flags.login
        password = flags.password
        package_slug = flags.fully_qualified_name()
        self.blended_command = "%s %s push %s %s %s --force" % (flags.blended, flags.package,
                                                                package_slug,
                                                                list(login.keys())[0],
                                                                list(password.keys())[0],
                                                                )
        self.required_arguments = [{package_slug: "account/package_slug is fully qualified name of package,"
                                                  " that needs to be pass here"}]
        self.optional_arguments = [login, password,
                                   {"--force": "This is a boolean flag, should be used when need to"
                                               " push package without an comparision of files"},
                                   {"--files": "This is a boolean flag, should be used when need to"
                                               " push specific files. Need to pass the file path after this flag"},
                                   ]
        self.description = "This command is use to upload package's files in package draft on Hub."


class PackagePull(Command):
    def __init__(self):
        super(PackagePull, self).__init__()
        flags = Flags()
        login = flags.login
        password = flags.password
        draft = flags.draft
        # label = flags.label
        package_slug = flags.fully_qualified_name()
        self.blended_command = "%s %s push %s %s %s --force %s" % (flags.blended, flags.package,
                                                                   package_slug,
                                                                   list(login.keys())[0],
                                                                   list(password.keys())[0],
                                                                   list(draft.keys())[0]
                                                                   )
        self.required_arguments = [{package_slug: "account/package_slug is fully qualified name of package,"
                                                  " that needs to be pass here"}]
        self.optional_arguments = [login, password,
                                   {"--force": "This is a boolean flag, should be used when need to"
                                               " pull package without an comparision of files"},
                                   {"--files": "This is a boolean flag, should be used when need to"
                                               " pull specific files. Need to pass the file path after this flag"},
                                   # draft,
                                   ]
        self.description = "This command is use to download package into filesystem from Hub. One "\
                           "can download draft version by specifying --draft in command."


class PackageInstall(Command):
    def __init__(self):
        super(PackageInstall, self).__init__()
        flags = Flags()
        login = flags.login
        password = flags.password
        draft = flags.draft
        label = flags.label
        package_slug = flags.fully_qualified_name()
        self.blended_command = "%s %s install %s %s %s %s" % (flags.blended, flags.package,
                                                              package_slug,
                                                              list(login.keys())[0],
                                                              list(password.keys())[0],
                                                              list(label.keys())[0]
                                                              )
        self.required_arguments = [{package_slug: "account/package_slug is fully qualified name of package,"
                                                  " that needs to be pass here"}]
        self.optional_arguments = [login, password, label]
        self.description = "This command is use to download a package and all it's dependencies in filesystem, "\
                           "all package which are downloaded by install command will goes into 'lib' directory "\
                           "in current account directory of logged-in user's in filesytem."


class PackageExtend(Command):
    def __init__(self):
        super(PackageExtend, self).__init__()
        flags = Flags()
        login = flags.login
        password = flags.password
        draft = flags.draft
        new_name = flags.new_name
        label = flags.label
        package_slug = flags.fully_qualified_name()
        self.blended_command = "%s %s extend %s %s %s %s %s %s --description" % (flags.blended, flags.package,
                                                                                 package_slug,
                                                                                 list(login.keys())[0],
                                                                                 list(password.keys())[0],
                                                                                 list(draft.keys())[0],
                                                                                 list(label.keys())[0],
                                                                                 list(new_name.keys())[0]
                                                                                 )
        self.required_arguments = [{package_slug: "account/package_slug is fully qualified name of package,"
                                                  " that needs to be pass here"}]
        self.optional_arguments = [login, password, label, draft, new_name,
                                   {"--description": "Description for the package should pass with ths flag"}]
        self.description = "This command is use to extend a package local in filesystem. "\
                           "No package will create on hub with this command. By extending a package, a new package " \
                           "will created in filesystem, which will referencing to the package it is extended from"\
                           " i.e. its parent package. referencing to parent package is done in _index.json file "\
                           "created in extended package."


class PackageSnapshot(Command):
    def __init__(self):
        super(PackageSnapshot, self).__init__()
        self.flags = Flags()
        self.login = self.flags.login
        self.password = self.flags.password
        self.label = self.flags.label
        self.package_slug = self.flags.package_slug()
        self.blended_command = "%s %s snapshot %s %s %s %s" % (self.flags.blended, self.flags.package,
                                                               self.package_slug,
                                                               list(self.login.keys())[0],
                                                               list(self.password.keys())[0],
                                                               list(self.label.keys())[0],
                                                               )
        self.required_arguments = [{self.package_slug: "slug of package,"
                                                       " that needs to be pass here"}]
        self.optional_arguments = [self.login, self.password, self.label]
        self.description = "This command is use to create a snapshot of a package with the given version label."


class PackagePublish(Command):
    def __init__(self):
        super(PackagePublish, self).__init__()
        flags = Flags()
        login = flags.login
        password = flags.password
        label = flags.label
        license_flag = flags.license
        package_slug = flags.package_slug()
        self.blended_command = "%s %s publish %s %s %s %s %s --prcie" % (flags.blended, flags.package,
                                                                         package_slug,
                                                                         list(login.keys())[0],
                                                                         list(password.keys())[0],
                                                                         list(label.keys())[0],
                                                                         list(license_flag.keys())[0],
                                                                         )
        self.required_arguments = [{package_slug: "slug of package,"
                                                  " that needs to be pass here"}]
        self.optional_arguments = [login, password, label, license_flag,
                                   {"--price": "Price of License given to the package should pass with this flag"}]
        self.description = "This command will make the snapshot version of the package publicly available to"\
                           " get or buy."


class PackageCanonize(PackageSnapshot):
    def __init__(self):
        super(PackageCanonize, self).__init__()
        self.blended_command = "%s %s canonize %s %s %s %s" % (self.flags.blended, self.flags.package,
                                                               self.package_slug,
                                                               list(self.login.keys())[0],
                                                               list(self.password.keys())[0],
                                                               list(self.label.keys())[0],
                                                               )
        self.description = "This command creates a canonical version of a published package."


class PackageShare(Command):
    def __init__(self):
        super(PackageShare, self).__init__()
        self.flags = Flags()
        self.login = self.flags.login
        self.password = self.flags.password
        self.package_slug = self.flags.package_slug()
        self.blended_command = "%s %s share %s %s %s --with" % (self.flags.blended, self.flags.package,
                                                                self.package_slug,
                                                                list(self.login.keys())[0],
                                                                list(self.password.keys())[0]
                                                                )
        self.required_arguments = [{self.package_slug: "Package Slug needs to pass here"}]
        self.optional_arguments = [self.login, self.password,
                                   {"--with": "Account slug of an account the package needs to be share "
                                              "should pass with this flag"}]
        self.description = "This command Shares a package with the specified account."


class PackageTransfer(PackageShare):
    def __init__(self):
        super(PackageTransfer, self).__init__()
        self.blended_command = "%s %s transfer %s %s %s --to" % (self.flags.blended, self.flags.package,
                                                                 self.package_slug,
                                                                 list(self.login.keys())[0],
                                                                 list(self.password.keys())[0]
                                                                 )
        self.optional_arguments = [self.login, self.password,
                                   {"--to": "Account slug of an account the package needs to be transfer "
                                            "should pass with this flag"}]
        self.description = "This command Transfers a package to specified account."


class PackagePreview(Command):
    def __init__(self):
        super(PackagePreview, self).__init__()
        flags = Flags()
        login = flags.login
        password = flags.password
        package_slug = flags.fully_qualified_name()
        self.blended_command = "%s %s preview %s %s %s --host --port" % (flags.blended, flags.package,
                                                                         package_slug,
                                                                         list(login.keys())[0],
                                                                         list(password.keys())[0]
                                                                         )
        self.required_arguments = [{package_slug: "slug or fully qualified name of package should pass here"}]
        self.optional_arguments = [login, password,
                                   {"--host": "ip address of the machine or localhost should pass with this flag"},
                                   {"--port": "port number on which preview server needs to run, should pass"
                                              " with this flag"}]
        self.description = "This command is use to run a preview server by which we can able to preview " \
                           "theme in browser."


class PackageRevoke(Command):
    def __init__(self):
        super(PackageRevoke, self).__init__()
        self.blended_command = "Needs to be implement"


class PackageRetract(Command):
    def __init__(self):
        super(PackageRetract, self).__init__()
        self.blended_command = "Needs to be implement"


class PackageValidate(Command):
    def __init__(self):
        super(PackageValidate, self).__init__()
        self.blended_command = "Needs to be implement"


class PackageGet(Command):
    """
    """
    def __init__(self):
        super(PackageGet, self).__init__()
        flags = Flags()
        login = flags.login
        password = flags.password
        new_name = flags.new_name
        license_flag = flags.license
        package_slug = flags.fully_qualified_name()
        self.blended_command = "%s %s get %s %s %s %s %s" % (flags.blended, flags.package,
                                                             package_slug,
                                                             list(login.keys())[0],
                                                             list(password.keys())[0],
                                                             list(license_flag.keys())[0],
                                                             list(new_name.keys())[0]
                                                             )
        self.required_arguments = [{package_slug: "fully qualified name of package should pass here"}]
        self.optional_arguments = [login, password, license_flag, new_name]
        self.description = "This command is use to get acquisition of a package which is publish with a free license."


class PackageList(Command):
    def __init__(self):
        super(PackageList, self).__init__()
        flags = Flags()
        login = flags.login
        password = flags.password
        package_slug = flags.package_slug()
        account = flags.account_flag
        self.blended_command = "%s %s list %s %s %s %s" % (flags.blended, flags.package,
                                                           package_slug,
                                                           list(login.keys())[0],
                                                           list(password.keys())[0],
                                                           list(account.keys())[0]
                                                           )
        self.required_arguments = []
        self.optional_arguments = [{package_slug: "Package slug of package should pass here"},
                                   login, password, account]
        self.description = "This command is use to display list of packages on current or specified account and " \
                           "to display list of account who has acquisition of the specified package name"


class PackageDetail(Command):
    def __init__(self):
        super(PackageDetail, self).__init__()
        flags = Flags()
        login = flags.login
        password = flags.password
        license_flag = flags.license
        description = flags.description
        package_slug = flags.fully_qualified_name()
        self.blended_command = "%s %s detail %s %s %s %s %s" % (flags.blended, flags.package,
                                                                package_slug,
                                                                list(login.keys())[0],
                                                                list(password.keys())[0],
                                                                list(license_flag.keys())[0],
                                                                list(description.keys())[0]
                                                                )
        self.required_arguments = [{package_slug: "fully qualified name of package should pass here"}]
        self.optional_arguments = [login, password, license_flag, description]
        self.description = "This command is use to display details of a package."


class PackageVersion(Command):
    def __init__(self):
        super(PackageVersion, self).__init__()
        flags = Flags()
        login = flags.login
        password = flags.password
        package_slug = flags.fully_qualified_name()
        self.blended_command = "%s %s detail %s %s %s --canonical " % (flags.blended, flags.package,
                                                                       package_slug,
                                                                       list(login.keys())[0],
                                                                       list(password.keys())[0],
                                                                       )
        self.required_arguments = [{package_slug: "fully qualified name of package should pass here"}]
        self.optional_arguments = [login, password, {"--canonical": "boolean flag, no value will pass in this flag"}]
        self.description = "This command is use to display version list details of a package."


class PackageUpdate(Command):
    def __init__(self):
        super(PackageUpdate, self).__init__()
        flags = Flags()
        login = flags.login
        password = flags.password
        label = flags.label
        package_slug = flags.fully_qualified_name()
        self.blended_command = "%s %s update %s <source_package_name> --from "\
                               " %s %s %s " % (flags.blended, flags.package,
                                               package_slug,
                                               list(login.keys())[0],
                                               list(password.keys())[0],
                                               list(label.keys())[0],
                                               )
        self.required_arguments = [{package_slug: "account/package_slug is fully qualified name of package,"
                                                  " that needs to be pass here"}]
        self.optional_arguments = [login, password,
                                   {"--from": "Need to pass source package after it."},
                                   label,
                                   {"<package_name>": "Source package name: Either pass it name with \"--from\" flag or"
                                                      " pass it after \"package name\" without \"--from\" flag."}]
        self.description = "This command updates a package with another package."


class PackageUp(Command):
    def __init__(self):
        super(PackageUp, self).__init__()
        flags = Flags()
        login = flags.login
        password = flags.password
        label = flags.label
        package_slug = flags.fully_qualified_name()
        self.blended_command = "%s %s update %s <source_package_name> --from "\
                               " %s %s %s " % (flags.blended, flags.package,
                                               package_slug,
                                               list(login.keys())[0],
                                               list(password.keys())[0],
                                               list(label.keys())[0],
                                               )
        self.required_arguments = [{package_slug: "account/package_slug is fully qualified name of package,"
                                                  " that needs to be pass here"}]
        self.optional_arguments = [login, password,
                                   {"--from": "Need to pass source package after it."},
                                   label,
                                   {"<package_name>": "Source package name: Either pass it name with \"--from\" flag or"
                                                      " pass it after \"package name\" without \"--from\" flag."}]
        self.description = "This command updates a package with another package."


class PackageAsJson(Command):
    def __init__(self):
        super(PackageAsJson, self).__init__()
        flags = Flags()
        login = flags.login
        password = flags.password
        label = flags.label
        package_slug = flags.fully_qualified_name()
        self.blended_command = "%s %s as-json %s "\
                               " %s %s %s " % (flags.blended, flags.package,
                                               package_slug,
                                               list(login.keys())[0],
                                               list(password.keys())[0],
                                               list(label.keys())[0],
                                               )
        self.required_arguments = [{package_slug: "account/package_slug is fully qualified name of package,"
                                                  " that needs to be pass here"}]
        self.optional_arguments = [login, password, label]
        self.description = "This command display package in JSON format."


class PackageCompare(Command):
    def __init__(self):
        super(PackageCompare, self).__init__()
        flags = Flags()
        login = flags.login
        password = flags.password
        label = flags.label
        package_slug = flags.fully_qualified_name()
        self.blended_command = "%s %s compare %s --files"\
                               " %s %s %s " % (flags.blended, flags.package,
                                               package_slug,
                                               list(login.keys())[0],
                                               list(password.keys())[0],
                                               list(label.keys())[0],
                                               )
        self.required_arguments = [{package_slug: "account/package_slug is fully qualified name of package,"
                                                  " that needs to be pass here"}]
        self.optional_arguments = [login, password, label,
                                   {
                                          "--files": "This is a boolean flag, should be used when need to"
                                          " push specific files. Need to pass the file path after this flag"
                                      },
                                   ]
        self.description = "This command compares local filesystem package with Hub, If any differences are found," \
                           " conflicts/differences are printed listing all of the files and their locations, and the command exits."


class DirectorySetup(Command):
    def __init__(self):
        super(DirectorySetup, self).__init__()
        flags = Flags()
        login = flags.login
        password = flags.password
        self.blended_command = "%s setup <directory_path>"\
                               " %s %s " % (flags.blended, list(login.keys())[0], list(password.keys())[0])
        self.required_arguments = [{"<directory_path>": "path of the directory where themes in their respective account stored"}]
        self.optional_arguments = [login, password,
                                   {"--force": "This is a boolean flag, should be used when need to"
                                               " create forcefully"},
                                   ]
        self.description = "Initialize the path of the directory where themes in their respective account stored in the local filesystem."


class HelpCommands(object):
    def __init__(self, command, sub_command):
        commands = {
                    'account': {'create': AccountCreate,
                                'confirm': AccountConfirm,
                                'login': AccountLogin,
                                'add': AccountAdd,
                                'accept': AccountAccept,
                                'set-current': AccountSetCurrent,
                                'set': AccountSet,
                                'list': AccountList,
                                'revoke': AccountRevoke,
                                'current': AccountCurrent,
                                'email-verification': AccountEmailVerification,
                                },
                    'package': {'create': PackageCreate,
                                'clone': PackageClone,
                                'push': PackagePush,
                                'pull': PackagePull,
                                'install': PackageInstall,
                                'extend': PackageExtend,
                                'snapshot': PackageSnapshot,
                                'publish': PackagePublish,
                                'canonize': PackageCanonize,
                                'share': PackageShare,
                                'transfer': PackageTransfer,
                                'preview': PackagePreview,
                                'get': PackageGet,
                                'list': PackageList,
                                'revoke': PackageRevoke,
                                'retract': PackageRetract,
                                'detail': PackageDetail,
                                'version': PackageVersion,
                                'validate': PackageValidate,
                                'update': PackageUpdate,
                                'up': PackageUp,
                                'as-json': PackageAsJson,
                                'compare': PackageCompare,
                                },
                    'directory': {'setup': DirectorySetup},
                    }
        try:
            help_command_class = commands[command][sub_command]
        except KeyError:
            raise KeyError()
        else:
            print('help for:\n%sblended %s %s' % (spaces, command, sub_command))
        help_object = help_command_class()
        help_object.print_help()

# CLI HELP COMMAND CLASS
package_help_commands = HELP_BASIC_PACKAGE_COMMAND
account_help_commands = HELP_BASIC_ACCOUNT_COMMAND
package_help_commands_descriptions = HELP_BASIC_PACKAGE_COMMAND_DESCRIPTION
account_help_commands_descriptions = HELP_BASIC_ACCOUNT_COMMAND_DESCRIPTION


def help_command(commands, descriptions):
    """
    :param commands:
    :param descriptions:
    :return:
    """
    length_of_basic_commands = len(commands)
    for item in range(0, length_of_basic_commands):
        print('{2:>5}{0:{width}1}{1}'.format(commands[item],
                                             descriptions[item],
                                             '', width=3))


def help_for_domain():
    print('for detailed help')
    print("You can Use: 'blended help <domain>' (<domain> will be account or package)")

help_command_domain_list = ['package', 'account']
help_command_domain_details = {
    'package': {
        'commands': package_help_commands,
        'descriptions': package_help_commands_descriptions
    },
    'account': {
        'commands': account_help_commands,
        'descriptions': account_help_commands_descriptions
    },

}


def help_error_message(**kwargs):
    """
    :param kwargs:
    :return:
    """
    command = kwargs.get('command')
    sub_command = kwargs.get('sub_command')
    if not sub_command:
        sub_command = ''
    if not command:
        command = ''
    print("\nWrong Command: %s %s!!" % (command, sub_command))
    print("please use this command: 'blended help more' "
          "to know the actual <command> and <sub-command>!!")
    print("And try again with correct <command> and <sub-command> with:"
          " 'blended help <command> <sub-command>'\n")


class Help(CliffCommand):
    """
    """
    def get_parser(self, prog_name, **kwargs):
        parser = super(Help, self).get_parser(prog_name)
        parser.add_argument('command', nargs='?', default=None)
        parser.add_argument('subcommand', nargs='?', default=None)
        return parser

    def take_action(self, parsed_args):
        command = parsed_args.command
        sub_command = parsed_args.subcommand
        if (not command) and (not sub_command):
            help_command(HELP_BASIC_COMMAND, HELP_BASIC_COMMAND_DESCRIPTION)
            print("\nWant more commands?\nUse this command: 'blended help more'")
            print("{0:>5}or".format(''))
            help_for_domain()
        elif command == 'more':
            help_command(HELP_MORE_COMMAND, HELP_MORE_COMMAND_DESCRIPTION)
            help_for_domain()
            pass
        elif command == 'setup' and (not sub_command):
            try:
                HelpCommands("directory", 'setup')
            except KeyError:
                return help_error_message(command=command, sub_command=sub_command)
        elif (command in help_command_domain_list) and (not sub_command):
            print('%s commands:' % command)
            get_command = help_command_domain_details.get(command)
            help_commands = get_command.get('commands')
            help_commands_descriptions = get_command.get('descriptions')
            help_command(help_commands, help_commands_descriptions)
            print("\nfor details of an specific command\nUse this: 'blended help %s <sub-command>'" % (command))
            pass
        elif (command in help_command_domain_list) and sub_command:
            try:
                HelpCommands(command, sub_command.lower())
            except KeyError:
                return help_error_message(command=command, sub_command=sub_command)
        else:
            pass

