import configparser
import sys
from argparse import ArgumentParser


def user_settings(argv):

    parser = ArgumentParser()

    # ARGUMENTS --> hosting server
    parser.add_argument("-s", "--server", dest="serverHost",
                        help="add the hosting server IP", metavar="<HOSTING_SERVER_IP>")

    # ARGUMENTS --> basic_auth
    parser.add_argument("-u", "--username", dest="username",
                        help="add the username", metavar="<USERNAME>")
    parser.add_argument("-p", "--password", dest="password",
                        help="add the password", metavar="<PASSWORD>")

    # ARGUMENTS --> oath
    parser.add_argument("-a", "--access_token", dest="access_token",
                        help="add the access token", metavar="<ACCESS_TOKEN>")
    parser.add_argument("-t", "--access_token_secret", dest="access_token_secret",
                        help="add the Access Token Secret", metavar="<ACCESS_TOKEN_SECRET>")
    parser.add_argument("-k", "--consumer_key", dest="consumer_key",
                        help="add the Consumer Key", metavar="<CONSUMER_KEY>")
    # parser.add_argument("-c", "--key_cert", dest="key_cert",
    #                     help="add the Key Cert", metavar="<KEY_CERT>")

    key_cert_data = 'still looking for the data access'
    # code for key cert here:
    # key_cert_data = None
    # with open(key_cert, 'r') as key_cert_file:
    #     key_cert_data = key_cert_file.read()

    # ARGUMENTS --> extra
    parser.add_argument("-q", "--quiet",
                        action="store_false", dest="verbose", default=True,
                        help="don't print status messages to stdout")

    # arguments print
    arguments = parser.parse_args()
    print('HOSTING SERVER')
    print('server:', arguments.serverHost)
    print()
    print('BASIC AUTH')
    print('Username:', arguments.username)
    print('Password:', arguments.password)
    print()
    print('OAUTH')
    print('Access Token:', arguments.access_token)
    print('Access Token Secret:', arguments.access_token_secret)
    print('Consumer Key:', arguments.consumer_key)
    print('Key Cert:', key_cert_data)
    print()

    # ARGUMENTS --> KERBEROS
    kerberos_usage = input('Do you use Kerberos authentication protocol? (y/n)? ')
    if kerberos_usage == 'y':
        kerberos_enabled = True
        kerberos_options = {'mutual_authentication': 'DISABLED'}
        print('KERBEROS')
        print('Kerberos Usage:', kerberos_enabled)
        print('Kerberos options:', kerberos_options)
    if kerberos_usage == 'n':
        kerberos_enabled = False
        kerberos_options = 'There are no Kerberos options because Kerberos usage is False.'
        print('KERBEROS')
        print('Kerberos Usage:', kerberos_enabled)
        print('Kerberos options:', kerberos_options)
    print()
    print(arguments.verbose)


"""CREATING JIRA CONFIGURATION FILE"""


# def user_write_authorization(server, username, password, access_token, access_token_secret, consumer_key, key_cert):
#
#     config = configparser.ConfigParser()
#     config['jira_hosting_server'] = {'server': server}
#     config['jira_basic_auth'] = {'username': username,
#                                  'password': password
#                                  }
#     config['jira_oauth'] = {'access_token': access_token,
#                             'access_token_secret': access_token_secret,
#                             'consumer_key': consumer_key,
#                             'key_cert': key_cert
#                             }
#     with open('authentication.conf', 'w') as configfile:
#         config.write(configfile)
#     print()
#     print('Writing..')
#     print('Configuration file was created successfully!')


"""READING JIRA - BUGZILLA CONFIGURATION FILE CLASSES"""


# JIRA

class JiraReadConfigurationServer:

    config = configparser.ConfigParser()
    config.read('config.conf')
    # print(config.sections())
    if config['jira_hosting_server']['server'] is not '':
        server = config['jira_hosting_server']['server']
        server_reason = 'Server configuration is defined.'
    else:
        server = None
        server_reason = 'No server configuration is defined. Please define a server link connection.'


class JiraReadConfigurationBasicAuth:
    config = configparser.ConfigParser()
    config.read('config.conf')
    if config['jira_basic_auth']['username'] is '' or config['jira_basic_auth']['password'] is '':
        basic_auth_reason = 'Missing values for valid Basic Authorization connection.'
        if config['jira_basic_auth']['username'] is '':
            username = None
            username_reason = 'Missing username. Please define a username.'
        else:
            username = config['jira_basic_auth']['username']
        if config['jira_basic_auth']['password'] is '':
            password = None
            password_reason = 'Missing password. Please define a password.'
        else:
            password = config['jira_basic_auth']['password']
    else:
        basic_auth_reason = 'All values for Basic Authorization connection are defined.'
        username = config['jira_basic_auth']['username']
        password = config['jira_basic_auth']['password']


class JiraReadConfigurationOAuth:
    config = configparser.ConfigParser()
    config.read('config.conf')
    if config['jira_oauth']['access_token'] is '' or config['jira_oauth']['access_token_secret'] is '' or config['jira_oauth']['consumer_key'] is '':
        oauth_reason = 'Missing values for valid OAuth connection.'
        if config['jira_oauth']['access_token'] is '':
            access_token = None
            access_token_reason = 'No Access Token configuration is defined. Please define an Access Token.'
        else:
            access_token = config['jira_oauth']['access_token']
        if config['jira_oauth']['access_token_secret'] is '':
            access_token_secret = None
            access_token_secret_reason = 'No Access Token Secret configuration is defined. Please define an Access Token Secret.'
        else:
            access_token_secret = config['jira_oauth']['access_token_secret']
        if config['jira_oauth']['consumer_key'] is '':
            consumer_key = None
            consumer_key_reason = 'No Consumer Key configuration is defined. Please define a Consumer Key.'
        else:
            consumer_key = config['jira_oauth']['consumer_key']
        if config['jira_oauth']['key_cert'] is '':
            key_cert = None
            key_cert_reason = 'No Key Certificate configuration is defined. Please define a Key Certificate.'
    else:
        oauth_reason = 'All values for OAuth connection are defined.'
        access_token = config['jira_oauth']['access_token']
        access_token_secret = config['jira_oauth']['access_token_secret']
        consumer_key = config['jira_oauth']['consumer_key']
        key_cert = config['jira_oauth']['key_cert']


class JiraReadConfigurationKerberos:
    config = configparser.ConfigParser()
    config.read('config.conf')
    if config['jira_kerberos']['kerberos'] is '' or config['jira_kerberos_options']['mutual_authentication'] is '':
        kerberos_auth_reason = 'Missing values for valid Kerberos Authorization connection.'
        if config['jira_kerberos']['kerberos'] is '':
            kerberos = None
            kerberos_reason = 'Missing Kerberos Boolean value. Please define a value: True/False'
        else:
            kerberos = bool(config['jira_kerberos']['kerberos'])
        if config['jira_kerberos_options']['mutual_authentication'] is '':
            kerberos_options = None
            kerberos_options_reason = 'Missing Kerberos option. PLease define a value: ENABLED/DISABLED'
        else:
            kerberos_options = config['jira_kerberos_options']['mutual_authentication']
    else:
        kerberos_auth_reason = 'All values for Kerberos Authorization are defined.'
        kerberos = bool(config['jira_kerberos']['kerberos'])
        kerberos_options = config['jira_kerberos_options']['mutual_authentication']


# Bugzilla

class BugzillaReadConfigurationBasicAuth:

    config = configparser.ConfigParser()
    config.read('config.conf')
    if config['bugzilla_basic_auth']['username'] is '' or config['bugzilla_basic_auth']['password'] is '':
        basic_auth_reason = 'Missing values for valid Basic Authorization connection.'
        if config['bugzilla_basic_auth']['username'] is '':
            username = None
            username_reason = 'Missing username. Please define a username.'
        else:
            username = config['bugzilla_basic_auth']['username']
        if config['bugzilla_basic_auth']['password'] is '':
            password = None
            password_reason = 'Missing password. Please define a password.'
        else:
            password = config['bugzilla_basic_auth']['password']
    else:
        basic_auth_reason = 'All values for Basic Authorization connection are defined.'
        username = config['bugzilla_basic_auth']['username']
        password = config['bugzilla_basic_auth']['password']


class BugzillaReadConfigurationApiKey:

    config = configparser.ConfigParser()
    config.read('config.conf')
    if config['bugzilla_oauth']['api_key'] is not '':
        api_key = config['bugzilla_oauth']['api_key']
        api_key_reason = 'API Key configuration is defined.'
    else:
        api_key = None
        api_key_reason = 'Missing API Key configuration. Please define an API Key.'


if __name__ == '__main__':

    # user_settings(sys.argv[1:])

    # print()
    # print('CONFIGURATION FILE CREATION')
    # user_write_authorization(server=host, username=usr, password=pwd, access_token=acc_tok,
    #                          access_token_secret=acc_tok_secret, consumer_key=cons_key, key_cert=k_cert)
    # print()
    print('Reading configuration file..')
    print()
    print('-------------------- JIRA ----------------------')
    jira_connection = JiraReadConfigurationServer()
    jira_basic_auth = JiraReadConfigurationBasicAuth()
    jira_oauth = JiraReadConfigurationOAuth()
    jira_kerberos = JiraReadConfigurationKerberos()

    print('-------')
    print()
    print('JIRA Server')
    print()
    print(jira_connection.server_reason)
    print()
    if jira_connection.server is not None:
        print('Server:', jira_connection.server)
    else:
        print('Server:', jira_connection.server_reason)
    print()
    print('--------')
    print()
    print('JIRA Basic Authorization')
    print()
    print(jira_basic_auth.basic_auth_reason)
    print()
    if jira_basic_auth.username is not None:
        print('Username:', jira_basic_auth.username)
    else:
        print('Username:', jira_basic_auth.username_reason)
    if jira_basic_auth.password is not None:
        print('Password:', jira_basic_auth.password)
    else:
        print('Password:', jira_basic_auth.password_reason)
    print()
    print('--------')
    print()
    print('JIRA OAuth')
    print()
    print(jira_oauth.oauth_reason)
    print()
    if jira_oauth.access_token_secret is not None:
        print('Access Token:', jira_oauth.access_token)
    else:
        print('Access Token:', jira_oauth.access_token_reason)
    if jira_oauth.access_token_secret is not None:
        print('Access Token Secret:', jira_oauth.access_token_secret)
    else:
        print('Access Token Secret:', jira_oauth.access_token_secret_reason)
    if jira_oauth.consumer_key is not None:
        print('Consumer Key:', jira_oauth.consumer_key)
    else:
        print('Consumer Key:', jira_oauth.consumer_key_reason)
    if jira_oauth.key_cert is not None:
        print('Key Certificate:', jira_oauth.key_cert)
    else:
        print('Key Certificate:', jira_oauth.key_cert_reason)
    print()
    print('--------')
    print()
    print('JIRA Kerberos')
    print()
    print(jira_kerberos.kerberos_auth_reason)
    print()
    if jira_kerberos.kerberos is not None:
        print('Kerberos:', jira_kerberos.kerberos)
    else:
        print('Kerberos:', jira_kerberos.kerberos_reason)
    if jira_kerberos.kerberos_options is not None:
        print('kerberos Options - Mutual Authentication:', jira_kerberos.kerberos_options)
    else:
        print('kerberos Options - Mutual Authentication:', jira_kerberos.kerberos_options_reason)

    print()
    print()
    print()
    print('-------------------- Bugzilla ----------------------')
    print()
    bugzilla_basic_auth = BugzillaReadConfigurationBasicAuth()
    bugzilla_api_key_auth = BugzillaReadConfigurationApiKey()

    print('--------')
    print()
    print('Bugzilla Basic Authorization')
    print()
    print(bugzilla_basic_auth.basic_auth_reason)
    print()
    if bugzilla_basic_auth.username is not None:
        print('Username:', bugzilla_basic_auth.username)
    else:
        print('Username:', bugzilla_basic_auth.username_reason)
    if bugzilla_basic_auth.password is not None:
        print('Password:', bugzilla_basic_auth.password)
    else:
        print('Password:', bugzilla_basic_auth.password_reason)
    print()
    print('--------')
    print()
    print('Bugzilla API Key')
    print()
    if bugzilla_api_key_auth.api_key is not None:
        print('API Key:', bugzilla_api_key_auth.api_key)
    else:
        print('API Key:', bugzilla_api_key_auth.api_key_reason)
