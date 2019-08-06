import logging
import requests
import configparser
import os
from requests_oauthlib import OAuth1
from pprint import pprint

from conf.confparse import JiraReadConfigurationServer
from conf.confparse import JiraReadConfigurationBasicAuth
from conf.confparse import JiraReadConfigurationOAuth

from logger_creation import LoggerSetup

current_d = os.getcwd()
# print(current_d)
directories_list = current_d.split('/')
# print(directories_list)
# print(directories_list[1:4])
basic_desktop_path = directories_list[1:4]
new_path = 'conf/'
basic_desktop_path.append(new_path)
conf_path = '/' + '/'.join(basic_desktop_path)
working_directory_path = directories_list[1:]
configuration_directory_path = '/' + '/'.join(working_directory_path)


""" CONNECTING TO JIRA API WITH THE CORRESPONDING AUTHENTICATION WAY """


class Connector:
    def __init__(self, debug_level):
        self.debug_level = debug_level

    def connection_jira(self):
        logging_jira_connection = LoggerSetup(name='jira_connection_logger',
                                              log_file='log/jira_connection.log',
                                              level=self.debug_level)
        logger_jira_connection = logging_jira_connection.setup_logger()
        logger_jira_connection.debug('Connection to JIRA API')
        # AUTHENTICATION
        options = {}
        # JIRA connection credentials
        server_connection = JiraReadConfigurationServer()
        server_auth = server_connection.read_server_conf()['server_auth']
        if server_auth is True:
            server_value = server_connection.read_server_conf()['server']
            options['server'] = server_value
        else:
            server_reason_value = server_connection.read_server_conf()['server_reason']
            logger_jira_connection.warning(server_reason_value)
            # raise Exception(server_reason_value)
        # Authentication objects
        jira_basic_auth = JiraReadConfigurationBasicAuth()
        jira_oauth = JiraReadConfigurationOAuth()
        # code for key cert here
        key_cert_data = None
        # with open(key_cert, 'r') as key_cert_file:
        #     key_cert_data = key_cert_file.read()
        key_cert_data = 'To be added'

        basic_auth = jira_basic_auth.read_user_basic_auth()['basic_auth']
        oauth = jira_oauth.read_oauth()['oauth']

        if basic_auth is True or oauth is True:
            if basic_auth is True:
                basic_auth_reason_value = jira_basic_auth.read_user_basic_auth()['basic_auth_reason']
                username_value = jira_basic_auth.read_user_basic_auth()['username']
                username_reason_value = jira_basic_auth.read_user_basic_auth()['username_reason']
                password_value = jira_basic_auth.read_user_basic_auth()['password']
                password_reason_value = jira_basic_auth.read_user_basic_auth()['password_reason']
                options['authentication'] = (username_value, password_value)
                logger_jira_connection.info(basic_auth_reason_value)
                # logger_jira_connection.debug(str(options['authentication']))
            elif oauth is True:
                oauth_reason_value = jira_oauth.read_oauth()['oauth_reason']
                access_token_value = jira_oauth.read_oauth()['access_token']
                access_token_reason_value = jira_oauth.read_oauth()['access_token_reason']
                access_token_secret_value = jira_oauth.read_oauth()['access_token_secret']
                access_token_secret_reason_value = jira_oauth.read_oauth()['access_token_secret_reason']
                consumer_key_value = jira_oauth.read_oauth()['consumer_key']
                consumer_key_reason_value = jira_oauth.read_oauth()['consumer_key_reason']
                logger_jira_connection.info(oauth_reason_value)
                logger_jira_connection.info(access_token_reason_value)
                logger_jira_connection.info(access_token_secret_reason_value)
                logger_jira_connection.info(consumer_key_reason_value)
                # (TO DEFINE THE IF STATEMENT HERE):
                if key_cert_data is not None:
                    # OAuth1('YOUR_APP_KEY', 'YOUR_APP_SECRET', 'USER_OAUTH_TOKEN', 'USER_OAUTH_TOKEN_SECRET')
                    options['authentication'] = OAuth1(access_token_value,
                                                       access_token_secret_value,
                                                       consumer_key_value,
                                                       key_cert_data)
                else:
                    logger_jira_connection.warning('Please add the key certification data.')
                    # raise Exception('Please add the key certification data.')
        else:
            if basic_auth is False:
                basic_auth_reason_value = jira_basic_auth.read_user_basic_auth()['basic_auth_reason']
                username_reason_value = jira_basic_auth.read_user_basic_auth()['username_reason']
                password_reason_value = jira_basic_auth.read_user_basic_auth()['password_reason']
                print(basic_auth_reason_value)
                print(username_reason_value)
                print(password_reason_value)
                logger_jira_connection.warning(basic_auth_reason_value)
                logger_jira_connection.warning(username_reason_value)
                logger_jira_connection.warning(password_reason_value)
                logger_jira_connection.warning('Basic Authentication failed.')
                # raise Exception('Basic Authentication failed.')
            elif oauth is False:
                oauth_reason_value = jira_oauth.read_oauth()['oauth_reason']
                access_token_reason_value = jira_oauth.read_oauth()['access_token_reason']
                access_token_secret_reason_value = jira_oauth.read_oauth()['access_token_secret_reason']
                consumer_key_reason_value = jira_oauth.read_oauth()['consumer_key_reason']
                print(oauth_reason_value)
                print(access_token_reason_value)
                print(access_token_secret_reason_value)
                print(consumer_key_reason_value)
                logger_jira_connection.warning(oauth_reason_value)
                logger_jira_connection.warning(access_token_reason_value)
                logger_jira_connection.warning(access_token_secret_reason_value)
                logger_jira_connection.warning(consumer_key_reason_value)
                logger_jira_connection.warning('OAuth Authentication failed.')
                # raise Exception('OAuth Authentication failed.')

        return options


""" READING SEARCH TERMS FROM CONFIGURATION FILE """


class ConfigData:
    def __init__(self, search_field, input_terms):
        self.search_field = search_field
        self.input_terms = input_terms

    def get_config_search_data(self):
        # READ FIELDS FROM CONF or USER INPUT
        search_list_output = ''
        config = configparser.ConfigParser()
        config.read('{}config.conf'.format(conf_path))
        # read fields from configuration
        # JIRA search terms configuration file reading
        search_terms_config = configparser.ConfigParser()
        search_terms_config.read('{}/conf/search_terms.conf'.format(configuration_directory_path))
        search_list_conf_input = search_terms_config[self.search_field]['search_list']
        search_list_conf_input = search_list_conf_input.replace(', ', ',')
        search_list_conf_input = search_list_conf_input.replace(' ,', ',')
        search_list_conf_input = search_list_conf_input.replace(' , ', ',')
        search_list_conf_input = search_list_conf_input.split(',')
        print('Fields from conf file:', search_list_conf_input)
        print('Fields from terminal:', self.search_field)
        if self.input_terms is not None:
            search_list_output = search_list_conf_input + self.input_terms
            print(search_list_output)
        elif self.input_terms is None:
            search_list_output = search_list_conf_input
            print(search_list_output)

        return search_list_output


"""  TARGET RELEASE """


class TargetReleaseJira:
    def __init__(self, release_name, release, order, debug_level):
        self.release_name = release_name
        self.release = release
        self.order = order
        self.debug_level = debug_level

    def get_release_notes(self):
        logging_jira_release_notes = LoggerSetup(name='jira_target_release_logger',
                                                 log_file='log/jira_target_releases.log',
                                                 level=self.debug_level)
        logger_jira_release_notes = logging_jira_release_notes.setup_logger()
        logger_jira_release_notes.debug('Entering JIRA Target Release function')
        # AsciiDoc data collection list
        ascii_data_list = []

        # Connecting to JIRA REST API
        logger_jira_release_notes.debug('Calling Connection to JIRA API Class')
        connection = Connector(debug_level=self.debug_level)
        options = connection.connection_jira()

        # Retrieving the Release Notes from the API
        logger_jira_release_notes.debug('Retrieving the Release Notes from the API')
        for release_item in self.release:
            print('Release Note:', release_item)
            ascii_data_list.append('== Release Note: {}'.format(release_item))
            release_name_url = '{}'.format(self.release_name)
            release_url = '{}'.format(release_item)
            # Deciding Ascending/Descending order of the results
            logger_jira_release_notes.debug('Deciding Ascending/Descending order of the results')
            ascending_order = ' ORDER BY priority ASC'
            descending_order = ' ORDER BY priority DESC'
            order_definition = ''
            if self.order is 'a' or self.order is 'A':
                order_definition = ascending_order
            elif self.order is 'd' or self.order is 'D':
                order_definition = descending_order
            elif self.order is None:
                order_definition = ''

            logger_jira_release_notes.debug('URL of Connection')
            url = '{}rest/api/latest/search?jql="{}"="{}"{}'.format(options['server'],
                                                                    release_name_url,
                                                                    release_url,
                                                                    order_definition)

            # Data retrieved from the REST API
            logger_jira_release_notes.debug('Data retrieved from the REST API')
            r = requests.get(url, auth=options['authentication'])
            data = r.json()

            keys_list = data.keys()
            logger_jira_release_notes.debug(str(keys_list))

            for key in keys_list:
                if key == 'errorMessages':
                    logger_jira_release_notes.warning(
                        'This Field does not exist or you do not have permission to view it.')
                    ascii_data_list.append('* This Field does not exist or you do not have permission to view it.')
                    # raise Exception('This Field does not exist or you do not have permission to view it.')
                elif key == 'issues':
                    logger_jira_release_notes.info('Total Jiras found based on that release: {}'.format(data.get('total')))
                    ascii_data_list.append('* Total Jiras: {}'.format(data.get('total')))
                    print()
                    jiras = data['issues']
                    for issue in jiras:
                        logger_jira_release_notes.info('Collecting Key: {}'.format(issue.get('key')))
                        print('Collecting Key:', issue.get('key'))
                        # print('taking selected fields..')
                        ascii_data_list.append('==== {}'.format(issue.get('key')))
                        issue_fields = issue.get('fields')
                        ascii_data_list.append('* Summary: {}'.format(issue_fields.get('summary'),
                                                                      'No summary is provided here.'))
                        ascii_data_list.append('* Description:')
                        ascii_data_list.append('============================')
                        ascii_data_list.append('{}'.format(issue_fields.get('description',
                                                                            'No description is provided here.')))
                        ascii_data_list.append('============================')
                        # print()
            print()
            print('----------------------------')
            print()

        return ascii_data_list


class IssueDataRetrieverJira:
    def __init__(self, issue, terms, cf_name, cf_id, debug_level):
        self.issue = issue
        self.terms = terms
        self.cf_name = cf_name
        self.cf_id = cf_id
        self.debug_level = debug_level

    def get_data(self):
        # AsciiDoc data collection list
        ascii_data_list = []

        connection = Connector(debug_level=self.debug_level)
        options = connection.connection_jira()

        print('Connection:')
        print(options)
        url = '{}rest/api/latest/issue/{}'.format(options['server'], self.issue)
        # data retrieving from the REST API
        r = requests.get(url, auth=options['authentication'])

        # layer 1
        data_layer_1 = r.json()
        if data_layer_1:
            return data_layer_1
        else:
            return None

    # GETTING BASIC ISSUE DATA
    def get_basic_issue_data(self, data):
        logging_jira_issue_basic_data = LoggerSetup(name='jira_issue_basic_data_logger',
                                                    log_file='log/jira_issue_basic_data_function_requester.log',
                                                    level=self.debug_level)
        logger_jira_issue_basic_data = logging_jira_issue_basic_data.setup_logger()
        logger_jira_issue_basic_data.debug('entered JIRA basic issue information function')

        ascii_data_list = []

        # Issue header
        ascii_data_list.append('== Issue: {}'.format(self.issue))

        if data is not None:

            # READ FIELDS FROM CONF or USER INPUT
            search_list_output = []
            search_list = ConfigData('jira_fields', self.terms)
            search_list_output = search_list.get_config_search_data()
            logger_jira_issue_basic_data.debug('Search list: {}'.format(str(search_list_output)))

            # pprint(data_layer_1)
            data_keys_layer_1 = data.keys()
            # print(data_keys_layer_1)
            print()
            print()
            # layer 1
            print('Fetching the data from the JIRA API.')
            for key in search_list_output:
                if key in data_keys_layer_1:
                    print(key + ': ' + data.get(key))

            # layer 2
            print('Inserting into Issue data.')
            # print(data.keys())
            if 'errorMessages' in data.keys():
                for item in data['errorMessages']:
                    ascii_data_list.append('* {}'.format(item))
                    print('\t' + item)
            else:
                data_layer_2 = data['fields']
                # pprint(data_layer_2)
                data_keys_layer_2 = data_layer_2.keys()
                print(data_keys_layer_2)
                print()
                print()
                print('Fetching the data - Layer 2:')

                # read fields from configuration
                # JIRA search terms configuration file reading
                search_terms_config = configparser.ConfigParser()
                search_terms_config.read('{}/conf/search_terms.conf'.format(configuration_directory_path))
                custom_field_names = search_terms_config['jira_custom_fields']['name']
                custom_field_names_list = custom_field_names.split(',')

                custom_field_ids = search_terms_config['jira_custom_fields']['id']
                custom_field_ids_list = custom_field_ids.split(',')
                for index, id in enumerate(custom_field_ids_list):
                    custom_field_ids_list[index] = 'customfield_' + str(id)
                print(custom_field_ids_list)

                if len(custom_field_names_list) == len(custom_field_ids_list):
                    custom_fields_list = list(zip(custom_field_names_list, custom_field_ids_list))
                    print(custom_fields_list)
                    search_list_output = search_list_output + custom_fields_list
                print(search_list_output)

                for key in search_list_output:
                    if type(key) is tuple:
                        name = key[0]
                        key = key[1]
                    else:
                        key = key
                    if key in data_keys_layer_2:
                        if type(data_layer_2.get(key)) is str:
                            print(key + ': ' + data_layer_2.get(key))
                            ascii_data_list.append('* {}: {}'.format(key, data_layer_2.get(key)))
                        if type(data_layer_2.get(key)) is list:
                            print(key + ':')
                            ascii_data_list.append('* {}:'.format(key))
                            keys_list = data_layer_2.get(key)
                            counter_dict_list = 1
                            for key_list_item in keys_list:
                                if type(key_list_item) is dict:
                                    dict_list_item_keys = key_list_item.keys()
                                    # print(dict_list_item_keys)
                                    print('\tItem {}'.format(counter_dict_list))
                                    ascii_data_list.append('** Item {}'.format(counter_dict_list))
                                    for key_item in dict_list_item_keys:
                                        if key_item != 'self':
                                            print('\t\t {}: '.format(key_item) + str(key_list_item.get(key_item)))
                                            ascii_data_list.append('*** {}: {}'.format(key_item, key_list_item.get(key_item)))
                                    counter_dict_list += 1
                                else:
                                    print('\t' + str(key_list_item))
                        if type(data_layer_2.get(key)) is dict:
                            if key.startswith('customfield_'):
                                print(name + ':')
                                ascii_data_list.append('* {}:'.format(name))
                            else:
                                print(key + ':')
                                ascii_data_list.append('* {}:'.format(key))
                            dict_item = data_layer_2.get(key)
                            dict_item_keys_list = dict_item.keys()
                            for item_key in dict_item_keys_list:
                                if item_key != 'self' and item_key != 'iconUrl' and item_key != 'avatarUrls':
                                    if type(dict_item.get(item_key)) is dict:
                                        print('\t' + item_key + ':')
                                        ascii_data_list.append('** {}:'.format(item_key))
                                        data_dict = dict_item.get(item_key)
                                        data_dict_keys = data_dict.keys()
                                        for data_key in data_dict_keys:
                                            if data_key != 'self' and data_key != 'iconUrl' and data_key != 'avatarUrls':
                                                print('\t\t\t' + data_key + ': ' + data_dict.get(data_key))
                                                ascii_data_list.append('*** {}: {}'.format(data_key, data_dict.get(data_key)))
                                    else:
                                        print('\t' + item_key + ': {}'.format(dict_item.get(item_key)))
                                        ascii_data_list.append('** {}: {}'.format(item_key, dict_item.get(item_key)))
                    print()
        else:
            ascii_data_list.append('* There is no data available for that issue or check the issue name.')

        return ascii_data_list

    # COMMENTS
    def getting_comments_data(self, data):
        logging_jira_issue_basic_data = LoggerSetup(name='jira_issue_basic_data_logger',
                                                    log_file='log/jira_issue_basic_data_function_requester.log',
                                                    level=self.debug_level)
        logger_jira_issue_basic_data = logging_jira_issue_basic_data.setup_logger()
        logger_jira_issue_basic_data.debug('entered JIRA issue comments function')

        ascii_data_list = []

        # Issue header
        ascii_data_list.append('== Issue: {}'.format(self.issue))
        if data is not None:
            # READ FIELDS FROM CONF or USER INPUT
            search_list = ConfigData('jira_comments', self.terms)
            search_list_output = search_list.get_config_search_data()

            # layer 2
            print('Inserting into Issue Comments data.')
            # print(data.keys())
            if 'errorMessages' in data.keys():
                for item in data['errorMessages']:
                    ascii_data_list.append('* {}'.format(item))
                    print('\t' + item)
            else:
                # data 2 layer for comments
                data_layer_2_comments = data['fields']['comment']['comments']
                if len(data_layer_2_comments) > 0:
                    counter_comments = 1
                    for comment_item in data_layer_2_comments:
                        print(('Comment {}:'.format(counter_comments)))
                        ascii_data_list.append('=== Comment {}:'.format(counter_comments))
                        comment_keys_list = comment_item.keys()
                        # print(comment_keys_list)
                        # for key in search_list_output:
                        #     if key in comment_keys_list:
                        #         if type(comment_item[key]) is str:
                        #             print('\t' + key + ': ' + str(comment_item[key]))
                        list_of_fields = []
                        for key in comment_keys_list:
                            if key != 'updateAuthor':
                                # print('\t' + str(type(comment_item[key])))
                                if type(comment_item[key]) is str or type(comment_item[key]) is int or type(comment_item[key]) is bool:
                                    if key in search_list_output:
                                        # print('\t\t' + key + ': ' + str(comment_item[key]))
                                        list_of_fields.append('* {}: {}'.format(key, str(comment_item[key])))
                                if type(comment_item[key]) is dict:
                                    nested_comment_item = comment_item[key]
                                    nested_comment_item_keys = nested_comment_item.keys()
                                    for nested_key in nested_comment_item_keys:
                                        if nested_key in search_list_output:
                                            list_of_fields.append('* {}: {}'.format(nested_key, str(nested_comment_item[nested_key])))
                        final_list_of_fields = list(dict.fromkeys(list_of_fields))
                        for item in final_list_of_fields:
                            ascii_data_list.append(item)

                        for item in final_list_of_fields:
                            print('\t' + item)

                        counter_comments += 1

            return ascii_data_list
        else:
            ascii_data_list.append('* There is no data available for that issue or check the issue name.')

        return ascii_data_list


