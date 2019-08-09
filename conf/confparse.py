import configparser
import logging
import os

# from logger_creation import LoggerSetup

current_d = os.getcwd()
# print(current_d)
directories_list = current_d.split('/')
# print(directories_list)
# print(directories_list[1:4])
# basic_desktop_path = directories_list[1:4]
conf_path = 'conf/'
# new_path = 'conf/'
# basic_desktop_path.append(new_path)
# conf_path = '/' + '/'.join(basic_desktop_path)


"""READING JIRA - BUGZILLA CONFIGURATION FILE CLASSES"""


# JIRA

class JiraReadConfigurationServer:
    # def __init__(self, debug_level):
    #     self.debug_level = debug_level

    def read_server_conf(self):

        # logging_configuration_server = LoggerSetup(name='jira_configuration_server',
        #                                            log_file='log/jira_configuration_server.log',
        #                                            level=self.debug_level)
        # logger_configuration_server = logging_configuration_server.setup_logger()
        # logger_configuration_server.info('JIRA Server declaration')
        config = configparser.ConfigParser()
        config.read('{}config.conf'.format(conf_path))
        # print(config.sections())
        if config['jira_hosting_server']['server'] is not '':
            server_auth = True
            server = config['jira_hosting_server']['server']
            server_reason = 'Server configuration is defined.'
            # logger_configuration_server.info('Server Declaration:')
            # logger_configuration_server.info(server_reason)
            # logger_configuration_server.debug('Server: ' + str(server))
            return {'server_auth': server_auth, 'server': server, 'server_reason': server_reason}
        else:
            server_auth = False
            server = None
            server_reason = 'No server configuration is defined. Please define a valid server link connection.'
            # logger_configuration_server.warning(server_reason)
            return {'server_auth': server_auth, 'server': server, 'server_reason': server_reason}


class JiraReadConfigurationBasicAuth:
    # def __init__(self, debug_level):
    #     self.debug_level = debug_level

    def read_user_basic_auth(self):
        # logging_configuration_basic_auth = LoggerSetup(name='jira_configuration_basic_auth',
        #                                                log_file='log/jira_configuration_basic_auth.log',
        #                                                level=self.debug_level)
        # logger_configuration_basic_auth = logging_configuration_basic_auth.setup_logger()
        # logger_configuration_basic_auth.info('JIRA Basic Authorization')
        config = configparser.ConfigParser()
        config.read('{}config.conf'.format(conf_path))
        if config['jira_basic_auth']['username'] is '' or config['jira_basic_auth']['password'] is '':
            basic_auth_reason = 'Missing values for valid Basic Authorization connection.'
            basic_auth = False
            if config['jira_basic_auth']['username'] is '':
                username = None
                username_reason = 'Missing username. Please define a username.'
                # logger_configuration_basic_auth.info(username_reason)
            else:
                username = config['jira_basic_auth']['username']
                username_reason = 'Username is defined.'
                # logger_configuration_basic_auth.info(username_reason)
                # logger_configuration_basic_auth.debug('Username: ' + str(username))
            if config['jira_basic_auth']['password'] is '':
                password = None
                password_reason = 'Missing password. Please define a password.'
                # logger_configuration_basic_auth.warning(password_reason)
            else:
                password = config['jira_basic_auth']['password']
                password_reason = 'Password is defined'
                # logger_configuration_basic_auth.info(password_reason)
                # logger_configuration_basic_auth.debug('Password: ' + str(password))
            return {'basic_auth': basic_auth, 'username': username, 'username_reason': username_reason,
                    'password': password, 'password_reason': password_reason, 'basic_auth_reason': basic_auth_reason}
        else:
            basic_auth_reason = 'All values for Basic Authorization connection are defined.'
            basic_auth = True
            username = config['jira_basic_auth']['username']
            username_reason = 'Username is defined.'
            password = config['jira_basic_auth']['password']
            password_reason = 'Password is defined'
            # logger_configuration_basic_auth.info(basic_auth_reason)
            # logger_configuration_basic_auth.debug('Username: ' + str(username))
            # logger_configuration_basic_auth.debug('Password: ' + str(password))
            return {'basic_auth': basic_auth, 'username': username, 'username_reason': username_reason,
                    'password': password, 'password_reason': password_reason, 'basic_auth_reason': basic_auth_reason}


class JiraReadConfigurationOAuth:
    # def __init__(self, debug_level):
    #     self.debug_level = debug_level

    def read_oauth(self):
        # logging_configuration_oauth = LoggerSetup(name='jira_configuration_oauth',
        #                                           log_file='log/jira_configuration_oauth.log',
        #                                           level=self.debug_level)
        # logger_configuration_oauth = logging_configuration_oauth.setup_logger()
        # logger_configuration_oauth.info('JIRA OAuth')
        config = configparser.ConfigParser()
        config.read('{}config.conf'.format(conf_path))
        if config['jira_oauth']['access_token'] is '' or config['jira_oauth']['access_token_secret'] is '' or config['jira_oauth']['consumer_key'] is '':
            oauth = False
            oauth_reason = 'Missing values for valid OAuth connection.'
            if config['jira_oauth']['access_token'] is '':
                access_token = None
                access_token_reason = 'No Access Token configuration is defined. Please define a valid Access Token.'
                # logger_configuration_oauth.warning(access_token_reason)
            else:
                access_token = config['jira_oauth']['access_token']
                access_token_reason = 'Access Token is defined.'
                # logger_configuration_oauth.info(access_token_reason)
                # logger_configuration_oauth.debug('Access Token: ' + str(access_token))
            if config['jira_oauth']['access_token_secret'] is '':
                access_token_secret = None
                access_token_secret_reason = 'No Access Token Secret configuration is defined. Please define ' \
                                             'a valid Access Token Secret.'
                # logger_configuration_oauth.warning(access_token_secret_reason)
            else:
                access_token_secret = config['jira_oauth']['access_token_secret']
                access_token_secret_reason = 'Access Token Secret is defined'
                # logger_configuration_oauth.info(access_token_secret_reason)
                # logger_configuration_oauth.debug('Access Token Secret: ' + str(access_token_secret))
            if config['jira_oauth']['consumer_key'] is '':
                consumer_key = None
                consumer_key_reason = 'No Consumer Key configuration is defined. Please define a Consumer Key.'
                # logger_configuration_oauth.warning(consumer_key_reason)
            else:
                consumer_key = config['jira_oauth']['consumer_key']
                consumer_key_reason = 'Consumer Key is defined.'
                # logger_configuration_oauth.info(consumer_key_reason)
                # logger_configuration_oauth.debug('Consumer Key: ' + str(consumer_key))
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
            # logger_configuration_oauth.info(oauth_reason)
            # logger_configuration_oauth.info(access_token_reason)
            # logger_configuration_oauth.debug('Access Token: ' + str(access_token))
            # logger_configuration_oauth.info(access_token_secret_reason)
            # logger_configuration_oauth.debug('Access Token Secret: ' + str(access_token_secret))
            # logger_configuration_oauth.info(consumer_key_reason)
            # logger_configuration_oauth.debug('Consumer Key: ' + str(consumer_key))
            return {'oauth': oauth, 'oauth_reason': oauth_reason, 'access_token': access_token,
                    'access_token_reason': access_token_reason, 'access_token_secret': access_token_secret,
                    'access_token_secret_reason': access_token_secret_reason, 'consumer_key': consumer_key,
                    'consumer_key_reason': consumer_key_reason}


class JiraReadConfigurationKerberos:
    # def __init__(self, debug_level):
    #     self.debug_level = debug_level

    def read_kerberos_auth(self):
        # logging_configuration_kerberos = LoggerSetup(name='jira_configuration_kerberos',
        #                                              log_file='log/jira_configuration_kerberos.log',
        #                                              level=self.debug_level)
        # logger_configuration_kerberos= logging_configuration_kerberos.setup_logger()
        # logger_configuration_kerberos.info('JIRA Kerberos Authorization')
        config = configparser.ConfigParser()
        config.read('{}config.conf'.format(conf_path))
        if config['jira_kerberos']['kerberos'] is '' or config['jira_kerberos_options']['mutual_authentication'] is '':
            kerberos_auth = False
            kerberos_auth_reason = 'Missing values for valid Kerberos Authorization connection.'
            # logger_configuration_kerberos.warning(kerberos_auth_reason)
            if config['jira_kerberos']['kerberos'] is '':
                kerberos = None
                kerberos_reason = 'Missing Kerberos Boolean value. Please define a value: True/False'
                # logger_configuration_kerberos.warning(kerberos_reason)
            else:
                kerberos = bool(config['jira_kerberos']['kerberos'])
                kerberos_reason = 'Kerberos Boolean is defined'
                # logger_configuration_kerberos.info(kerberos_reason)
                # logger_configuration_kerberos.debug('Kerberos: ' + str(kerberos))
            if config['jira_kerberos_options']['mutual_authentication'] is '':
                kerberos_options = None
                kerberos_options_reason = 'Missing Kerberos option. PLease define a value: ENABLED/DISABLED'
                # logger_configuration_kerberos.warning(kerberos_options_reason)
            else:
                kerberos_options = config['jira_kerberos_options']['mutual_authentication']
                kerberos_options_reason = 'Kerberos options are defined'
                # logger_configuration_kerberos.info(kerberos_options_reason)
                # logger_configuration_kerberos.debug('Kerberos options: ' + str(kerberos_options))
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
            # logger_configuration_kerberos.info(kerberos_auth_reason)
            # logger_configuration_kerberos.info(kerberos_reason)
            # logger_configuration_kerberos.debug('Kerberos: ' + str(kerberos))
            # logger_configuration_kerberos.info(kerberos_options_reason)
            # logger_configuration_kerberos.debug('Kerberos options: ' + str(kerberos_options))
            return {'kerberos_auth': kerberos_auth,'kerberos_auth_reason': kerberos_auth_reason, 'kerberos': kerberos,
                    'kerberos_reason': kerberos_reason,
                    'kerberos_options': kerberos_options,
                    'kerberos_options_reason': kerberos_options_reason}


# Bugzilla

class BugzillaReadConfigurationBasicAuth:
    # def __init__(self, debug_level):
    #     self.debug_level = debug_level

    def read_user_auth(self):
        # logging_configuration_basic_auth_bugzila = LoggerSetup(name='bugzilla_configuration_basic_auth',
        #                                                        log_file='log/bugzilla_configuration_basic_auth.log',
        #                                                        level=self.debug_level)
        # logger_configuration_basic_auth_bugzilla = logging_configuration_basic_auth_bugzila.setup_logger()
        # logger_configuration_basic_auth_bugzilla.info('Bugzilla Basic Authorization')
        config = configparser.ConfigParser()
        config.read('{}config.conf'.format(conf_path))
        if config['bugzilla_basic_auth']['username'] is '' or config['bugzilla_basic_auth']['password'] is '':
            basic_auth = False
            basic_auth_reason = 'Missing values for valid Basic Authorization connection.'
            # logger_configuration_basic_auth_bugzilla.warning(basic_auth_reason)
            if config['bugzilla_basic_auth']['username'] is '':
                username = None
                username_reason = 'Missing username. Please define a username.'
                # logger_configuration_basic_auth_bugzilla.warning(username_reason)
            else:
                username = config['bugzilla_basic_auth']['username']
                username_reason = 'Username is defined'
                # logger_configuration_basic_auth_bugzilla.info(username_reason)
                # logger_configuration_basic_auth_bugzilla.debug('Username: ' + str(username))
            if config['bugzilla_basic_auth']['password'] is '':
                password = None
                password_reason = 'Missing password. Please define a password.'
                # logger_configuration_basic_auth_bugzilla.info(password_reason)
            else:
                password = config['bugzilla_basic_auth']['password']
                password_reason = 'Password is defined'
                # logger_configuration_basic_auth_bugzilla.info(password_reason)
                # logger_configuration_basic_auth_bugzilla.debug('Password: ' + str(password))
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
            # logger_configuration_basic_auth_bugzilla.info(basic_auth_reason)
            # logger_configuration_basic_auth_bugzilla.info(username_reason)
            # logger_configuration_basic_auth_bugzilla.debug('Username: ' + str(username))
            # logger_configuration_basic_auth_bugzilla.info(password_reason)
            # logger_configuration_basic_auth_bugzilla.debug('Password: ' + str(password))
            return {'basic_auth': basic_auth, 'basic_auth_reason': basic_auth_reason, 'username': username,
                    'username_reason': username_reason,
                    'password': password, 'password_reason': password_reason}


class BugzillaReadConfigurationApiKey:
    # def __init__(self, debug_level):
    #     self.debug_level = debug_level

    def key_auth(self):
        # logging_configuration_key_bugzilla = LoggerSetup(name='bugzilla_configuration_key',
        #                                                  log_file='log/bugzilla_configuration_key.log',
        #                                                  level=self.debug_level)
        # logger_configuration_key_bugzilla = logging_configuration_key_bugzilla.setup_logger()
        # logger_configuration_key_bugzilla.info('Bugzilla API Key Authorization')
        config = configparser.ConfigParser()
        config.read('{}config.conf'.format(conf_path))
        if config['bugzilla_oauth']['api_key'] is not '':
            api_key_auth = True
            api_key = config['bugzilla_oauth']['api_key']
            api_key_reason = 'API Key configuration is defined.'
            # logger_configuration_key_bugzilla.info(api_key_reason)
            # logger_configuration_key_bugzilla.debug('API Key: ' + str(api_key))
        else:
            api_key_auth = False
            api_key = None
            api_key_reason = 'Missing API Key configuration. Please define an API Key.'
            # logger_configuration_key_bugzilla.warning(api_key_reason)
        return {'api_key_auth': api_key_auth, 'api_key': api_key, 'api_key_reason': api_key_reason}

