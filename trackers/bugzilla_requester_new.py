import logging
import requests
from pprint import pprint
import configparser
import os

from conf.confparse import BugzillaReadConfigurationApiKey

# create and configure a logger
LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging_file = logging.basicConfig(filename='log/bugzilla_request_new.log',
                                   level=logging.DEBUG,
                                   format=LOG_FORMAT,
                                   filemode='w')

# root logger (without name)
logger = logging.getLogger(__name__)

current_d = os.getcwd()
# print(current_d)
directories_list = current_d.split('/')
# print(directories_list)
# print(directories_list[1:4])
basic_desktop_path = directories_list[1:4]
new_path = 'conf/'
basic_desktop_path.append(new_path)
conf_path = '/' + '/'.join(basic_desktop_path)


class BugFields:
    def __init__(self, bug_id):
        self.bug_id = bug_id

    def get_bug_fields(self):
        api_connection = BugzillaReadConfigurationApiKey()
        api_key_auth = api_connection.key_auth()['api_key_auth']
        if api_key_auth is True:
            api_key_reason = api_connection.key_auth()['api_key_reason']
            logger.debug(api_key_reason)
            api_key = api_connection.key_auth()['api_key']
        else:
            api_key_reason = api_connection.key_auth()['api_key_reason']
            logger.warning(api_key_reason)
            raise Exception(api_key_reason)

        config = configparser.ConfigParser()
        config.read('{}config.conf'.format(conf_path))
        company = config['bugzilla_basic_auth']['company']
        r = requests.get('https://bugzilla.{}/rest/bug/'.format(company), params={'ids': '{}'.format(self.bug_id),
                                                                                  'api_key': '{}'.format(api_key)})
        data = r.json()
        # pprint(data)
        if 'bugs' in data.keys():
            print('Bug Fields:')
            print()
            keys = data.get('bugs')[0].keys()
            for key in keys:
                print(key)


class DataRetriever:
    def __init__(self, bug_id, terms, user, release):
        self.bug_id = bug_id
        self.terms = terms
        self.user = user
        self.release = release

    # TARGET RELEASE
    def getting_target_release_notes(self):
        retrieve = 'target_release_notes'
        ascii_target_release_list = []
        # for item in self.release:
        print('Release:', self.release)
        print('------------------')
        ascii_target_release_list.append('== Release: {}'.format(self.release))
        api_connection = BugzillaReadConfigurationApiKey()
        api_key_auth = api_connection.key_auth()['api_key_auth']
        if api_key_auth is True:
            api_key_reason = api_connection.key_auth()['api_key_reason']
            logger.debug(api_key_reason)
            api_key = api_connection.key_auth()['api_key']
        else:
            api_key_reason = api_connection.key_auth()['api_key_reason']
            logger.warning(api_key_reason)
            raise Exception(api_key_reason)

        config = configparser.ConfigParser()
        config.read('{}config.conf'.format(conf_path))
        company = config['bugzilla_basic_auth']['company']
        url = 'https://bugzilla.{}/rest/bug?target_release={}'.format(company, self.release)
        r = requests.get(url, params={'api_key': '{}'.format(api_key)})
        print('Retrieving the Target Release data from Bugzilla..')
        data = r.json()
        # pprint(data)
        print('Successfully fetched the data.')

        if data['bugs']:
            data_output = data.get('bugs')
            # pprint(data_output)
        else:
            data_output = None

        # read fields from configuration
        search_list_conf_input = config['target_release']['search_list']
        search_list_conf_input = search_list_conf_input.replace(', ', ',')
        search_list_conf_input = search_list_conf_input.replace(' ,', ',')
        search_list_conf_input = search_list_conf_input.replace(' , ', ',')
        search_list_conf_input = search_list_conf_input.split(',')
        print('Fields from conf file:', search_list_conf_input)
        if self.terms is not None:
            search_list_output = search_list_conf_input.extend(self.terms)

        else:
            search_list_output = search_list_conf_input

        print('Final fields to search:', search_list_output)
        ascii_target_release_list.append('* Search Fields: {}'.format(search_list_output))
        return {'retrieve': retrieve,
                'data_output': data_output,
                'search_list_output': search_list_output,
                'ascii_target_release_list': ascii_target_release_list}

        # for item in data['bugs']:
        #     print(item.get('target_release'))
        #     print(item.get('id'))
        #     print(item.get('summary'))
        #     print('+++++++++++++++++++++++++++++++++++++++++++++++++')
        # print()

    # BUG INFORMATION
    def getting_bug_info(self):
        retrieve = 'bug_info'
        ascii_bug_info_list = []
        print('Bug ID:', self.bug_id)
        print('------------------')
        ascii_bug_info_list.append('== Bug ID: {}'.format(self.bug_id))
        api_connection = BugzillaReadConfigurationApiKey()
        api_key_auth = api_connection.key_auth()['api_key_auth']
        if api_key_auth is True:
            api_key_reason = api_connection.key_auth()['api_key_reason']
            logger.debug(api_key_reason)
            api_key = api_connection.key_auth()['api_key']
        else:
            api_key_reason = api_connection.key_auth()['api_key_reason']
            logger.warning(api_key_reason)
            raise Exception(api_key_reason)

        config = configparser.ConfigParser()
        config.read('{}config.conf'.format(conf_path))
        # read company data from configuration file
        company = config['bugzilla_basic_auth']['company']
        r = requests.get('https://bugzilla.{}/rest/bug/'.format(company), params={'ids': '{}'.format(self.bug_id),
                                                                                  'api_key': '{}'.format(api_key)})
        print('Retrieving the Bug Information data from Bugzilla..')
        data = r.json()
        print('Successfully fetched the data.')

        if data['bugs']:
            data_output = data.get('bugs')
            # pprint(data_output)
        else:
            data_output = None

        # read fields from configuration
        search_list_conf_input = config['bug']['search_list']
        search_list_conf_input = search_list_conf_input.replace(', ', ',')
        search_list_conf_input = search_list_conf_input.replace(' ,', ',')
        search_list_conf_input = search_list_conf_input.replace(' , ', ',')
        search_list_conf_input = search_list_conf_input.split(',')
        print('Fields from conf file:', search_list_conf_input)
        if self.terms is not None:
            search_list_output = search_list_conf_input.extend(self.terms)

        else:
            search_list_output = search_list_conf_input

        print('Final fields to search:', search_list_output)
        ascii_bug_info_list.append('* Search Fields: {}'.format(search_list_output))
        return {'retrieve': retrieve,
                'data_output': data_output,
                'search_list_output': search_list_output,
                'ascii_bug_info_list': ascii_bug_info_list}

    # USER ASSIGNED BUGS
    def getting_user_assigned_bugs(self):
        retrieve = 'user_assigned_bugs'
        ascii_user_assigned_bugs_list = []
        print('User:', self.user)
        print('------------------')
        ascii_user_assigned_bugs_list.append('== User: {}'.format(self.user))
        api_connection = BugzillaReadConfigurationApiKey()
        api_key_auth = api_connection.key_auth()['api_key_auth']
        if api_key_auth is True:
            api_key_reason = api_connection.key_auth()['api_key_reason']
            logger.debug(api_key_reason)
            api_key = api_connection.key_auth()['api_key']
        else:
            api_key_reason = api_connection.key_auth()['api_key_reason']
            logger.warning(api_key_reason)
            raise Exception(api_key_reason)
        config = configparser.ConfigParser()
        config.read('{}config.conf'.format(conf_path))
        company = config['bugzilla_basic_auth']['company']
        r = requests.get('https://bugzilla.{}/rest/bug?assigned_to={}'.format(company, self.user),
                         params={'api_key': '{}'.format(api_key)})
        print('Retrieving the User Assigned Bugs data from Bugzilla..')
        data = r.json()
        # pprint(data)
        print('Successfully fetched the data.')

        if data['bugs']:
            data_output = data.get('bugs')
            # pprint(data_output)
        else:
            data_output = None

        # read fields from configuration
        search_list_conf_input = config['user_assigned_bugs']['search_list']
        search_list_conf_input = search_list_conf_input.replace(', ', ',')
        search_list_conf_input = search_list_conf_input.replace(' ,', ',')
        search_list_conf_input = search_list_conf_input.replace(' , ', ',')
        search_list_conf_input = search_list_conf_input.split(',')
        print('Fields from conf file:', search_list_conf_input)
        if self.terms is not None:
            search_list_output = search_list_conf_input.extend(self.terms)

        else:
            search_list_output = search_list_conf_input
        ascii_user_assigned_bugs_list.append('* Search Fields: {}'.format(search_list_output))
        print('Final fields to search:', search_list_output)
        return {'retrieve': retrieve,
                'data_output': data_output,
                'search_list_output': search_list_output,
                'ascii_user_assigned_bugs_list': ascii_user_assigned_bugs_list}

    # USER INFORMATION
    def getting_user_info(self):
        retrieve = 'user_info'
        ascii_user_info_list = []
        print('User:', self.user)
        print('------------------')
        ascii_user_info_list.append('== User: {}'.format(self.user))
        api_connection = BugzillaReadConfigurationApiKey()
        api_key_auth = api_connection.key_auth()['api_key_auth']
        if api_key_auth is True:
            api_key_reason = api_connection.key_auth()['api_key_reason']
            logger.debug(api_key_reason)
            api_key = api_connection.key_auth()['api_key']
        else:
            api_key_reason = api_connection.key_auth()['api_key_reason']
            logger.warning(api_key_reason)
            raise Exception(api_key_reason)

        config = configparser.ConfigParser()
        config.read('{}config.conf'.format(conf_path))
        company = config['bugzilla_basic_auth']['company']
        url = 'https://bugzilla.{}/rest/user?names={}'.format(company, self.user)
        r = requests.get(url, params={'api_key': '{}'.format(api_key)})
        print('Retrieving the User Information data from Bugzilla..')
        data = r.json()
        print('Successfully fetched the data.')

        if data['users']:
            data_output = data.get('users')
            # pprint(data_output)
        else:
            data_output = None

        # read fields from configuration
        search_list_conf_input = config['user_info']['search_list']
        search_list_conf_input = search_list_conf_input.replace(', ', ',')
        search_list_conf_input = search_list_conf_input.replace(' ,', ',')
        search_list_conf_input = search_list_conf_input.replace(' , ', ',')
        search_list_conf_input = search_list_conf_input.split(',')
        print('Fields from conf file:', search_list_conf_input)
        if self.terms is not None:
            search_list_output = search_list_conf_input.extend(self.terms)

        else:
            search_list_output = search_list_conf_input

        print('Final fields to search:', search_list_output)
        ascii_user_info_list.append('* Search Fields: {}'.format(search_list_output))
        return {'retrieve': retrieve,
                'data_output': data_output,
                'search_list_output': search_list_output,
                'ascii_user_info_list': ascii_user_info_list}

    # BUG COMMENTS
    def getting_bug_comments(self):
        retrieve = 'bug_comments'
        ascii_bug_comments_list = []
        print('Bug ID:', self.bug_id)
        print('------------------')
        ascii_bug_comments_list.append('== Bug ID: {}'.format(self.bug_id))
        api_connection = BugzillaReadConfigurationApiKey()
        api_key_auth = api_connection.key_auth()['api_key_auth']
        if api_key_auth is True:
            api_key_reason = api_connection.key_auth()['api_key_reason']
            logger.debug(api_key_reason)
            api_key = api_connection.key_auth()['api_key']
        else:
            api_key_reason = api_connection.key_auth()['api_key_reason']
            logger.warning(api_key_reason)
            raise Exception(api_key_reason)
        config = configparser.ConfigParser()
        config.read('{}config.conf'.format(conf_path))
        company = config['bugzilla_basic_auth']['company']
        # url = 'https://bugzilla.mozilla.org/rest/bug/{}/comment'.format(self.bug_id)
        url = 'https://bugzilla.{}/rest/bug/{}/comment'.format(company, self.bug_id)
        # u = url + "?token={}".format(api_key)
        r = requests.get(url, params={'api_key': '{}'.format(api_key)})

        print('Retrieving the Bug Comments data from Bugzilla..')
        data = r.json()
        print('Successfully fetched the data.')

        if data['bugs']:
            data_output = data.get('bugs')
            # pprint(data_output)
        else:
            data_output = None

        # read fields from configuration
        search_list_conf_input = config['comments']['search_list']
        search_list_conf_input = search_list_conf_input.replace(', ', ',')
        search_list_conf_input = search_list_conf_input.replace(' ,', ',')
        search_list_conf_input = search_list_conf_input.replace(' , ', ',')
        search_list_conf_input = search_list_conf_input.split(',')
        print('Fields from conf file:', search_list_conf_input)
        if self.terms is not None:
            search_list_output = search_list_conf_input.extend(self.terms)

        else:
            search_list_output = search_list_conf_input

        print('Final fields to search:', search_list_output)
        ascii_bug_comments_list.append('* Search Fields: {}'.format(search_list_output))
        return {'retrieve': retrieve,
                'data_output': data_output,
                'search_list_output': search_list_output,
                'ascii_bug_comments_list': ascii_bug_comments_list}

    # BUG HISTORY
    def getting_bug_history(self):
        retrieve = 'bug_history'
        ascii_bug_history_list = []
        print('Bug ID:', self.bug_id)
        print('------------------')
        ascii_bug_history_list.append('== Bug ID: {}'.format(self.bug_id))
        api_connection = BugzillaReadConfigurationApiKey()
        api_key_auth = api_connection.key_auth()['api_key_auth']
        if api_key_auth is True:
            api_key_reason = api_connection.key_auth()['api_key_reason']
            logger.debug(api_key_reason)
            api_key = api_connection.key_auth()['api_key']
        else:
            api_key_reason = api_connection.key_auth()['api_key_reason']
            logger.warning(api_key_reason)
            raise Exception(api_key_reason)
        config = configparser.ConfigParser()
        config.read('{}config.conf'.format(conf_path))
        company = config['bugzilla_basic_auth']['company']
        # url = 'https://bugzilla.mozilla.org/rest/bug/{}/history'.format(self.bug_id)
        url = 'https://bugzilla.{}/rest/bug/{}/history'.format(company, self.bug_id)
        # u = url + "?token={}".format(api_key)
        r = requests.get(url, params={'api_key': '{}'.format(api_key)})

        print('Retrieving the Bug History data from Bugzilla..')
        data = r.json()
        print('Successfully fetched the data.')

        if data['bugs']:
            data_output = data.get('bugs')
            # pprint(data_output)
        else:
            data_output = None

        # read fields from configuration
        search_list_conf_input = config['bug_history']['search_list']
        search_list_conf_input = search_list_conf_input.replace(', ', ',')
        search_list_conf_input = search_list_conf_input.replace(' ,', ',')
        search_list_conf_input = search_list_conf_input.replace(' , ', ',')
        search_list_conf_input = search_list_conf_input.split(',')
        print('Fields from conf file:', search_list_conf_input)
        if self.terms is not None:
            search_list_output = search_list_conf_input.extend(self.terms)

        else:
            search_list_output = search_list_conf_input

        print('Final fields to search:', search_list_output)
        ascii_bug_history_list.append('* Search Fields: {}'.format(search_list_output))
        return {'retrieve': retrieve,
                'data_output': data_output,
                'search_list_output': search_list_output,
                'ascii_bug_history_list': ascii_bug_history_list}

    # MAIN CLASS FUNCTION FOR DATA RETRIEVING FROM EACH QUERY TO THE REST API
    def data_retriever(self, retrieval, data, search_list, ascii_doc_data):
        ascii_doc_data_list = []
        print('Search List:', search_list)
        print('Search List Length:', len(search_list))
        print()
        ascii_doc_data_list.extend(ascii_doc_data)
        # BUG COMMENTS
        if retrieval is 'bug_comments' and data[self.bug_id]['comments']:
            comments = data[self.bug_id]['comments']
            counter_comment = 1
            for comment in comments:
                print('Comment: {}'.format(counter_comment))
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
                                print()
                            if type(comment.get(key)) is list:
                                print(key + ':')
                                ascii_doc_data_list.append('* {}'.format(key))
                                key_list = comment.get(key)
                                for item_key in key_list:
                                    print('\t', item_key)
                                    ascii_doc_data_list.append('** {}'.format(item_key))
                                print()
                            if type(comment.get(key)) is int:
                                print(key + ':', str(comment.get(key, 'Nothing related to {} has been found.'.format(key))))
                                ascii_doc_data_list.append('* ' + key + ': ' + str(
                                    comment.get(key, 'Nothing related to {} is now available.'.format(key))))
                                print()
                            if type(comment.get(key)) is bool:
                                print(key + ':', str(comment.get(key, 'Nothing related to {} has been found.'.format(key))))
                                ascii_doc_data_list.append('* ' + key + ': ' + str(
                                    comment.get(key, 'Nothing related to {} is now available.'.format(key))))
                                print()
                counter_comment += 1
                print()
                print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
                print()
        else:
            for bug in data:
                # BUG HISTORY
                if retrieval is 'bug_history' and bug['history']:
                    history = bug.get('history')
                    counter_history = 1
                    for item_history in history:
                        item_history_keys_list = item_history.keys()
                        # print('BUGKEYSALL:', item_history_keys_list)
                        keys_to_retrieve = []
                        if len(search_list) > 0:
                            for key in search_list:
                                if key in item_history_keys_list:
                                    keys_to_retrieve.append(key)
                                else:
                                    print('Some of the keys you entered do not match in the fields of the issue.')
                        else:
                            keys_to_retrieve = item_history_keys_list
                        ascii_doc_data_list.append('')
                        ascii_doc_data_list.append('=== History {}'.format(counter_history))
                        for key in keys_to_retrieve:
                            if type(item_history.get(key)) is str:
                                print(key + ':', item_history.get(key))
                                ascii_doc_data_list.append('* ' + key + ': ' + item_history.get(key))
                            if type(item_history.get(key)) is list:
                                print(key + ':')
                                ascii_doc_data_list.append('* {}:'.format(key))
                                item_history_list = item_history.get(key)
                                counter_item_list = 1
                                for item_list in item_history_list:
                                    item_list_keys = item_list.keys()
                                    print('\tItem {}'.format(counter_item_list))
                                    ascii_doc_data_list.append('** Item {}'.format(counter_item_list))
                                    for key in item_list_keys:
                                        print('\t\t' + key + ':', str(item_list.get(key)))
                                        ascii_doc_data_list.append('*** ' + key + ': ' + str(item_list.get(key)))
                                    print()
                                    counter_item_list += 1
                        counter_history += 1
                        print()
                        print('++++++++++++++++++++++++++++++++++++++++++++++++')
                        print()
                # USER INFORMATION
                elif retrieval is 'user_info':
                    user_keys_list = bug.keys()
                    # print('USERKEYSALL:', user_keys_list)
                    keys_to_retrieve = []
                    if len(search_list) > 0:
                        for key in search_list:
                            if key in user_keys_list:
                                keys_to_retrieve.append(key)
                            else:
                                print('Some of the keys you entered do not match in the fields of the issue.')
                    else:
                        keys_to_retrieve = user_keys_list

                    ascii_doc_data_list.append('')
                    ascii_doc_data_list.append('=== User Fields')
                    for key in keys_to_retrieve:
                        if key in user_keys_list:
                            print(key + ':', str(bug.get(key)))
                            ascii_doc_data_list.append('* ' + key + ': ' + str(bug.get(key)))
                    print('+++++++++++++++++++++++++++++++++++++++++++++++++++')
                # TARGET RELEASE | BUG INFORMATION | USER ASSIGNED BUGS
                elif retrieval is 'target_release_notes' or retrieval is 'bug_info' or retrieval is 'user_assigned_bugs':
                    bug_keys_list = bug.keys()
                    # print(bug_keys_list)
                    # print(len(bug_keys_list))
                    keys_to_retrieve = []
                    if len(search_list) > 0:
                        for key in search_list:
                            if key in bug_keys_list:
                                keys_to_retrieve.append(key)
                            else:
                                print('Some of the keys you entered do not match in the fields of the issue.')
                    else:
                        keys_to_retrieve = bug_keys_list
                    # retrieving keys
                    print('BUG ID:', bug.get('id'))
                    ascii_doc_data_list.append('')
                    if retrieval is 'bug_info':
                        ascii_doc_data_list.append('=== Bug Information')
                    else:
                        ascii_doc_data_list.append('=== Bug: {}'.format(bug.get('id')))
                    for key in keys_to_retrieve:
                        if type(bug.get(key)) is str or type(bug.get(key)) is bool or type(bug.get(key)) is int or type(bug.get(key)) is None:
                            if bug.get(key) is '':
                                print(key + ': ' + 'Nothing related to {} is now available.'.format(key))
                                ascii_doc_data_list.append('* ' + key + ': ' + 'Nothing related to {} is now available.'.format(key))
                            else:
                                print(key + ': ' + str(bug.get(key, 'Nothing related to {} is now available.'.format(key))))
                                ascii_doc_data_list.append('* ' + key + ': ' + str(bug.get(key, 'Nothing related to {} is now available.'.format(key))))
                            # print(type(bug.get(key)))
                            print()
                        if type(bug.get(key)) is list:
                            print(key + ':')
                            ascii_doc_data_list.append('* {}:'.format(key))
                            counter__dictionary_items = 1
                            for list_item in bug.get(key):
                                if type(list_item) is dict:
                                    print('\tItem: {}'.format(counter__dictionary_items))
                                    ascii_doc_data_list.append('** Item: {}'.format(counter__dictionary_items))
                                    dictionary_keys = list_item.keys()
                                    for dictionary_key in dictionary_keys:
                                        # print(dictionary_keys)
                                        print('\t\t' + dictionary_key + ': ' + str(list_item.get(dictionary_key)))
                                        ascii_doc_data_list.append('*** ' + dictionary_key + ': ' + str(list_item.get(dictionary_key)))
                                    print()
                                    counter__dictionary_items += 1
                                else:
                                    print('\t', list_item)
                                    ascii_doc_data_list.append('** {}'.format(list_item))
                                    print()
                    print()
                    print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
                    print()

        # returning all the data for the AsciiDoc file
        print()
        print('ASCIIDOC')
        for item in ascii_doc_data_list:
            print(item)
        return ascii_doc_data_list

# bugID = str(1376835)
# bug_fields = BugFields(bug_id=bugID)
# # bug_fields.get_bug_fields()
# print()
# print()



