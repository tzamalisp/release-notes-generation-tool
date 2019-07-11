import configparser
import logging
import sys
from argparse import ArgumentParser

# create and configure a logger
LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging_file = logging.basicConfig(filename='configuration.log', level=logging.DEBUG, format=LOG_FORMAT, filemode='w')

# root logger (without name)
logger = logging.getLogger()


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
    def read_server_conf(self):
        config = configparser.ConfigParser()
        config.read('conf/config.conf')
        # print(config.sections())
        if config['jira_hosting_server']['server'] is not '':
            server = config['jira_hosting_server']['server']
            server_reason = 'Server configuration is defined.'
            return {'server': server, 'server reason': server_reason}
        else:
            server = None
            server_reason = 'No server configuration is defined. Please define a server link connection.'
            return {'server': server, 'server_reason': server_reason}


class JiraReadConfigurationBasicAuth:
    def read_user_basic_auth(self):
        config = configparser.ConfigParser()
        config.read('conf/config.conf')
        if config['jira_basic_auth']['username'] is '' or config['jira_basic_auth']['password'] is '':
            basic_auth_reason = 'Missing values for valid Basic Authorization connection.'
            if config['jira_basic_auth']['username'] is '':
                username = None
                username_reason = 'Missing username. Please define a username.'
            else:
                username = config['jira_basic_auth']['username']
                username_reason = 'Username is defined.'
            if config['jira_basic_auth']['password'] is '':
                password = None
                password_reason = 'Missing password. Please define a password.'
            else:
                password = config['jira_basic_auth']['password']
                password_reason = 'Password is defined'
            return {'username': username, 'username_reason': username_reason, 'password': password,
                    'password_reason': password_reason, 'basic_auth_reason': basic_auth_reason}
        else:
            basic_auth_reason = 'All values for Basic Authorization connection are defined.'
            username = config['jira_basic_auth']['username']
            username_reason = 'Username is defined.'
            password = config['jira_basic_auth']['password']
            password_reason = 'Password is defined'
            return {'username': username, 'username_reason': username_reason, 'password': password,
                    'password_reason': password_reason, 'basic_auth_reason': basic_auth_reason}


class JiraReadConfigurationOAuth:
    def read_oauth(self):
        config = configparser.ConfigParser()
        config.read('conf/config.conf')
        if config['jira_oauth']['access_token'] is '' or config['jira_oauth']['access_token_secret'] is '' or config['jira_oauth']['consumer_key'] is '':
            oauth_reason = 'Missing values for valid OAuth connection.'
            if config['jira_oauth']['access_token'] is '':
                access_token = None
                access_token_reason = 'No Access Token configuration is defined. Please define an Access Token.'
            else:
                access_token = config['jira_oauth']['access_token']
                access_token_reason = 'Access Token is defined.'
            if config['jira_oauth']['access_token_secret'] is '':
                access_token_secret = None
                access_token_secret_reason = 'No Access Token Secret configuration is defined. Please define ' \
                                             'an Access Token Secret.'
            else:
                access_token_secret = config['jira_oauth']['access_token_secret']
                access_token_secret_reason = 'Access Token Secret is defined'
            if config['jira_oauth']['consumer_key'] is '':
                consumer_key = None
                consumer_key_reason = 'No Consumer Key configuration is defined. Please define a Consumer Key.'
            else:
                consumer_key = config['jira_oauth']['consumer_key']
                consumer_key_reason = 'Consumer Key is defined.'
            return {'oauth_reason': oauth_reason, 'access_token': access_token,
                    'access_token_reason': access_token_reason, 'access_token_secret': access_token_secret,
                    'access_token_secret_reason': access_token_secret_reason, 'consumer_key': consumer_key,
                    'consumer_key_reason': consumer_key_reason}
        else:
            oauth_reason = 'All values for OAuth connection are defined.'
            access_token = config['jira_oauth']['access_token']
            access_token_reason = 'Access Token is defined.'
            access_token_secret = config['jira_oauth']['access_token_secret']
            access_token_secret_reason = 'Access Token Secret is defined'
            consumer_key = config['jira_oauth']['consumer_key']
            consumer_key_reason = 'Consumer Key is defined.'
            return {'oauth_reason': oauth_reason, 'access_token': access_token,
                    'access_token_reason': access_token_reason, 'access_token_secret': access_token_secret,
                    'access_token_secret_reason': access_token_secret_reason, 'consumer_key': consumer_key,
                    'consumer_key_reason': consumer_key_reason}


class JiraReadConfigurationKerberos:
    def read_kerberos_auth(self):
        config = configparser.ConfigParser()
        config.read('conf/config.conf')
        if config['jira_kerberos']['kerberos'] is '' or config['jira_kerberos_options']['mutual_authentication'] is '':
            kerberos_auth_reason = 'Missing values for valid Kerberos Authorization connection.'
            if config['jira_kerberos']['kerberos'] is '':
                kerberos = None
                kerberos_reason = 'Missing Kerberos Boolean value. Please define a value: True/False'
            else:
                kerberos = bool(config['jira_kerberos']['kerberos'])
                kerberos_reason = 'Kerberos Boolean is defined'
            if config['jira_kerberos_options']['mutual_authentication'] is '':
                kerberos_options = None
                kerberos_options_reason = 'Missing Kerberos option. PLease define a value: ENABLED/DISABLED'
            else:
                kerberos_options = config['jira_kerberos_options']['mutual_authentication']
                kerberos_options_reason = 'Kerberos options are defined'
            return {'kerberos_auth_reason': kerberos_auth_reason, 'kerberos': kerberos,
                    'kerberos_reason': kerberos_reason,
                    'kerberos_options': kerberos_options,
                    'kerberos_options_reason': kerberos_options_reason}
        else:
            kerberos_auth_reason = 'All values for Kerberos Authorization are defined.'
            kerberos = bool(config['jira_kerberos']['kerberos'])
            kerberos_reason = 'Kerberos Boolean is defined'
            kerberos_options = config['jira_kerberos_options']['mutual_authentication']
            kerberos_options_reason = 'Kerberos options are defined'
            return {'kerberos_auth_reason': kerberos_auth_reason, 'kerberos': kerberos,
                    'kerberos_reason': kerberos_reason,
                    'kerberos_options': kerberos_options,
                    'kerberos_options_reason': kerberos_options_reason}


# Bugzilla

class BugzillaReadConfigurationBasicAuth:
    def read_user_auth(self):
        config = configparser.ConfigParser()
        config.read('conf/config.conf')
        if config['bugzilla_basic_auth']['username'] is '' or config['bugzilla_basic_auth']['password'] is '':
            basic_auth_reason = 'Missing values for valid Basic Authorization connection.'
            if config['bugzilla_basic_auth']['username'] is '':
                username = None
                username_reason = 'Missing username. Please define a username.'
            else:
                username = config['bugzilla_basic_auth']['username']
                username_reason = 'Username is defined'
            if config['bugzilla_basic_auth']['password'] is '':
                password = None
                password_reason = 'Missing password. Please define a password.'
            else:
                password = config['bugzilla_basic_auth']['password']
                password_reason = 'Password is defined'
            return {'basic_auth_reason': basic_auth_reason, 'username': username, 'username_reason': username_reason,
                    'password': password, 'password_reason': password_reason}
        else:
            basic_auth_reason = 'All values for Basic Authorization connection are defined.'
            username = config['bugzilla_basic_auth']['username']
            username_reason = 'Username is defined'
            password = config['bugzilla_basic_auth']['password']
            password_reason = 'Password is defined'
            return {'basic_auth_reason': basic_auth_reason, 'username': username, 'username_reason': username_reason,
                    'password': password, 'password_reason': password_reason}


class BugzillaReadConfigurationApiKey:
    def key_auth(self):
        config = configparser.ConfigParser()
        config.read('conf/config.conf')
        if config['bugzilla_oauth']['api_key'] is not '':
            api_key = config['bugzilla_oauth']['api_key']
            api_key_reason = 'API Key configuration is defined.'
        else:
            api_key = None
            api_key_reason = 'Missing API Key configuration. Please define an API Key.'
        return {'api_key': api_key, 'api_key_reason': api_key_reason}


if __name__ == '__main__':

    print()
    print('Reading configuration file..')
    print()

    # print()
    # print('JIRA Basic Authorization')
    # print()
    # print(jira_basic_auth.basic_auth_reason)
    # print()
    # if jira_basic_auth.username is not None:
    #     print('Username:', jira_basic_auth.username)
    # else:
    #     print('Username:', jira_basic_auth.username_reason)
    # if jira_basic_auth.password is not None:
    #     print('Password:', jira_basic_auth.password)
    # else:
    #     print('Password:', jira_basic_auth.password_reason)
    # print()
    # print('--------')
    # print()
    # print('JIRA OAuth')
    # print()
    # print(jira_oauth.oauth_reason)
    # print()
    # if jira_oauth.access_token_secret is not None:
    #     print('Access Token:', jira_oauth.access_token)
    # else:
    #     print('Access Token:', jira_oauth.access_token_reason)
    # if jira_oauth.access_token_secret is not None:
    #     print('Access Token Secret:', jira_oauth.access_token_secret)
    # else:
    #     print('Access Token Secret:', jira_oauth.access_token_secret_reason)
    # if jira_oauth.consumer_key is not None:
    #     print('Consumer Key:', jira_oauth.consumer_key)
    # else:
    #     print('Consumer Key:', jira_oauth.consumer_key_reason)
    # if jira_oauth.key_cert is not None:
    #     print('Key Certificate:', jira_oauth.key_cert)
    # else:
    #     print('Key Certificate:', jira_oauth.key_cert_reason)
    # print()
    # print('--------')
    # print()
    # print('JIRA Kerberos')
    # print()
    # print(jira_kerberos.kerberos_auth_reason)
    # print()
    # if jira_kerberos.kerberos is not None:
    #     print('Kerberos:', jira_kerberos.kerberos)
    # else:
    #     print('Kerberos:', jira_kerberos.kerberos_reason)
    # if jira_kerberos.kerberos_options is not None:
    #     print('kerberos Options - Mutual Authentication:', jira_kerberos.kerberos_options)
    # else:
    #     print('kerberos Options - Mutual Authentication:', jira_kerberos.kerberos_options_reason)
    #
    # print()
    # print()
    # print()
    # print('-------------------- Bugzilla ----------------------')
    # print()
    # bugzilla_basic_auth = BugzillaReadConfigurationBasicAuth()
    # bugzilla_api_key_auth = BugzillaReadConfigurationApiKey()
    #
    # print('--------')
    # print()
    # print('Bugzilla Basic Authorization')
    # print()
    # print(bugzilla_basic_auth.basic_auth_reason)
    # print()
    # if bugzilla_basic_auth.username is not None:
    #     print('Username:', bugzilla_basic_auth.username)
    # else:
    #     print('Username:', bugzilla_basic_auth.username_reason)
    # if bugzilla_basic_auth.password is not None:
    #     print('Password:', bugzilla_basic_auth.password)
    # else:
    #     print('Password:', bugzilla_basic_auth.password_reason)
    # print()
    # print('--------')
    # print()
    # print('Bugzilla API Key')
    # print()
    # if bugzilla_api_key_auth.api_key is not None:
    #     print('API Key:', bugzilla_api_key_auth.api_key)
    # else:
    #     print('API Key:', bugzilla_api_key_auth.api_key_reason)
