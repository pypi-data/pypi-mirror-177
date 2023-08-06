from __future__ import absolute_import
import os
import sys
import json
from getpass import getpass
if sys.version_info[0] < 3:
    from __builtin__ import raw_input as input
else:
    from builtins import input
from beautifultable import BeautifulTable
from cliff.command import Command
from blended.blended_hostlib.backend import FileSystemBackend
from blended.blended_hostlib.network import Network
from blended.blended_hostlib.controller import Controller
from blended.blended_hostlib.exceptions import BlendedException, AccountActivationException

from blended.blendedcli.helpers import create_account, manage_session_key, \
      get_current_account, set_current_account, account_name_validation, \
      sessionNotAllowed, check_password, get_logged_in_account, get_current_account_from_network, \
      setup_logger


class AccountCreate(Command):
    """
    Command to create user.
    """
    def get_parser(self, prog_name, **kwargs):
        parser = super(AccountCreate, self).get_parser(prog_name)
        parser.add_argument('account_name', nargs='?', default=None)
        parser.add_argument('--name', nargs='?', default=None)
        parser.add_argument('--password', nargs='?', default=None)
        parser.add_argument('--email', nargs='?', default=None)
        parser.add_argument('--no-login', nargs='?', default=False, const=True)
        return parser

    def take_action(self, parsed_args):
        name = parsed_args.name
        password = parsed_args.password
        username = parsed_args.account_name
        email = parsed_args.email
        no_login = parsed_args.no_login
        if not username:
            username = input('Enter UserName: ')
        username = account_name_validation(username)
        if not name:
            name = input('Enter Name: ')
        if not email:
            email = input('Enter Email: ')
        if not password:
            password = getpass('Enter Password: ')
            re_password = getpass('Enter Confirm Password: ')
            if re_password != password:
                print("Confirm Password entry does not match Password.")
                sys.exit(0)
        if username.lower() == 'anonymous':
            print("Error: anonymous is not permitted as an account name.")
            sys.exit(0)            

        create_account(username, name, password, email=email, no_login=no_login)


class AccountActivate(Command):
    """
    Command to activate Account.
    """
    def get_parser(self, prog_name, **kwargs):
        parser = super(AccountActivate, self).get_parser(prog_name)
        parser.add_argument('token', default=None)
        parser.add_argument('--login', nargs='?', default=None)
        parser.add_argument('--password', nargs='?', default=None)
        parser.add_argument('--no-login', nargs='?', default=False, const=True)
        return parser

    def take_action(self, parsed_args):
        token = parsed_args.token
        password = parsed_args.password
        username = parsed_args.login
        no_login = parsed_args.no_login
        backend = FileSystemBackend()
        network = Network()
        if not token:
            token = input('Enter Token: ')
        if not username:
            username = input('Enter UserName: ')
        if not password:
            password = getpass('Enter Password: ')

        controller = Controller(network, backend)
        user_pk = network.get_user_pk()
        try:
            response = controller.update_account(username, activation_token=token)
        except BlendedException as exc:
            raise BlendedException(exc)
        else:
            print("Account %s is Activated" % (username))

        if no_login:
            network.session_key, user_pk = network.get_sessionkey()
            pass
        elif not no_login:
            network, user_pk = manage_session_key(username, password, network)
        else:
            raise ValueError("No value should passed in no-login option")

        return response
        # print("username: %s, password: %s, token: %s" % (username, password, token))


class AccountAccept(Command):
    """
    Command to accept inivitaion of Account.
    """
    def get_parser(self, prog_name, **kwargs):
        parser = super(AccountAccept, self).get_parser(prog_name)
        parser.add_argument('account_name', nargs='?', default=None)
        parser.add_argument('--login', nargs='?', default=None)
        parser.add_argument('--password', nargs='?', default=None)
        return parser

    def take_action(self, parsed_args):
        account_name = parsed_args.account_name
        password = parsed_args.password
        username = parsed_args.login
        network = Network()
        network, user_pk = manage_session_key(username, password, network)
        backend = FileSystemBackend()
        controller = Controller(network, backend)
        try:
            current_account = get_current_account(network, user_pk)
        except BlendedException as exc:
            raise BlendedException(exc)
        if current_account == 'anonymous':
            print("You are not logged in. Please log in or create an account.")
            sys.exit(0)
        if not account_name:
            account_name = input("Please Enter Account Name : ")
        account_name = account_name_validation(account_name, action='accept')
        try:
            response = controller.accept_invite(user_pk, account_slug=account_name)  # token=token
        except BlendedException as exc:
            try:
                if exc.args[0].args[0]['status_code'] == 5022:
                    print("False attempt.")
                    sys.exit(0)
                elif exc.args[0].args[0]['status_code'] == 4035:
                    print("Account name is required. It may not be blank. Please try again.")
                    sys.exit(0)
                elif exc.args[0].args[0]['status_code'] == 5054:
                    print("Already member of account \"%s\"." % (account_name))
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
        if response:
            print(response)
        print("Now you are added as Collaborator in the account \"%s\"." % (account_name))


class AccountList(Command):
    """
    Command to get the list of accounts.
    """
    def get_parser(self, prog_name, **kwargs):
        parser = super(AccountList, self).get_parser(prog_name)
        parser.add_argument('account_name', nargs='?', default=None)
        parser.add_argument('--login', nargs='?', default=None, help="Login account")
        parser.add_argument('--password', nargs='?', default=None)
        return parser

    def take_action(self, parsed_args):
        account_name = parsed_args.account_name
        password = parsed_args.password
        username = parsed_args.login
        # account_list_user_collaborator_on = []
        # all_collaborator_in_current_account = []
        # all_collaborator_in_account = []
        network = Network()
        network, user_pk = manage_session_key(username, password, network)

        backend = FileSystemBackend()
        controller = Controller(network, backend)
        try:
            current_account = get_current_account(network, user_pk)
        except BlendedException as exc:
            raise BlendedException(exc)
        if current_account == 'anonymous':
            print("You are not logged in. Please log in or create an account.")
            sys.exit(0)

        all_collaborator_in_current_account = BeautifulTable()
        all_collaborator_in_current_account.column_headers = ['User_Name', 'Email']
        all_collaborator_in_account = BeautifulTable()
        all_collaborator_in_account.column_headers = ['User_Name', 'Email']
        account_list_user_collaborator_on = BeautifulTable()
        account_list_user_collaborator_on.column_headers = ['Account_Name', 'Role']
        if account_name:
            try:
                response_user = controller.get_account_users(account_name)
            except BlendedException as exc:
                try:
                    if exc.args[0].args[0]['status_code'] == 5014:
                        print("User \"%s\" is not a member of Account \"%s\"." % (account_name, user_pk))
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
            for user in response_user.items:
                # all_collaborator_in_account.append({'user_name': user.user_name,
                #                                     'email': user.email})
                all_collaborator_in_account.append_row([user.user_name, user.email])

            print("\nList of all Collaborators in Account \"%s\":\n" % (account_name))
            if not len(all_collaborator_in_account):
                all_collaborator_in_account = []
            print(all_collaborator_in_account)
            print("\n")
        else:
            try:
                response_list = controller.get_account_list(user_pk)
            except BlendedException as exc:
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
            try:
                response_user = controller.get_account_users(current_account)
            except BlendedException as exc:
                raise BlendedException(exc)
            for item in response_list.items:
                # account_list_user_collaborator_on.append({'account_name': item.name,
                #                                          'role': item.role})
                account_list_user_collaborator_on.append_row([item.name, item.role])
            for user in response_user.items:
                # all_collaborator_in_current_account.append({'user_name': user.user_name,
                #                                             'email': user.email})
                all_collaborator_in_current_account.append_row([user.user_name, user.email])

            print("\nList of all Accounts user is Collaborator on:\n")
            if not len(account_list_user_collaborator_on):
                account_list_user_collaborator_on = []
            print(account_list_user_collaborator_on)
            print("\nList of all Collaborators in Current-account:\n")
            if not len(all_collaborator_in_current_account):
                all_collaborator_in_current_account = []
            print(all_collaborator_in_current_account)
            print("\n")


class AccountEmailVerification(Command):
    """
    Command to set current Account active.
    """
    def get_parser(self, prog_name, **kwargs):
        parser = super(AccountEmailVerification, self).get_parser(prog_name)
        parser.add_argument('email', nargs='?', default=None, help="Needed email address that need to be added")
        parser.add_argument('--login', nargs='?', default=None)
        parser.add_argument('--password', nargs='?', default=None)
        return parser

    def take_action(self, parsed_args):
        email = parsed_args.email
        password = parsed_args.password
        username = parsed_args.login
        network = Network()
        network, user_pk = manage_session_key(username, password, network)
        backend = FileSystemBackend()
        controller = Controller(network, backend)
        try:
            current_account = get_current_account(network, user_pk)
        except BlendedException as exc:
            raise BlendedException(exc)
        if current_account == 'anonymous':
            print("You are not logged in. Please log in or create an account.")
            sys.exit(0)
        if not email:
            email = input("Please Enter email : ")
        try:
            response = controller.account_email_verification(email)
        except BlendedException as exc:
            try:
                if exc.args[0].args[0]['status_code'] == 5002:
                    sessionNotAllowed()
                    sys.exit(0)
            except Exception:
                pass
            print(exc)
            sys.exit(0)
        except AccountActivationException as exc:
            print(exc)
            sys.exit(0)
        if response:
            print(response)
        print("A verification link has been sent to your email \"%s\". Please verify your account." % (email))


class AccountAdd(Command):
    """
    Command to add collaborator to an account.
    """
    def get_parser(self, prog_name, **kwargs):
        parser = super(AccountAdd, self).get_parser(prog_name)
        parser.add_argument('account_name', nargs='?', default=None, help="Needed account name that need to be added")
        parser.add_argument('--login', nargs='?', default=None)
        parser.add_argument('--password', nargs='?', default=None)
        parser.add_argument('--account', nargs='?', default=None)
        parser.add_argument('--admin', nargs='?', default=False, const=True)
        parser.add_argument('--read', nargs='?', default=False, const=True)
        parser.add_argument('--write', nargs='?', default=False, const=True)
        parser.add_argument('--email',  nargs='?', default=False, const=True)
        return parser

    def take_action(self, parsed_args):
        account_name = parsed_args.account_name
        password = parsed_args.password
        username = parsed_args.login
        email = parsed_args.email
        user_account = parsed_args.account
        admin_option = parsed_args.admin
        read_option = parsed_args.read
        write_option = parsed_args.write
        network = Network()
        network, user_pk = manage_session_key(username, password, network)
        backend = FileSystemBackend()
        controller = Controller(network, backend)
        check_flag = False
        access_type = None
        if account_name:
            account_name = account_name_validation(account_name, action='add')
        elif isinstance(email, bool):
            if email:
                email = input("Please Enter Email : ")
                check_flag = True
        elif not email:
            email = input("Please Enter Email : ")
            check_flag = True
        
        if check_flag and not email:
            print("Error: Email is required. It may not be blank. Please try again.")
            sys.exit(0)
        if not (email or account_name):
            account_name = input("Please Enter Account Name : ")
            account_name = account_name_validation(account_name, action='add')
       
        try:
            if get_current_account(network, user_pk) == 'anonymous':
                print("You are not logged in. Please log in or create an account.")
                sys.exit(0)
        except BlendedException as exc:
            raise BlendedException(exc)

        try:
            assert user_account != None
            try:
                if admin_option and not (read_option or write_option):
                    access_type = 'ADMIN'
                elif read_option and not (admin_option or write_option):
                    access_type = 'READ'
                elif write_option and not (admin_option or read_option):
                    access_type = 'WRITE'
                elif (admin_option or read_option or write_option):
                    print("You can not pass multiple access type. Please try again.")
                    sys.exit(0)
                if not access_type:
                    access_type = 'READ'
                if account_name:
                    response = controller.invite_user(user_account, account_slug=account_name, access_type=access_type)
                elif email:
                    response = controller.invite_user(user_account, email=email, access_type=access_type)
                else:
                    print("Error: Account name is required. It may not be blank. Please try again.")
                    sys.exit(0)
            except BlendedException as exc:
                print(exc.args[0]['message'])
                sys.exit(0)
        except AssertionError:
            try:
                user_account = get_current_account(network, user_pk)
            except BlendedException as exc:
                raise BlendedException(exc)
            else:
                try:
                    if admin_option and not (read_option or write_option):
                        access_type = 'ADMIN'
                    elif read_option and not (admin_option or write_option):
                        access_type = 'READ'
                    elif write_option and not (admin_option or read_option):
                        access_type = 'WRITE'
                    elif admin_option or read_option or write_option:
                        print("You can not pass multiple access type. Please try again.")
                        sys.exit(0)
                    if not access_type:
                        access_type = 'READ'
                    if account_name:
                        response = controller.invite_user(user_account, account_slug=account_name, access_type=access_type)
                    elif email:
                        response = controller.invite_user(user_account, email=email, access_type=access_type)
                    else:
                        print("Error: Account name is required. It may not be blank. Please try again.")
                        sys.exit(0)
                except BlendedException as exc:
                    try:
                        if exc.args[0]['status_code'] == 5002:
                            sessionNotAllowed()
                            sys.exit(0)
                        print("\nError: Invitation Failed\n")
                        if exc.args[0]['status_code'] == 4035:
                            print('Enter a valid email address.')
                            sys.exit(0)
                        elif exc.args[0]['status_code'] == 5054:
                            if exc.args[0]['message'] == '%s is already member of account.' % (account_name):
                                print('Account "%s" is already a member of your organization.' % (account_name))
                            else:
                                print(exc.args[0]['message'])
                            sys.exit(0)
                        elif exc.args[0]['status_code'] == 5069:
                            print('You cannot invite to an organization. Try to invite an individual Account.')
                            sys.exit(0)
                        elif exc.args[0]['status_code']:
                            print(exc.args[0]['message'])
                            sys.exit(0)
                        else:
                            raise BlendedException(exc)
                    except Exception:
                        raise BlendedException(exc)
 
        if account_name:
            print("Pending Invite Sent Successfully To Account \"%s\". Please accept it." % (account_name))
        else:
            print("Pending Invite Sent Successfully To Your Email \"%s\". Please accept it." % (email))


class AccountRevoke(Command):
    """
    Command to Revoke collaborator from an account.
    """
    def get_parser(self, prog_name, **kwargs):
        parser = super(AccountRevoke, self).get_parser(prog_name)
        parser.add_argument('account_name', default=None, help="Needed account name that need to be added")
        parser.add_argument('--login', nargs='?', default=None)
        parser.add_argument('--password', nargs='?', default=None)
        parser.add_argument('--account', nargs='?', default=None, help="Needed 'user account name' where 'account name' need to be added")
        return parser

    def take_action(self, parsed_args):
        # import pdb; pdb.set_trace()
        slug = parsed_args.account_name
        password = parsed_args.password
        username = parsed_args.login
        account_slug = parsed_args.account
        if not username:
            username = input('Enter UserName: ')
        if not password:
            password = getpass('Enter Password: ')
        network = Network()
        network, user_pk = manage_session_key(username, password, network)
        backend = FileSystemBackend()  # FileSystemBackend(blended_dir)
        controller = Controller(network, backend)
        if not account_slug:
            account_slug = get_current_account(network, user_pk)
        try:
            response = controller.revoke_account(slug, account_slug)
        except BlendedException as exc:
            raise BlendedException(exc)
        print(response)


class AccountSetCurrent(Command):
    """
    Command to set current Account active.
    """
    def get_parser(self, prog_name, **kwargs):
        parser = super(AccountSetCurrent, self).get_parser(prog_name)
        parser.add_argument('account_name', nargs='?', default=None, help="Needed account name that need to be added")
        parser.add_argument('--login', nargs='?', default=None)
        parser.add_argument('--password', nargs='?', default=None)
        return parser

    def take_action(self, parsed_args):
        account_name = parsed_args.account_name
        password = parsed_args.password
        username = parsed_args.login
        network = Network()
        network, user_pk = manage_session_key(username, password, network)
        current_account = user_pk
        backend = FileSystemBackend()
        controller = Controller(network, backend)
        try:
            current_account = get_current_account(network, user_pk)
        except BlendedException as exc:
            raise BlendedException(exc)
        if current_account == 'anonymous':
            print("You are not logged in. Please log in or create an account.")
            sys.exit(0)
        if account_name:
            try:
                response = controller.set_current_account(account_name)
            except BlendedException as exc:
                try:
                    if exc.args[0].args[0]['status_code'] == 1001:
                        print("\nAlert: Operation Not Permitted\n")
                        print(exc.args[0].args[0]['message'])
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
            else:
                set_current_account(account_name)
        else:
            account_name = input("Please enter the account name you want to set as current account:")
            account_name = account_name_validation(account_name, action='set')
            try:
                response = controller.set_current_account(account_name)
            except BlendedException as exc:
                try:
                    if exc.args[0].args[0]['status_code'] == 5002:
                        sessionNotAllowed()
                        sys.exit(0)
                    elif exc.args[0].args[0]['status_code'] == 4035:
                        print("Error: Account name is required. It may not be blank. Please try again.")
                        sys.exit(0)
                    elif exc.args[0].args[0]['status_code'] == 5014:
                        print("Error:User is not a member of the account \"%s\"." % (current_account))
                        sys.exit(0)
                    elif exc.args[0].args[0]['status_code']:
                        print(exc.args[0].args[0]['message'])
                        sys.exit(0)
                    else:
                        raise BlendedException(exc)
                except Exception:
                    raise BlendedException(exc)
            else:
                set_current_account(account_name)
        if response:
            print(response)
        print("Account \"%s\" is set as current-account successfully!" % (account_name))


class AccountCurrent(Command):
    """
    """
    def get_parser(self, prog_name, **kwargs):
        parser = super(AccountCurrent, self).get_parser(prog_name)
        parser.add_argument('--login', nargs='?', default=None)
        parser.add_argument('--password', nargs='?', default=None)
        return parser

    def take_action(self, parsed_args):
        password = parsed_args.password
        username = parsed_args.login
        network = Network()
        network, user_slug = manage_session_key(username, password, network)
        account_name = get_current_account_from_network(network, user_slug)
        if account_name:
            print(account_name)


class AccountLogin(Command):
    """
    Command to login.
    """
    def get_parser(self, prog_name, **kwargs):
        parser = super(AccountLogin, self).get_parser(prog_name)
        parser.add_argument('account_name', nargs='?', default=None, help="Needed account name that need to be added")
        parser.add_argument('--login', nargs='?', default=None)
        parser.add_argument('--password', nargs='?', default=None)
        return parser

    def take_action(self, parsed_args):
        account_name = parsed_args.account_name
        password = parsed_args.password
        username = parsed_args.login
        if not username:
            username = input("Enter Username: ").strip()
            username = account_name_validation(username)
        if not password:
            password = getpass("Enter Password: ")
            password = check_password(password)
        network = Network()
        network, user_slug = manage_session_key(username, password, network)
        print("Hi %s, you are logged in now!" % (user_slug))


class AccountLogout(Command):
    """
    Command to logout.
    """
    def get_parser(self, prog_name, **kwargs):
        parser = super(AccountLogout, self).get_parser(prog_name)
        parser.add_argument('--login', nargs='?', default=None)
        parser.add_argument('--password', nargs='?', default=None)
        return parser

    def take_action(self, parsed_args):
        password = parsed_args.password
        username = parsed_args.login
        network = Network()
        network = Network()
        network, user_slug = manage_session_key(username, password, network)
        try:
            current_account = get_current_account(network, user_slug)
        except BlendedException as exc:
            raise BlendedException(exc)
        logged_in_user = get_logged_in_account()
        if not logged_in_user:
            logged_in_user = current_account
        if current_account == 'anonymous':
            print("You are not logged in. Please log in or create an account.")
            sys.exit(0)
        try:
            network.logout()
        except BlendedException as exc:
            raise BlendedException(exc)
        network.set_sessionkey(None, 'anonymous')
        set_current_account('anonymous')
        
        print("Hi %s, you are logged out now!" % (logged_in_user))


class AccountPasswordUpdate(Command):
    """
    Command to Change password.
    """
    
    def get_parser(self, prog_name, **kwargs):
        parser = super(AccountPasswordUpdate, self).get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        network = Network()
        backend = FileSystemBackend()
        network, user_slug = manage_session_key(None, None, network)
        try:
            current_account = get_current_account(network, user_slug)
        except BlendedException as exc:
            raise BlendedException(exc)
        logged_in_user = get_logged_in_account()
        if not logged_in_user:
            logged_in_user = current_account
        if current_account == 'anonymous':
            print("You are not logged in. Please log in or create an account.")
            sys.exit(0)
        print("Note: Password must be at least 8 characters, and contain one letter and one number.\n")
        old_password = getpass('Enter Current Password: ')
        if not old_password:
            print("Error: Password is required. It may not be blank. Please try again.")
            sys.exit(0)
        password = getpass('Enter New Password: ')
        if not password:
            print("Error: New Password is required. It may not be blank. Please try again.")
            sys.exit(0)
        authenticate_password(password)
        re_password = getpass('Enter Confirm New Password: ')
        if password and re_password and (re_password != password):
            print("Confirm Password entry does not match Password.")
            sys.exit(0)
        elif  not re_password:
            print("Error: Confirm New Password is required. It may not be blank. Please try again.")
            sys.exit(0)
        controller = Controller(network, backend)
        body = {"oldPassword": old_password, "newPassword": password}
        # import pdb; pdb.set_trace()
        try:
            response = controller.update_account(logged_in_user, old_password=old_password, new_password=password)
        except BlendedException as exc:
            try:
                if exc.args[0].args[0]['status_code'] == 5002:
                    sessionNotAllowed()
                elif exc.args[0].args[0]['status_code']:
                    print(exc.args[0].args[0]['message'])
                    sys.exit(0)
                else:
                    raise BlendedException(exc)
            except Exception:
                raise BlendedException(exc)
        network.set_sessionkey(None, 'anonymous')
        set_current_account('anonymous')
        print("Your password has been changed successfully! Please login to continue." )


def authenticate_password(password):
    """
    """
    import re
    if len(password)<8 or not re.match('^(?=.*[0-9]$)(?=.*[a-zA-Z])', password):
        print("Error: Password must be at least 8 characters, and contain one letter and one number.")
        sys.exit(0)
    if not re.match(r'^([0-9]*[a-z]*[A-Z]*[@]*[-]*[_]*)*$', password):
        re.match(r'^(?=.*[\w\d]).+', password)
        print("Error: You've entered an invalid Password. "
                "Accepted Password include alphanumeric, underscore(_) and/or dash(-).")
        sys.exit(0)
