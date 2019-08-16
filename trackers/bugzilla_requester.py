import logging
import requests
from pprint import pprint
import configparser
import os

from conf.confparse import BugzillaReadConfigurationApiKey

from logger_creation import LoggerSetup

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
# print('Path rlgen is found:')
working_directory_path = directories_list[1:]
configuration_directory_path = '/' + '/'.join(working_directory_path)
# print(configuration_directory_path)


class TargetReleaseBugzilla:
    def __init__(self, releases, terms, debug_level):
        self.releases = releases
        self.terms = terms
        self.debug_level = debug_level

    # TARGET RELEASE FUNCTION
    def getting_target_release_notes(self):
        # logger creation
        logging_bugzilla_target_releases = LoggerSetup(name='bugzilla_target_releases',
                                                       log_file='log/bugzilla_target_releases.log',
                                                       level=self.debug_level)
        logger_bugzilla_tr = logging_bugzilla_target_releases.setup_logger()
        logger_bugzilla_tr.info('Entered Bugzilla - Release Notes Function')

        # release notes defined in user input
        retrieve = 'target_release_notes'
        print('Releases defined by the user input:', self.releases)
        logger_bugzilla_tr.debug('Releases defined by the user inputs: {}'.format(str(self.releases)))

        ascii_target_release_list = []

        # Entering releases field to collect information.
        logger_bugzilla_tr.info('Entering releases field to collect information.')
        for release in self.releases:
            print('Release:', release)
            logger_bugzilla_tr.info('Release: {}'.format(release))
            print('------------------')
            logger_bugzilla_tr.info('------------------')
            ascii_target_release_list.append('== Release: {}'.format(release))

            # Retrieving Bugzilla API Authentication Key from the configuration file.
            logger_bugzilla_tr.debug('Retrieving Bugzilla API Authentication Key from the configuration file.')
            api_connection = BugzillaReadConfigurationApiKey()
            api_key_auth = api_connection.key_auth()['api_key_auth']
            api_key = ''
            if api_key_auth is True:
                api_key_reason = api_connection.key_auth()['api_key_reason']
                logger_bugzilla_tr.debug(api_key_reason)
                api_key = api_connection.key_auth()['api_key']
            else:
                api_key_reason = api_connection.key_auth()['api_key_reason']
                logger_bugzilla_tr.warning(api_key_reason)
                # raise Exception(api_key_reason)

            # Retrieving the company link from the conf file to insert it later into the API request
            logger_bugzilla_tr.info('Retrieving the company link from the conf file to insert it later '
                                    'into the API request.')
            config = configparser.ConfigParser()
            config.read('{}config.conf'.format(conf_path))
            # read company data from configuration file
            company = config['bugzilla_basic_auth']['company']
            logger_bugzilla_tr.debug('Company link: {}'.format(company))

            # read fields from configuration
            # Bugzilla search terms configuration file reading
            logger_bugzilla_tr.info('Retrieving Bugzilla search terms (fields) from the configuration file.')
            search_terms_config = configparser.ConfigParser()
            search_terms_config.read('{}/conf/search_terms.conf'.format(configuration_directory_path))
            search_list_conf_input = search_terms_config['bugzilla_target_release']['search_list']
            search_list_conf_input = search_list_conf_input.replace(', ', ',')
            search_list_conf_input = search_list_conf_input.replace(' ,', ',')
            search_list_conf_input = search_list_conf_input.replace(' , ', ',')
            search_list_conf_input = search_list_conf_input.split(',')
            print('Fields to search from conf file:', search_list_conf_input)
            logger_bugzilla_tr.debug('Fields from conf file: {}'.format(str(search_list_conf_input)))
            print('Fields to search from terminal:', self.terms)
            logger_bugzilla_tr.debug('Fields from user input in terminal: {}'.format(str(self.terms)))
            if self.terms is not None:
                search_list_output = search_list_conf_input + self.terms
            elif self.terms is None:
                search_list_output = search_list_conf_input
            print('Final fields to search (conf file + terminal):', str(search_list_output))
            logger_bugzilla_tr.info('Final fields to search (conf file + terminal): {}'.format(str(search_list_output)))

            url = 'https://bugzilla.{}/rest/bug?target_release={}'.format(company, release)
            # Connecting to Bugzilla API
            logger_bugzilla_tr.info('Connecting to Bugzilla API')
            logger_bugzilla_tr.debug('URL: {}'.format(url))
            logger_bugzilla_tr.debug('API Key: {}'.format(api_key))
            r = requests.get(url, params={'api_key': '{}'.format(api_key)})
            print('Retrieving the Target Release data from Bugzilla..')
            logger_bugzilla_tr.info('Retrieving the Target Release data from Bugzilla..')
            data = r.json()
            # pprint(data)
            print('The API response was successful.')
            logger_bugzilla_tr.info('The API response was successful.')

            if 'error' in data.keys():
                logger_bugzilla_tr.warning('Error in fetching the queried data.')
                for key in search_list_output:
                    if key in data.keys():
                        ascii_target_release_list.append('{}: {}'.format(key, data.get(key)))
                        logger_bugzilla_tr.warning('{}: {}'.format(key, data.get(key)))
            elif 'bugs' in data.keys():
                data_release_bugs = data.get('bugs')
                if len(data_release_bugs) > 0:
                    logger_bugzilla_tr.debug('The data retrieval related to the query is successful.')
                    # pprint(data_release_bugs)
                    for bug in data_release_bugs:
                        bug_keys_list = bug.keys()
                        # print(bug_keys_list)
                        # print(len(bug_keys_list))
                        keys_to_retrieve = []
                        if len(search_list_output) > 0:
                            for key in search_list_output:
                                if key in bug_keys_list:
                                    keys_to_retrieve.append(key)
                                # else:
                                #     print('Some of the keys you entered do not match in the fields of the issue.')
                        else:
                            keys_to_retrieve = bug_keys_list
                        # retrieving keys
                        ascii_target_release_list.append('')
                        ascii_target_release_list.append('=== Bug: {}'.format(bug.get('id')))
                        print('Bug:', bug.get('id'))
                        logger_bugzilla_tr.info('Collecting information for the Bug: {}'.format(bug.get('id')))
                        for key in keys_to_retrieve:
                            if type(bug.get(key)) is str or type(bug.get(key)) is bool or type(bug.get(key)) is int or type(bug.get(key)) is None:
                                if bug.get(key) is '':
                                    print(key + ': ' + 'Nothing related to {} is now available.'.format(key))
                                    ascii_target_release_list.append('* ' + key + ': ' + 'Nothing related to {} is now available.'.format(key))
                                    logger_bugzilla_tr.debug('{}: Nothing related to {} is now available.'.format(key, key))
                                else:
                                    print(key + ': ' + str(bug.get(key, 'Nothing related to {} is now available.'.format(key))))
                                    ascii_target_release_list.append('* ' + key + ': ' + str(bug.get(key, 'Nothing related to {} is now available.'.format(key))))
                                    logger_bugzilla_tr.debug(str(key) + ': ' + str(bug.get(key, 'Nothing related to {} is now available.'.format(key))))
                            if type(bug.get(key)) is list:
                                print(key + ':')
                                ascii_target_release_list.append('* {}:'.format(key))
                                logger_bugzilla_tr.info('Collecting listed Key: {}'.format(key))
                                counter__dictionary_items = 1
                                for list_item in bug.get(key):
                                    if type(list_item) is dict:
                                        print('\tItem: {}'.format(counter__dictionary_items))
                                        ascii_target_release_list.append('** Item: {}'.format(counter__dictionary_items))
                                        logger_bugzilla_tr.debug('Item: {}'.format(counter__dictionary_items))
                                        dictionary_keys = list_item.keys()
                                        for dictionary_key in dictionary_keys:
                                            print('\t\t' + dictionary_key + ': ' + str(list_item.get(dictionary_key)))
                                            ascii_target_release_list.append('*** ' + dictionary_key + ': ' + str(list_item.get(dictionary_key)))
                                            logger_bugzilla_tr.debug(str(dictionary_key) + ': ' + str(list_item.get(dictionary_key)))
                                        counter__dictionary_items += 1
                                    else:
                                        print('\t', list_item)
                                        ascii_target_release_list.append('** {}'.format(list_item))
                                        logger_bugzilla_tr.debug(str(list_item))
                        print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
                        logger_bugzilla_tr.debug('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
                else:
                    ascii_target_release_list.append('* There is no Target Release with that name or there are no '
                                                     'issues related to that Target Release.')
                    logger_bugzilla_tr.info('There is no Target Release with that name or there are no issues related '
                                            'to that Target Release.')
                    logger_bugzilla_tr.warning('Error on querying the data. The username is not right or there are no '
                                               'assigned bugs yet to that username.')
                    print('\t There is no Target Release with that name or there are no issues related to that Target '
                          'Release.')

            ascii_target_release_list.append('')
        # print AsciiDoc data
        # for item in ascii_target_release_list:
        #     print(item)
        return ascii_target_release_list


""" CLASS FOR RETRIEVING THE DATA FROM BUGZILLA API"""


class DataRetriever:
    def __init__(self, bug_id, terms, user, debug_level):
        self.bug_id = bug_id
        self.terms = terms
        self.user = user
        self.debug_level = debug_level

    # BUG INFORMATION
    def getting_bug_info(self):
        logging_bugzilla_func = LoggerSetup(name='bugzilla_exec_function',
                                            log_file='log/bugzilla_exec_function.log',
                                            level=self.debug_level)
        logger_bugzilla_func = logging_bugzilla_func.setup_logger()
        logger_bugzilla_func.info('Entered Bugzilla - Bug Information Function')
        retrieve = 'bug_info'
        ascii_bug_info_list = []
        print('Bug ID:', self.bug_id)
        logger_bugzilla_func.info('Bug: {}'.format(self.bug_id))
        print('------------------')
        logger_bugzilla_func.info('------------------')
        ascii_bug_info_list.append('== Bug ID: {}'.format(self.bug_id))

        # Retrieving Bugzilla API Authentication Key from the configuration file.
        logger_bugzilla_func.debug('Retrieving Bugzilla API Authentication Key from the configuration file.')
        api_connection = BugzillaReadConfigurationApiKey()
        api_key_auth = api_connection.key_auth()['api_key_auth']
        api_key = ''
        if api_key_auth is True:
            api_key_reason = api_connection.key_auth()['api_key_reason']
            logger_bugzilla_func.debug(api_key_reason)
            api_key = api_connection.key_auth()['api_key']
        else:
            api_key_reason = api_connection.key_auth()['api_key_reason']
            logger_bugzilla_func.warning(api_key_reason)
            # raise Exception(api_key_reason)

        # Retrieving the company link from the conf file to insert it later into the API request
        logger_bugzilla_func.info('Retrieving the company link from the conf file to insert it later '
                                  'into the API request.')
        config = configparser.ConfigParser()
        config.read('{}config.conf'.format(conf_path))
        # read company data from configuration file
        company = config['bugzilla_basic_auth']['company']
        logger_bugzilla_func.debug('Company link: {}'.format(company))

        # read fields from configuration
        # Bugzilla search terms configuration file reading
        logger_bugzilla_func.info('Retrieving Bugzilla search terms (fields) from the configuration file.')
        search_terms_config = configparser.ConfigParser()
        search_terms_config.read('{}/conf/search_terms.conf'.format(configuration_directory_path))
        search_list_conf_input = search_terms_config['bugzilla_bug']['search_list']
        search_list_conf_input = search_list_conf_input.replace(', ', ',')
        search_list_conf_input = search_list_conf_input.replace(' ,', ',')
        search_list_conf_input = search_list_conf_input.replace(' , ', ',')
        search_list_conf_input = search_list_conf_input.split(',')
        print('Fields to search from conf file:', search_list_conf_input)
        logger_bugzilla_func.debug('Fields from conf file: {}'.format(str(search_list_conf_input)))
        print('Fields to search from terminal:', self.terms)
        logger_bugzilla_func.debug('Fields from user input in terminal: {}'.format(str(self.terms)))
        if self.terms is not None:
            search_list_output = search_list_conf_input + self.terms
        elif self.terms is None:
            search_list_output = search_list_conf_input
        print('Final fields to search (conf file + terminal):', str(search_list_output))
        logger_bugzilla_func.info('Final fields to search (conf file + terminal): {}'.format(str(search_list_output)))

        # Connecting to Bugzilla API
        logger_bugzilla_func.info('Connecting to Bugzilla API')
        logger_bugzilla_func.debug('API Key: {}'.format(api_key))

        # request connection
        r = requests.get('https://bugzilla.{}/rest/bug/'.format(company), params={'ids': '{}'.format(self.bug_id),
                                                                                  'api_key': '{}'.format(api_key)})
        print('Retrieving the Bug Information data from Bugzilla..')
        logger_bugzilla_func.info('Retrieving the Target Release data from Bugzilla..')
        data = r.json()
        print('The API response was successful.')
        logger_bugzilla_func.info('The API response was successful.')

        if 'error' in data.keys():
            data_output = [data]
            logger_bugzilla_func.warning('Error on querying the data.')
            logger_bugzilla_func.warning(str(data['message']))
        elif 'bugs' in data.keys():
            data_output = data.get('bugs')
            logger_bugzilla_func.debug('The data retrieval related to the query is successful.')
            # pprint(data_output)
        else:
            data_output = None
            logger_bugzilla_func.warning('Error on querying the data.')

        # Show in AsciiDoc the fields to search for in Bugzilla API JSON response
        # ascii_bug_info_list.append('* Search Fields: {}'.format(search_list_output))
        return {'retrieve': retrieve,
                'data_output': data_output,
                'search_list_output': search_list_output,
                'ascii_bug_info_list': ascii_bug_info_list}

    # USER ASSIGNED BUGS
    def getting_user_assigned_bugs(self):
        logging_bugzilla_func = LoggerSetup(name='bugzilla_exec_function',
                                            log_file='log/bugzilla_exec_function.log',
                                            level=self.debug_level)
        logger_bugzilla_func = logging_bugzilla_func.setup_logger()
        logger_bugzilla_func.info('Entered Bugzilla - User Assigned Bugs Function')
        retrieve = 'user_assigned_bugs'
        ascii_user_assigned_bugs_list = []
        print('User:', self.user)
        logger_bugzilla_func.info('User: {}'.format(self.user))
        print('------------------')
        logger_bugzilla_func.info('------------------')
        ascii_user_assigned_bugs_list.append('== User: {}'.format(self.user))

        # Retrieving Bugzilla API Authentication Key from the configuration file.
        logger_bugzilla_func.debug('Retrieving Bugzilla API Authentication Key from the configuration file.')
        api_connection = BugzillaReadConfigurationApiKey()
        api_key_auth = api_connection.key_auth()['api_key_auth']
        api_key = ''
        if api_key_auth is True:
            api_key_reason = api_connection.key_auth()['api_key_reason']
            logger_bugzilla_func.debug(api_key_reason)
            api_key = api_connection.key_auth()['api_key']
        else:
            api_key_reason = api_connection.key_auth()['api_key_reason']
            logger_bugzilla_func.warning(api_key_reason)
            # raise Exception(api_key_reason)

        # Retrieving the company link from the conf file to insert it later into the API request
        logger_bugzilla_func.info('Retrieving the company link from the conf file to insert it later '
                                  'into the API request.')
        config = configparser.ConfigParser()
        config.read('{}config.conf'.format(conf_path))
        company = config['bugzilla_basic_auth']['company']

        # read fields from configuration
        # Bugzilla search terms configuration file reading
        logger_bugzilla_func.info('Retrieving Bugzilla search terms (fields) from the configuration file.')
        search_terms_config = configparser.ConfigParser()
        search_terms_config.read('{}/conf/search_terms.conf'.format(configuration_directory_path))
        search_list_conf_input = search_terms_config['bugzilla_user_assigned_bugs']['search_list']
        search_list_conf_input = search_list_conf_input.replace(', ', ',')
        search_list_conf_input = search_list_conf_input.replace(' ,', ',')
        search_list_conf_input = search_list_conf_input.replace(' , ', ',')
        search_list_conf_input = search_list_conf_input.split(',')
        print('Fields to search from conf file:', search_list_conf_input)
        logger_bugzilla_func.debug('Fields from conf file: {}'.format(str(search_list_conf_input)))
        print('Fields to search from terminal:', self.terms)
        logger_bugzilla_func.debug('Fields from user input in terminal: {}'.format(str(self.terms)))
        if self.terms is not None:
            search_list_output = search_list_conf_input + self.terms
        elif self.terms is None:
            search_list_output = search_list_conf_input
        logger_bugzilla_func.info('Final fields to search (conf file + terminal): {}'.format(str(search_list_output)))

        # Connecting to Bugzilla API
        logger_bugzilla_func.info('Connecting to Bugzilla API')
        logger_bugzilla_func.debug('API Key: {}'.format(api_key))

        # request connection
        r = requests.get('https://bugzilla.{}/rest/bug?assigned_to={}'.format(company, self.user),
                         params={'api_key': '{}'.format(api_key)})
        print('Retrieving the User Assigned Bugs data from Bugzilla..')
        logger_bugzilla_func.info('Retrieving the Target Release data from Bugzilla..')
        data = r.json()
        print('The API response was successful.')
        logger_bugzilla_func.info('The API response was successful.')

        if 'bugs' in data.keys() and len(data['bugs']) > 0:
            data_output = data.get('bugs')
            logger_bugzilla_func.debug('The data retrieval related to the query is successful.')
        else:
            data_output = None
            logger_bugzilla_func.warning('Error on querying the data. The username is not right or there are no '
                                         'assigned bugs yet to that username.')

        # Show in AsciiDoc the fields to search for in Bugzilla API JSON response
        # ascii_user_assigned_bugs_list.append('* Search Fields: {}'.format(search_list_output))
        return {'retrieve': retrieve,
                'data_output': data_output,
                'search_list_output': search_list_output,
                'ascii_user_assigned_bugs_list': ascii_user_assigned_bugs_list}

    # USER INFORMATION
    def getting_user_info(self):
        logging_bugzilla_func = LoggerSetup(name='bugzilla_exec_function',
                                            log_file='log/bugzilla_exec_function.log',
                                            level=self.debug_level)
        logger_bugzilla_func = logging_bugzilla_func.setup_logger()
        logger_bugzilla_func.info('Entered Bugzilla - User Information Function')
        retrieve = 'user_info'
        ascii_user_info_list = []
        print('User:', self.user)
        logger_bugzilla_func.info('User: {}'.format(self.user))
        print('------------------')
        logger_bugzilla_func.info('------------------')
        ascii_user_info_list.append('== User: {}'.format(self.user))
        api_connection = BugzillaReadConfigurationApiKey()
        api_key_auth = api_connection.key_auth()['api_key_auth']
        api_key = ''
        if api_key_auth is True:
            api_key_reason = api_connection.key_auth()['api_key_reason']
            logger_bugzilla_func.debug(api_key_reason)
            api_key = api_connection.key_auth()['api_key']
        else:
            api_key_reason = api_connection.key_auth()['api_key_reason']
            logger_bugzilla_func.warning(api_key_reason)
            # raise Exception(api_key_reason)

        # Retrieving Bugzilla API Authentication Key from the configuration file.
        logger_bugzilla_func.debug('Retrieving Bugzilla API Authentication Key from the configuration file.')
        config = configparser.ConfigParser()
        config.read('{}config.conf'.format(conf_path))
        company = config['bugzilla_basic_auth']['company']

        # read fields from configuration
        # Bugzilla search terms configuration file reading
        logger_bugzilla_func.info('Retrieving Bugzilla search terms (fields) from the configuration file.')
        search_terms_config = configparser.ConfigParser()
        search_terms_config.read('{}/conf/search_terms.conf'.format(configuration_directory_path))
        search_list_conf_input = search_terms_config['bugzilla_user_info']['search_list']
        search_list_conf_input = search_list_conf_input.replace(', ', ',')
        search_list_conf_input = search_list_conf_input.replace(' ,', ',')
        search_list_conf_input = search_list_conf_input.replace(' , ', ',')
        search_list_conf_input = search_list_conf_input.split(',')
        print('Fields to search from conf file:', search_list_conf_input)
        logger_bugzilla_func.debug('Fields from conf file: {}'.format(str(search_list_conf_input)))
        print('Fields to search from terminal:', self.terms)
        logger_bugzilla_func.debug('Fields from user input in terminal: {}'.format(str(self.terms)))
        if self.terms is not None:
            search_list_output = search_list_conf_input + self.terms
        elif self.terms is None:
            search_list_output = search_list_conf_input
        logger_bugzilla_func.info('Final fields to search (conf file + terminal): {}'.format(str(search_list_output)))

        # Connecting to Bugzilla API
        logger_bugzilla_func.info('Connecting to Bugzilla API')
        logger_bugzilla_func.debug('API Key: {}'.format(api_key))

        url = 'https://bugzilla.{}/rest/user?names={}'.format(company, self.user)
        logger_bugzilla_func.debug('URL: {}'.format(url))

        r = requests.get(url, params={'api_key': '{}'.format(api_key)})
        print('Retrieving the User Assigned Bugs data from Bugzilla..')
        logger_bugzilla_func.info('Retrieving the Target Release data from Bugzilla..')
        data = r.json()
        print('Successfully fetched the data.')
        logger_bugzilla_func.info('Successfully fetched the data.')

        if 'error' in data.keys():
            data_output = [data]
            logger_bugzilla_func.warning('Error on querying the data.')
            logger_bugzilla_func.warning(str(data['message']))
        elif 'users' in data.keys():
            data_output = data.get('users')
            logger_bugzilla_func.debug('The data retrieval related to the query is successful.')
        else:
            data_output = None
            logger_bugzilla_func.warning('Error on querying the data.')

        # Show in AsciiDoc the fields to search for in Bugzilla API JSON response
        # ascii_user_info_list.append('* Search Fields: {}'.format(search_list_output))
        return {'retrieve': retrieve,
                'data_output': data_output,
                'search_list_output': search_list_output,
                'ascii_user_info_list': ascii_user_info_list}

    # BUG COMMENTS
    def getting_bug_comments(self):
        logging_bugzilla_func = LoggerSetup(name='bugzilla_exec_function',
                                            log_file='log/bugzilla_exec_function.log',
                                            level=self.debug_level)
        logger_bugzilla_func = logging_bugzilla_func.setup_logger()
        logger_bugzilla_func.debug('Entered Bugzilla - Bug Comments Function')
        retrieve = 'bug_comments'
        ascii_bug_comments_list = []
        print('Bug ID:', self.bug_id)
        logger_bugzilla_func.info('Bug: {}'.format(self.bug_id))
        print('------------------')
        logger_bugzilla_func.info('------------------')
        ascii_bug_comments_list.append('== Bug ID: {}'.format(self.bug_id))

        # Retrieving Bugzilla API Authentication Key from the configuration file.
        logger_bugzilla_func.debug('Retrieving Bugzilla API Authentication Key from the configuration file.')
        api_connection = BugzillaReadConfigurationApiKey()
        api_key_auth = api_connection.key_auth()['api_key_auth']
        api_key = ''
        if api_key_auth is True:
            api_key_reason = api_connection.key_auth()['api_key_reason']
            logger_bugzilla_func.debug(api_key_reason)
            api_key = api_connection.key_auth()['api_key']
        else:
            api_key_reason = api_connection.key_auth()['api_key_reason']
            logger_bugzilla_func.warning(api_key_reason)
            # raise Exception(api_key_reason)

        # Retrieving the company link from the conf file to insert it later into the API request
        logger_bugzilla_func.info('Retrieving the company link from the conf file to insert it later '
                                  'into the API request.')
        config = configparser.ConfigParser()
        # read company data from configuration file
        config.read('{}config.conf'.format(conf_path))
        company = config['bugzilla_basic_auth']['company']

        # read fields from configuration
        # Bugzilla search terms configuration file reading
        logger_bugzilla_func.info('Retrieving Bugzilla search terms (fields) from the configuration file.')
        search_terms_config = configparser.ConfigParser()
        search_terms_config.read('{}/conf/search_terms.conf'.format(configuration_directory_path))
        search_list_conf_input = search_terms_config['bugzilla_comments']['search_list']
        search_list_conf_input = search_list_conf_input.replace(', ', ',')
        search_list_conf_input = search_list_conf_input.replace(' ,', ',')
        search_list_conf_input = search_list_conf_input.replace(' , ', ',')
        search_list_conf_input = search_list_conf_input.split(',')
        print('Fields to search from conf file:', search_list_conf_input)
        logger_bugzilla_func.debug('Fields from conf file: {}'.format(str(search_list_conf_input)))
        print('Fields to search from terminal:', self.terms)
        logger_bugzilla_func.debug('Fields from user input in terminal: {}'.format(str(self.terms)))
        if self.terms is not None:
            search_list_output = search_list_conf_input + self.terms
        elif self.terms is None:
            search_list_output = search_list_conf_input
        print('Final fields to search (conf file + terminal):', str(search_list_output))
        logger_bugzilla_func.info('Final fields to search (conf file + terminal): {}'.format(str(search_list_output)))

        # Connecting to Bugzilla API
        logger_bugzilla_func.info('Connecting to Bugzilla API')
        logger_bugzilla_func.debug('API Key: {}'.format(api_key))
        url = 'https://bugzilla.{}/rest/bug/{}/comment'.format(company, self.bug_id)
        logger_bugzilla_func.debug('URL: {}'.format(url))
        # u = url + "?token={}".format(api_key)
        # request connection
        r = requests.get(url, params={'api_key': '{}'.format(api_key)})

        print('Retrieving the Bug Information data from Bugzilla..')
        logger_bugzilla_func.info('Retrieving the Target Release data from Bugzilla..')
        data = r.json()
        print('The API response was successfully.')
        logger_bugzilla_func.info('The API response was successfully.')

        # if 'error' in data.keys():
        #     data_output = data
        if 'error' in data.keys():
            data_output = data
            logger_bugzilla_func.warning('Error on querying the data.')
            logger_bugzilla_func.warning(str(data['message']))
        elif 'bugs' in data.keys():
            data_output = data.get('bugs')
            logger_bugzilla_func.debug('The data retrieval related to the query is successful.')
        else:
            data_output = None
            logger_bugzilla_func.warning('Error on querying the data.')

        # Show in AsciiDoc the fields to search for in Bugzilla API JSON response
        # ascii_bug_comments_list.append('* Search Fields: {}'.format(search_list_output))
        return {'retrieve': retrieve,
                'data_output': data_output,
                'search_list_output': search_list_output,
                'ascii_bug_comments_list': ascii_bug_comments_list}

    # BUG HISTORY
    def getting_bug_history(self):
        logging_bugzilla_func = LoggerSetup(name='bugzilla_exec_function',
                                            log_file='log/bugzilla_exec_function.log',
                                            level=self.debug_level)
        logger_bugzilla_func = logging_bugzilla_func.setup_logger()
        logger_bugzilla_func.debug('Entered Bugzilla - Bug History Function')
        retrieve = 'bug_history'
        ascii_bug_history_list = []
        print('Bug ID:', self.bug_id)
        logger_bugzilla_func.info('Bug: {}'.format(self.bug_id))
        print('------------------')
        logger_bugzilla_func.info('------------------')
        ascii_bug_history_list.append('== Bug ID: {}'.format(self.bug_id))

        # Retrieving Bugzilla API Authentication Key from the configuration file.
        logger_bugzilla_func.debug('Retrieving Bugzilla API Authentication Key from the configuration file.')
        api_connection = BugzillaReadConfigurationApiKey()
        api_key_auth = api_connection.key_auth()['api_key_auth']
        api_key = ''
        if api_key_auth is True:
            api_key_reason = api_connection.key_auth()['api_key_reason']
            logger_bugzilla_func.debug(api_key_reason)
            api_key = api_connection.key_auth()['api_key']
        else:
            api_key_reason = api_connection.key_auth()['api_key_reason']
            logger_bugzilla_func.warning(api_key_reason)
            # raise Exception(api_key_reason)

        # Retrieving the company link from the conf file to insert it later into the API request
        logger_bugzilla_func.info('Retrieving the company link from the conf file to insert it later '
                                  'into the API request.')
        config = configparser.ConfigParser()
        config.read('{}config.conf'.format(conf_path))
        company = config['bugzilla_basic_auth']['company']

        # read fields from configuration
        # Bugzilla search terms configuration file reading
        logger_bugzilla_func.info('Retrieving Bugzilla search terms (fields) from the configuration file.')
        search_terms_config = configparser.ConfigParser()
        search_terms_config.read('{}/conf/search_terms.conf'.format(configuration_directory_path))
        search_list_conf_input = search_terms_config['bugzilla_bug_history']['search_list']
        search_list_conf_input = search_list_conf_input.replace(', ', ',')
        search_list_conf_input = search_list_conf_input.replace(' ,', ',')
        search_list_conf_input = search_list_conf_input.replace(' , ', ',')
        search_list_conf_input = search_list_conf_input.split(',')
        print('Fields to search from conf file:', search_list_conf_input)
        logger_bugzilla_func.debug('Fields from conf file: {}'.format(str(search_list_conf_input)))
        print('Fields to search from terminal:', self.terms)
        logger_bugzilla_func.debug('Fields from user input in terminal: {}'.format(str(self.terms)))
        if self.terms is not None:
            search_list_output = search_list_conf_input + self.terms
        elif self.terms is None:
            search_list_output = search_list_conf_input
        print('Final fields to search (conf file + terminal):', str(search_list_output))
        logger_bugzilla_func.info('Final fields to search (conf file + terminal): {}'.format(str(search_list_output)))

        # Connecting to Bugzilla API
        logger_bugzilla_func.info('Connecting to Bugzilla API')
        logger_bugzilla_func.debug('API Key: {}'.format(api_key))
        # url = 'https://bugzilla.mozilla.org/rest/bug/{}/history'.format(self.bug_id)
        url = 'https://bugzilla.{}/rest/bug/{}/history'.format(company, self.bug_id)
        logger_bugzilla_func.debug('URL: {}'.format(url))
        # u = url + "?token={}".format(api_key)
        # request connection
        r = requests.get(url, params={'api_key': '{}'.format(api_key)})

        print('Retrieving the Bug Information data from Bugzilla..')
        logger_bugzilla_func.info('Retrieving the Target Release data from Bugzilla..')
        data = r.json()
        print('The API response was successfully.')
        logger_bugzilla_func.info('The API response was successfully.')

        if 'error' in data.keys():
            data_output = [{'history': [data]}]
            logger_bugzilla_func.warning('Error on querying the data.')
            logger_bugzilla_func.warning(str(data['message']))
        elif 'bugs' in data.keys():
            data_output = data.get('bugs')
            logger_bugzilla_func.debug('The data retrieval related to the query is successful.')
        else:
            data_output = None
            logger_bugzilla_func.warning('Error on querying the data.')

        # Show in AsciiDoc the fields to search for in Bugzilla API JSON response
        # ascii_bug_history_list.append('* Search Fields: {}'.format(search_list_output))
        return {'retrieve': retrieve,
                'data_output': data_output,
                'search_list_output': search_list_output,
                'ascii_bug_history_list': ascii_bug_history_list}

    # MAIN FUNCTION FOR DATA RETRIEVING FROM EACH QUERY TO THE REST API
    def data_retriever(self, retrieval, data, search_list, ascii_doc_data):
        logging_bugzilla_main = LoggerSetup(name='bugzilla_data_retriever',
                                            log_file='log/bugzilla_data_retriever.log',
                                            level=self.debug_level)
        logger_bugzilla_main = logging_bugzilla_main.setup_logger()
        logger_bugzilla_main.debug('Entered Bugzilla - Data Retriever Function')
        ascii_doc_data_list = []
        logger_bugzilla_main.debug('Search List: {}'.format(str(search_list)))
        logger_bugzilla_main.debug('Search List Length: {}'.format(len(search_list)))
        ascii_doc_data_list.extend(ascii_doc_data)
        # BUG COMMENTS
        if retrieval is 'bug_comments' and self.bug_id in data.keys():
            logger_bugzilla_main.info('RETRIEVING BUG COMMENTS')
            comments = data[self.bug_id]['comments']
            counter_comment = 1
            for comment in comments:
                print('Comment: {}'.format(counter_comment))
                logger_bugzilla_main.info('Collecting Comment: {}'.format(counter_comment))
                ascii_doc_data_list.append('=== Comment {}'.format(counter_comment))
                comment_keys = comment.keys()
                print()
                if len(search_list) > 0:
                    for key in search_list:
                        if key in comment_keys:
                            if type(comment.get(key)) is str:
                                print(key + ':', comment.get(key, 'Nothing related to {} has been found.'.format(key)))
                                ascii_doc_data_list.append('* ' + key + ': ' + comment.get(
                                    key, 'Nothing related to {} has been found.'.format(key)))
                                logger_bugzilla_main.debug('>> string key: {}'.format(key))
                                print()
                            if type(comment.get(key)) is list:
                                print(key + ':')
                                ascii_doc_data_list.append('* {}'.format(key))
                                logger_bugzilla_main.debug('>> listed key: {}'.format(key))
                                key_list = comment.get(key)
                                for item_key in key_list:
                                    print('\t', item_key)
                                    ascii_doc_data_list.append('** {}'.format(item_key))
                                print()
                            if type(comment.get(key)) is int:
                                print(key + ':', str(comment.get(key, 'Nothing related to {} has been found.'.format(key))))
                                ascii_doc_data_list.append('* ' + key + ': ' + str(
                                    comment.get(key, 'Nothing related to {} is now available.'.format(key))))
                                logger_bugzilla_main.debug('>> int key: '.format(key))
                                print()
                            if type(comment.get(key)) is bool:
                                print(key + ':', str(comment.get(key, 'Nothing related to {} has been found.'.format(key))))
                                ascii_doc_data_list.append('* ' + key + ': ' + str(
                                    comment.get(key, 'Nothing related to {} is now available.'.format(key))))
                                logger_bugzilla_main.debug('>> boolean key: {}'.format(str(key)))
                                print()
                counter_comment += 1
                print()
                print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
                print()
        elif retrieval is 'bug_comments' and 'error' in data.keys():
            for key in search_list:
                if key in data.keys():
                    print('\t{}: {}'.format(key, data.get(key)))
                    ascii_doc_data_list.append('* {}: {}'.format(key, data.get(key)))
                    logger_bugzilla_main.info('{}: {}'.format(key, data.get(key)))
        else:
            if data is not None:
                for bug in data:
                    # BUG HISTORY
                    if retrieval is 'bug_history' and bug['history']:
                        logger_bugzilla_main.info('RETRIEVING BUG HISTORY')
                        history = bug.get('history')
                        counter_history = 1
                        for item_history in history:
                            item_history_keys_list = item_history.keys()
                            keys_to_retrieve = []
                            if len(search_list) > 0:
                                for key in search_list:
                                    if key in item_history_keys_list:
                                        keys_to_retrieve.append(key)
                                    # else:
                                    #     print('Some of the keys you entered do not match in the fields of the issue.')
                            else:
                                keys_to_retrieve = item_history_keys_list
                            ascii_doc_data_list.append('')
                            ascii_doc_data_list.append('=== History {}'.format(counter_history))
                            logger_bugzilla_main.info('Collecting History: {}'.format(counter_history))
                            for key in keys_to_retrieve:
                                if type(item_history.get(key)) is str:
                                    print(key + ':', item_history.get(key))
                                    ascii_doc_data_list.append('* ' + key + ': ' + item_history.get(key))
                                    logger_bugzilla_main.debug('>> string key: '.format(str(key)))
                                if type(item_history.get(key)) is list:
                                    print(key + ':')
                                    ascii_doc_data_list.append('* {}:'.format(key))
                                    logger_bugzilla_main.debug('>> listed key: {}'.format(str(key)))
                                    item_history_list = item_history.get(key)
                                    counter_item_list = 1
                                    for item_list in item_history_list:
                                        item_list_keys = item_list.keys()
                                        print('\tItem {}'.format(counter_item_list))
                                        ascii_doc_data_list.append('** Item {}'.format(counter_item_list))
                                        logger_bugzilla_main.debug('>>>> Item {}'.format(counter_item_list))
                                        for listed_key in item_list_keys:
                                            print('\t\t' + listed_key + ':', str(item_list.get(listed_key)))
                                            ascii_doc_data_list.append('*** ' + listed_key + ': ' + str(item_list.get(listed_key)))
                                            logger_bugzilla_main.debug('>>>>>> key: {}'.format(listed_key))
                                        print()
                                        counter_item_list += 1
                            counter_history += 1
                            print()
                            print('++++++++++++++++++++++++++++++++++++++++++++++++')
                            logger_bugzilla_main.debug('++++++++++++++++++++++++++++++++++++++++++++++++')
                            print()
                    # USER INFORMATION
                    elif retrieval is 'user_info':
                        logger_bugzilla_main.info('RETRIEVING USER INFORMATION')
                        user_keys_list = bug.keys()
                        keys_to_retrieve = []
                        if len(search_list) > 0:
                            for key in search_list:
                                if key in user_keys_list:
                                    keys_to_retrieve.append(key)
                                # else:
                                #     print('Some of the keys you entered do not match in the fields of the issue.')
                        else:
                            keys_to_retrieve = user_keys_list

                        ascii_doc_data_list.append('')
                        ascii_doc_data_list.append('=== User Fields')
                        logger_bugzilla_main.info('Collecting User Fields')
                        for key in keys_to_retrieve:
                            if key in user_keys_list:
                                print(key + ':', str(bug.get(key)))
                                ascii_doc_data_list.append('* ' + key + ': ' + str(bug.get(key)))
                                logger_bugzilla_main.debug('>> key: {}'.format(str(key)))
                        print('+++++++++++++++++++++++++++++++++++++++++++++++++++')
                        logger_bugzilla_main.debug('+++++++++++++++++++++++++++++++++++++++++++++++++++')
                    # BUG INFORMATION | USER ASSIGNED BUGS
                    elif retrieval is 'bug_info' or retrieval is 'user_assigned_bugs':
                        logger_bugzilla_main.info('RETRIEVING BUG INFORMATION')
                        bug_keys_list = bug.keys()
                        # print(bug_keys_list)
                        # print(len(bug_keys_list))
                        keys_to_retrieve = []
                        if len(search_list) > 0:
                            for key in search_list:
                                if key in bug_keys_list:
                                    keys_to_retrieve.append(key)
                                # else:
                                #     print('Some of the keys you entered do not match in the fields of the issue.')
                        else:
                            keys_to_retrieve = bug_keys_list
                        # retrieving keys
                        ascii_doc_data_list.append('')
                        if retrieval is 'bug_info':
                            print('Bug Information')
                            ascii_doc_data_list.append('=== Bug Information')
                            logger_bugzilla_main.info('Collecting Bug Information')
                        else:
                            print('BUG ID:', bug.get('id'))
                            ascii_doc_data_list.append('=== Bug: {}'.format(bug.get('id')))
                            logger_bugzilla_main.info('Collecting Information for the Bug: {}'.format(bug.get('id')))
                        for key in keys_to_retrieve:
                            if type(bug.get(key)) is str or type(bug.get(key)) is bool or type(bug.get(key)) is int or type(bug.get(key)) is None:
                                if bug.get(key) is '':
                                    print(key + ': ' + 'Nothing related to {} is now available.'.format(key))
                                    ascii_doc_data_list.append('* ' + key + ': ' + 'Nothing related to {} is now available.'.format(key))
                                    logger_bugzilla_main.debug('>> ' + key + ': ' + 'Nothing related to {} is now available.'.format(key))
                                else:
                                    print(key + ': ' + str(bug.get(key, 'Nothing related to {} is now available.'.format(key))))
                                    ascii_doc_data_list.append('* ' + key + ': ' + str(bug.get(key, 'Nothing related to {} is now available.'.format(key))))
                                    logger_bugzilla_main.debug('>> (string/boolean/integer) key: {}'.format(str(key)))
                                # print(type(bug.get(key)))
                                print()
                            if type(bug.get(key)) is list:
                                print(key + ':')
                                ascii_doc_data_list.append('* {}:'.format(key))
                                logger_bugzilla_main.debug('>> listed key: {}'.format(str(key)))
                                counter_dictionary_items = 1
                                for list_item in bug.get(key):
                                    if type(list_item) is dict:
                                        print('\tItem: {}'.format(counter_dictionary_items))
                                        ascii_doc_data_list.append('** Item: {}'.format(counter_dictionary_items))
                                        logger_bugzilla_main.debug('>>>> Dictionary Item: {}'.format(counter_dictionary_items))
                                        dictionary_keys = list_item.keys()
                                        for dictionary_key in dictionary_keys:
                                            # print(dictionary_keys)
                                            print('\t\t' + dictionary_key + ': ' + str(list_item.get(dictionary_key)))
                                            ascii_doc_data_list.append('*** ' + dictionary_key + ': ' + str(list_item.get(dictionary_key)))
                                            logger_bugzilla_main.debug('>>>>>> key: {}'.format(str(dictionary_key)))
                                        print()
                                        counter_dictionary_items += 1
                                    else:
                                        print('\t', list_item)
                                        ascii_doc_data_list.append('** {}'.format(list_item))
                                        logger_bugzilla_main.debug('>>>> list item collected')
                                        print()
                        print()
                        print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
                        print()
            else:
                print('* No data is now available for that query.')
                ascii_doc_data_list.append('* No data is now available for that query.')
                logger_bugzilla_main.warning('No data is now available for that query.')

        # returning all the data for the AsciiDoc file
        # print AsciiDoc data
        # for item in ascii_doc_data_list:
        #     print(item)
        return ascii_doc_data_list




