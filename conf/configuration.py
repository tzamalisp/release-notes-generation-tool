import configparser
import logging

# create and configure a logger
LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging_file = logging.basicConfig(filename='log/configuration.log',
                                   level=logging.DEBUG,
                                   format=LOG_FORMAT,
                                   filemode='w')

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
            server_auth = True
            server = config['jira_hosting_server']['server']
            server_reason = 'Server configuration is defined.'
            return {'server_auth': server_auth, 'server': server, 'server reason': server_reason}
        else:
            server_auth = False
            server = None
            server_reason = 'No server configuration is defined. Please define a server link connection.'
            return {'server_auth': server_auth, 'server': server, 'server_reason': server_reason}


class JiraReadConfigurationBasicAuth:
    def read_user_basic_auth(self):
        config = configparser.ConfigParser()
        config.read('conf/config.conf')
        if config['jira_basic_auth']['username'] is '' or config['jira_basic_auth']['password'] is '':
            basic_auth_reason = 'Missing values for valid Basic Authorization connection.'
            basic_auth = False
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
            return {'basic_auth': basic_auth, 'username': username, 'username_reason': username_reason,
                    'password': password, 'password_reason': password_reason, 'basic_auth_reason': basic_auth_reason}
        else:
            basic_auth_reason = 'All values for Basic Authorization connection are defined.'
            basic_auth = True
            username = config['jira_basic_auth']['username']
            username_reason = 'Username is defined.'
            password = config['jira_basic_auth']['password']
            password_reason = 'Password is defined'
            return {'basic_auth': basic_auth, 'username': username, 'username_reason': username_reason,
                    'password': password, 'password_reason': password_reason, 'basic_auth_reason': basic_auth_reason}


class JiraReadConfigurationOAuth:
    def read_oauth(self):
        config = configparser.ConfigParser()
        config.read('conf/config.conf')
        if config['jira_oauth']['access_token'] is '' or config['jira_oauth']['access_token_secret'] is '' or config['jira_oauth']['consumer_key'] is '':
            oauth = False
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
            return {'oauth': oauth, 'oauth_reason': oauth_reason, 'access_token': access_token,
                    'access_token_reason': access_token_reason, 'access_token_secret': access_token_secret,
                    'access_token_secret_reason': access_token_secret_reason, 'consumer_key': consumer_key,
                    'consumer_key_reason': consumer_key_reason}
        else:
            oauth = True
            oauth_reason = 'All values for OAuth connection are defined.'
            access_token = config['jira_oauth']['access_token']
            access_token_reason = 'Access Token is defined.'
            access_token_secret = config['jira_oauth']['access_token_secret']
            access_token_secret_reason = 'Access Token Secret is defined'
            consumer_key = config['jira_oauth']['consumer_key']
            consumer_key_reason = 'Consumer Key is defined.'
            return {'oauth': oauth, 'oauth_reason': oauth_reason, 'access_token': access_token,
                    'access_token_reason': access_token_reason, 'access_token_secret': access_token_secret,
                    'access_token_secret_reason': access_token_secret_reason, 'consumer_key': consumer_key,
                    'consumer_key_reason': consumer_key_reason}


class JiraReadConfigurationKerberos:
    def read_kerberos_auth(self):
        config = configparser.ConfigParser()
        config.read('conf/config.conf')
        if config['jira_kerberos']['kerberos'] is '' or config['jira_kerberos_options']['mutual_authentication'] is '':
            kerberos_auth = False
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
            return {'kerberos_auth': kerberos_auth, 'kerberos_auth_reason': kerberos_auth_reason, 'kerberos': kerberos,
                    'kerberos_reason': kerberos_reason,
                    'kerberos_options': kerberos_options,
                    'kerberos_options_reason': kerberos_options_reason}
        else:
            kerberos_auth = True
            kerberos_auth_reason = 'All values for Kerberos Authorization are defined.'
            kerberos = bool(config['jira_kerberos']['kerberos'])
            kerberos_reason = 'Kerberos Boolean is defined'
            kerberos_options = config['jira_kerberos_options']['mutual_authentication']
            kerberos_options_reason = 'Kerberos options are defined'
            return {'kerberos_auth': kerberos_auth,'kerberos_auth_reason': kerberos_auth_reason, 'kerberos': kerberos,
                    'kerberos_reason': kerberos_reason,
                    'kerberos_options': kerberos_options,
                    'kerberos_options_reason': kerberos_options_reason}


# Bugzilla

class BugzillaReadConfigurationBasicAuth:
    def read_user_auth(self):
        config = configparser.ConfigParser()
        config.read('conf/config.conf')
        if config['bugzilla_basic_auth']['username'] is '' or config['bugzilla_basic_auth']['password'] is '':
            basic_auth = False
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
            return {'basic_auth': basic_auth, 'basic_auth_reason': basic_auth_reason, 'username': username,
                    'username_reason': username_reason,
                    'password': password, 'password_reason': password_reason}
        else:
            basic_auth = True
            basic_auth_reason = 'All values for Basic Authorization connection are defined.'
            username = config['bugzilla_basic_auth']['username']
            username_reason = 'Username is defined'
            password = config['bugzilla_basic_auth']['password']
            password_reason = 'Password is defined'
            return {'basic_auth': basic_auth, 'basic_auth_reason': basic_auth_reason, 'username': username,
                    'username_reason': username_reason,
                    'password': password, 'password_reason': password_reason}


class BugzillaReadConfigurationApiKey:
    def key_auth(self):
        config = configparser.ConfigParser()
        config.read('conf/config.conf')
        if config['bugzilla_oauth']['api_key'] is not '':
            api_key_auth = True
            api_key = config['bugzilla_oauth']['api_key']
            api_key_reason = 'API Key configuration is defined.'
        else:
            api_key_auth = False
            api_key = None
            api_key_reason = 'Missing API Key configuration. Please define an API Key.'
        return {'api_key_auth': api_key_auth, 'api_key': api_key, 'api_key_reason': api_key_reason}

