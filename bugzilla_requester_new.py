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


class BugRetriever:
    def __init__(self, bug_id, terms, user, release):
        self.bug_id = bug_id
        self.terms = terms
        self.user = user
        self.release = release

    def bug_info_retriever(self):
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

        return data

    def user_assigned_bugs_retriever(self):
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
        data = r.json()

        return data

    def data_retriever(self, data):
        if type(self.terms) is str and self.terms is not '':
            search_list = self.terms.split(', ')
        elif type(self.terms) is list:
            search_list = self.terms
        else:
            search_list = []
        print('Search List:', search_list)
        print('Length:', len(search_list))
        print()
        for bug in data['bugs']:
            bug_keys_list = bug.keys()
            # print(bug_keys_list)
            # print(len(bug_keys_list))
            print()
            print('Printing Keys:')
            print()
            keys_to_retrieve = []
            counter_bug_keys = 0
            if len(search_list) > 0:
                for key in search_list:
                    if key in bug_keys_list:
                        keys_to_retrieve.append(key)
                    else:
                        print('Some of the keys you entered do not match in the fields of the issue.')
            else:
                keys_to_retrieve = bug_keys_list
            # retrieving keys
            for key in keys_to_retrieve:
                if type(bug.get(key)) is str or type(bug.get(key)) is bool or type(bug.get(key)) is int or type(bug.get(key)) is None:
                    if bug.get(key) is '':
                        print(key + ': ' + 'Nothing related to {} is now available.'.format(key))
                    else:
                        print(key + ': ' + str(bug.get(key, 'Nothing related to {} is now available.'.format(key))))
                    # print(type(bug.get(key)))
                    print()
                if type(bug.get(key)) is list:
                    print(key + ':')
                    counter__dictionary_items = 1
                    for list_item in bug.get(key):
                        if type(list_item) is dict:
                            print('\tItem: {}'.format(counter__dictionary_items))
                            dictionary_keys = list_item.keys()
                            for dictionary_key in dictionary_keys:
                                # print(dictionary_keys)
                                print('\t\t' + dictionary_key + ':' + str(list_item.get(dictionary_key)))
                            print()
                            counter__dictionary_items += 1
                        else:
                            print('\t', list_item)
                            print()
                    print()
                counter_bug_keys += 1
            print()
            print('Countered keys:', counter_bug_keys)

    def getting_target_release_notes(self):
        print('RELEASE:', self.release)
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

        user_info_list = []
        config = configparser.ConfigParser()
        config.read('{}config.conf'.format(conf_path))
        company = config['bugzilla_basic_auth']['company']
        url = 'https://bugzilla.{}/rest/bug?target_release={}'.format(company, self.release)
        r = requests.get(url, params={'api_key': '{}'.format(api_key)})
        data = r.json()
        # pprint(data)
        print('Retrieving the data..')
        print()
        for item in data['bugs']:
            print(item.get('target_release'))
            print(item.get('id'))
            print(item.get('summary'))
            print('+++++++++++++++++++++++++++++++++++++++++++++++++')
        print()
        print('Successfully feetched the data.')

    def getting_user_info(self):
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

        user_info_list = []
        config = configparser.ConfigParser()
        config.read('{}config.conf'.format(conf_path))
        company = config['bugzilla_basic_auth']['company']
        url = 'https://bugzilla.{}/rest/user?names={}'.format(company, self.user)
        r = requests.get(url, params={'api_key': '{}'.format(api_key)})
        data = r.json()
        # pprint(data)
        if data['users']:
            for user in data['users']:
                user_keys = user.keys()
                for key in user_keys:
                    print(key + ':', str(user.get(key)))
            print('+++++++++++++++++++++++++++++++++++++++++++++++++++')

    # Getting comments from a bug
    def getting_comments(self):
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
        print()
        print('Bug ID:', self.bug_id)
        print('------------------')
        config = configparser.ConfigParser()
        config.read('{}config.conf'.format(conf_path))
        company = config['bugzilla_basic_auth']['company']
        # url = 'https://bugzilla.mozilla.org/rest/bug/{}/comment'.format(self.bug_id)
        url = 'https://bugzilla.{}/rest/bug/{}/comment'.format(company, self.bug_id)
        # u = url + "?token={}".format(api_key)
        r = requests.get(url, params={'api_key': '{}'.format(api_key)})
        data = r.json()
        search_list = ['attachment_id', 'bug_id', 'count', 'creation_time', 'creator', 'creator_id', 'id', 'is_private',
                       'tags', 'text', 'time']
        if data['bugs'][self.bug_id]['comments']:
            comments = data['bugs'][self.bug_id]['comments']
            counter_comment = 1
            for comment in comments:
                print('Comment: {}'.format(counter_comment))
                comment_keys = comment.keys()
                print()
                for key in comment_keys:
                    if type(comment.get(key)) is str:
                        print(key + ':', comment.get(key, 'Nothing related to {} has been found.'.format(key)))
                        print()
                    if type(comment.get(key)) is list:
                        print(key + ':')
                        key_list = comment.get(key)
                        for item_key in key_list:
                            print('\t', item_key)
                        print()
                    if type(comment.get(key)) is int:
                        print(key + ':', str(comment.get(key, 'Nothing related to {} has been found.'.format(key))))
                        print()
                counter_comment += 1
                print()
                print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
                print()

    # Getting a bug's history
    def getting_history(self):
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

        ascii_history_list = []
        print()
        print('Bug ID:', self.bug_id)
        ascii_history_list.append('== Bug ID: {}'.format(self.bug_id))
        print('------------------')
        config = configparser.ConfigParser()
        config.read('{}config.conf'.format(conf_path))
        company = config['bugzilla_basic_auth']['company']
        # url = 'https://bugzilla.mozilla.org/rest/bug/{}/history'.format(self.bug_id)
        url = 'https://bugzilla.{}/rest/bug/{}/history'.format(company, self.bug_id)
        # u = url + "?token={}".format(api_key)
        r = requests.get(url, params={'api_key': '{}'.format(api_key)})
        data = r.json()
        if data['bugs']:
            for bug in data['bugs']:
                if bug['history']:
                    history = bug.get('history')
                    for item_history in history:
                        item_history_keys = item_history.keys()
                        for key in item_history_keys:
                            if type(item_history.get(key)) is str:
                                print(key + ':', item_history.get(key))
                            if type(item_history.get(key)) is list:
                                print(key + ':')
                                item_history_list = item_history.get(key)
                                counter_item_list = 1
                                for item_list in item_history_list:
                                    item_list_keys = item_list.keys()
                                    print('\tItem {}'.format(counter_item_list))
                                    for key in item_list_keys:
                                        print('\t\t' + key + ':',  str(item_list.get(key)))
                                    print()
                                    counter_item_list += 1
                                print()
                                print('++++++++++++++++++++++++++++++++++++++++++++++++')
                                print()
                    print()
        # returning the data for the AsciiDoc file
        return ascii_history_list


if __name__ == '__main__':
    bugID = str(1376835)
    bug_fields = BugFields(bug_id=bugID)
    # bug_fields.get_bug_fields()
    print()
    print()
    # input_list = input('Please insert with comma, and without spaces, the fields you want to use:\n')
    search_bug = ['summary', 'platform', 'component']
    bug = BugRetriever(bug_id=bugID, terms=search_bug, user='luhliari@redhat.com', release='8.0')
    # bug.data_retriever()
    # data = bug.user_assigned_bugs_retriever()
    # bug.data_retriever(data=data)
    user = bug.getting_user_info()
    # comments = bug.getting_comments()
    # bug.getting_target_release_notes()
    # bug.getting_comments()
    # history = bug.getting_history()
