import logging
import requests
from pprint import pprint

from conf.confparse import BugzillaReadConfigurationBasicAuth
from conf.confparse import BugzillaReadConfigurationApiKey

# create and configure a logger
LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging_file = logging.basicConfig(filename='log/bugzilla_request.log',
                                   level=logging.DEBUG,
                                   format=LOG_FORMAT,
                                   filemode='w')

# root logger (without name)
logger = logging.getLogger()


"""CLASS: CONNECTING TO BUGZILLA API WITH THE API TOKEN + BUG ID INSERTION --> FETCHING THE DATA"""


class Connector:
    def __init__(self, bug_id):
        self.bug_id = bug_id

    def connection(self):
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

        print('Connection to Bugzilla API..')
        logger.debug('Connection to Bugzilla API..')
        r = requests.get('https://bugzilla.mozilla.org/rest/bug/', params={'ids': '{}'.format(self.bug_id),
                                                                           'api_key': '{}'.format(api_key)})
        success_connection = str(r)
        if success_connection == '<Response [200]>':
            print('Connected successfully!')
            print('Fetching the data from the API..')
            # Data fetched in JSON format (Python Dictionary format)
            data = r.json()
            # Pretty printing of the JSON data
            # pprint(data)
            print()
            # returning the fetched JSON data
            return data
        else:
            data = 'Connection was not successful at this time. Please try again..'
            print(data)


"""CLASS: Handling all the data by a single bug """


class BugRetriever:
    def __init__(self, bug_id):
        self.bug_id = bug_id

    def data_retriever(self):
        #
        # Object creation for the connection to the API and searching for the Bug by its unique ID
        connector = Connector(self.bug_id)
        # Fetching the data from the API
        data_fetched = connector.connection()

        # Basic Fields List of asciidoc fields declaration
        bug_basic_fields_feed = []

        # Custom Fields List of asciidoc fields declaration
        bug_custom_fields_feed = []

        if data_fetched:
            print()
            print('Bug ID:', self.bug_id)
            print('------------------')
            # pprint(data_fetched)
            # print(data_fetched.keys())
            for bugs in data_fetched.keys():
                if bugs == 'bugs':
                    for bug in data_fetched[bugs]:
                        bug_keys_list = bug.keys()
                        counter_keys_basic = 0
                        # BASIC FIELDS
                        print('BASIC FIELDS')
                        for key in bug_keys_list:
                            if not key.startswith('cf'):
                                # print(key + ':', bug.get(key))
                                counter_keys_basic += 1

                        bug_basic_fields_feed.append('== Basic Fields')
                        # Summary
                        bug_basic_fields_feed.append('=== Summary')
                        if bug['summary'] and bug['summary'] is not '':
                            bug_basic_fields_feed.append('* Summary: {}'.format(bug['summary']))
                        else:
                            bug_basic_fields_feed.append('* No summary is available')
                        # Assigned_to
                        bug_basic_fields_feed.append('=== Assigned to')
                        if bug['assigned_to'] and bug['assigned_to'] is not '':
                            # Assigned to Info
                            bug_basic_fields_feed.append('* Email: {}'.format(bug['assigned_to_detail']['email']))
                            bug_basic_fields_feed.append('* ID: {}'.format(bug['assigned_to_detail']['id']))
                            bug_basic_fields_feed.append('* Name: {}'.format(bug['assigned_to_detail']['name']))
                            bug_basic_fields_feed.append('* Nickname: {}'.format(bug['assigned_to_detail']['nick']))
                            bug_basic_fields_feed.append('* Real Name: {}'
                                                         .format(bug['assigned_to_detail']['real_name']))
                        else:
                            bug_basic_fields_feed.append('No assigned user.')
                        # Blocks
                        bug_basic_fields_feed.append('=== Blocks')
                        list_blocks = bug['blocks']
                        if len(list_blocks) > 0:
                            counter_list_blocks = 1
                            for block_item in list_blocks:
                                bug_basic_fields_feed.append('* Block Item {}:'.format(counter_list_blocks) + ' {}'
                                                             .format(block_item))
                                counter_list_blocks += 1
                        else:
                            bug_basic_fields_feed.append('* No blocks listed at this time.')
                        # CC mails
                        bug_basic_fields_feed.append('=== CC')
                        list_cc = bug['cc']
                        if len(list_cc) > 0:
                            counter_list_cc = 1
                            for cc in list_cc:
                                bug_basic_fields_feed.append('* CC {}:'.format(counter_list_cc) + ' {}'.format(cc))
                                counter_list_cc += 1
                            # CC Detail
                            bug_basic_fields_feed.append('=== CC Information')
                            list_cc_detail = bug['cc_detail']
                            if len(list_cc_detail) > 0:
                                counter_cc_detail = 1
                                for cc_item in list_cc_detail:
                                    bug_basic_fields_feed.append('* CC {} Information:'.format(counter_cc_detail))
                                    bug_basic_fields_feed.append('** Email: {}'.format(cc_item['email']))
                                    bug_basic_fields_feed.append('** ID: {}'.format(cc_item['id']))
                                    bug_basic_fields_feed.append('** Name: {}'.format(cc_item['name']))
                                    bug_basic_fields_feed.append('** Nickname: {}'.format(cc_item['nick']))
                                    bug_basic_fields_feed.append('** Real Name: {}'.format(cc_item['real_name']))
                                    counter_cc_detail += 1
                        else:
                            bug_basic_fields_feed.append('* No CC listed at this time.')
                        # Classification
                        bug_basic_fields_feed.append('=== Classification')
                        if bug['classification'] and bug['classification'] is not '':
                            bug_basic_fields_feed.append('* {}'.format(bug['classification']))
                        else:
                            bug_basic_fields_feed.append('* No Classification is defined at this time.')
                        # Comments counted
                        bug_basic_fields_feed.append('=== Comments Counted')
                        if bug['comment_count']:
                            bug_basic_fields_feed.append('* Count: ' + str(bug['comment_count']))
                        else:
                            bug_basic_fields_feed.append('* No Comments are available at this time.')
                        # Component
                        bug_basic_fields_feed.append('=== Component')
                        if bug['component'] and bug['component'] is not '':
                            bug_basic_fields_feed.append('* {}'.format(bug['component']))
                        else:
                            bug_basic_fields_feed.append('* No Component is defined.')
                        # Creation Time
                        bug_basic_fields_feed.append('=== Creation Time')
                        if bug['creation_time'] and bug['creation_time'] is not '':
                            bug_basic_fields_feed.append('* {}'.format(bug['creation_time']))
                        else:
                            bug_basic_fields_feed.append('* No time of creation is available.')
                        # Creator
                        bug_basic_fields_feed.append('=== Creator')
                        if bug['creator'] and bug['creator'] is not '':
                            bug_basic_fields_feed.append('* {}'.format(bug['creator']))
                            # creator_detail
                            bug_basic_fields_feed.append('* Creator Information:')
                            bug_basic_fields_feed.append('** Email: {}'.format(bug['creator_detail']['email']))
                            bug_basic_fields_feed.append('** ID: {}'.format(bug['creator_detail']['id']))
                            bug_basic_fields_feed.append('** Name: {}'.format(bug['creator_detail']['name']))
                            bug_basic_fields_feed.append('** Nickname: {}'.format(bug['creator_detail']['nick']))
                            bug_basic_fields_feed.append('** Real Name: {}'.format(bug['creator_detail']['real_name']))
                        else:
                            bug_basic_fields_feed.append('* Creator is not defined.')
                        # Depends On
                        bug_basic_fields_feed.append('=== Depends On')
                        depends_on_list = bug['depends_on']
                        if len(depends_on_list) > 0:
                            counter_depends_on_list = 1
                            for depends_item in depends_on_list:
                                bug_basic_fields_feed.append('* Dependency {}'.format(counter_depends_on_list))
                                bug_basic_fields_feed.append('** {}'.format(depends_item))
                                counter_depends_on_list += 1
                        else:
                            bug_basic_fields_feed.append('* No dependencies were found.')
                        # Dupe of
                        bug_basic_fields_feed.append('=== Dupe of')
                        if bug['dupe_of'] and bug['dupe_of'] is not None:
                            bug_basic_fields_feed.append('* {}'.format(bug['dupe_of']))
                        else:
                            bug_basic_fields_feed.append('* No Dupe of information at this time.')
                        # Duplicates
                        bug_basic_fields_feed.append('=== Duplicates')
                        duplicates_list = bug['duplicates']
                        if len(duplicates_list) > 0:
                            counter_duplicates_list = 1
                            for duplicates_item in duplicates_list:
                                bug_basic_fields_feed.append('* Duplicate {}'.format(counter_duplicates_list))
                                bug_basic_fields_feed.append('** {}'.format(duplicates_item))
                                counter_duplicates_list += 1
                        else:
                            bug_basic_fields_feed.append('* No listed items.')
                        # Flags
                        flags_list = bug['flags']
                        bug_basic_fields_feed.append('=== Flags')
                        if len(flags_list) > 0:
                            counter_flags_list = 1
                            for flags_item in flags_list:
                                bug_basic_fields_feed.append('* Flag {}'.format(counter_flags_list))
                                bug_basic_fields_feed.append('** {}'.format(flags_item))
                                counter_flags_list += 1
                        else:
                            bug_basic_fields_feed.append('* No listed items.')
                        # Groups
                        bug_basic_fields_feed.append('=== Groups')
                        groups_list = bug['groups']
                        if len(groups_list) > 0:
                            counter_groups_list = 1
                            for group_item in groups_list:
                                bug_basic_fields_feed.append('* Group {}'.format(counter_groups_list))
                                bug_basic_fields_feed.append('** {}'.format(group_item))
                                counter_groups_list += 1
                        else:
                            bug_basic_fields_feed.append('* No listed items.')
                        # ID
                        bug_basic_fields_feed.append('=== ID')
                        if bug['id'] and bug['id'] is not None:
                            bug_basic_fields_feed.append('* {}'.format(bug['id']))
                        else:
                            bug_basic_fields_feed.append('* No ID available.')
                        # Is CC Accessble
                        bug_basic_fields_feed.append('=== Is CC Accessble')
                        bug_basic_fields_feed.append('* {}'.format(bug['is_cc_accessible']))
                        # Is Confirmed
                        bug_basic_fields_feed.append('=== Is Confirmed')
                        bug_basic_fields_feed.append('* {}'.format(bug['is_confirmed']))
                        # Is Creator Accessible
                        bug_basic_fields_feed.append('=== Is Creator Accessible')
                        bug_basic_fields_feed.append('* {}'.format(bug['is_creator_accessible']))
                        # Is Open
                        bug_basic_fields_feed.append('=== Is Open')
                        bug_basic_fields_feed.append('* {}'.format(bug['is_open']))
                        # Keywords
                        keywords_list = bug['keywords']
                        bug_basic_fields_feed.append('=== Keywords')
                        if len(keywords_list) > 0:
                            counter_keywords_list = 1
                            for keyword_item in keywords_list:
                                bug_basic_fields_feed.append('* Keyword {}'.format(counter_keywords_list))
                                bug_basic_fields_feed.append('** {}'.format(keyword_item))
                                counter_keywords_list += 1
                        else:
                            bug_basic_fields_feed.append('* No listed keywords.')
                        # Last Change Time
                        bug_basic_fields_feed.append('=== Last Change Time')
                        if bug['last_change_time'] and bug['last_change_time'] is not '':
                            bug_basic_fields_feed.append('* {}'.format(bug['last_change_time']))
                        else:
                            bug_basic_fields_feed.append('* No Last Change Time is available.')
                        # Mentors
                        bug_basic_fields_feed.append('=== Mentors')
                        mentors_list = bug['mentors']
                        if len(mentors_list) > 0:
                            counter_mentors_list = 1
                            for mentor_item in mentors_list:
                                bug_basic_fields_feed.append('* Mentor {}'.format(counter_mentors_list))
                                bug_basic_fields_feed.append('** {}'.format(mentor_item))
                                counter_mentors_list += 1
                            # Mentors Information
                            bug_basic_fields_feed.append('=== Mentors Information')
                            mentors_detail_list = bug['mentors_detail']
                            if len(mentors_detail_list) > 0:
                                counter_mentors_detail_list = 1
                                for mentor_item in mentors_detail_list:
                                    bug_basic_fields_feed.append('* Mentor {}'.format(counter_mentors_detail_list))
                                    bug_basic_fields_feed.append('** Email: {}'.format(mentor_item['email']))
                                    bug_basic_fields_feed.append('** ID: {}'.format(mentor_item['id']))
                                    bug_basic_fields_feed.append('** Name: {}'.format(mentor_item['name']))
                                    bug_basic_fields_feed.append('** Nickname: {}'.format(mentor_item['nick']))
                                    bug_basic_fields_feed.append('** Real Name: {}'.format(mentor_item['real_name']))
                                    counter_mentors_detail_list += 1
                        else:
                            bug_basic_fields_feed.append('* No listed Mentors.')
                        # Operation System
                        bug_basic_fields_feed.append('=== Operation System')
                        if bug['op_sys'] and bug['op_sys'] is not '':
                            bug_basic_fields_feed.append('* {}'.format(bug['op_sys']))
                        else:
                            bug_basic_fields_feed.append('* The operating system is not defined.')
                        # Platform
                        bug_basic_fields_feed.append('=== Platform')
                        if bug['platform'] and bug['platform'] is not '':
                            bug_basic_fields_feed.append('* {}'.format(bug['platform']))
                        else:
                            bug_basic_fields_feed.append('* The platform is not defined.')
                        # Priority
                        bug_basic_fields_feed.append('=== Priority')
                        if bug['priority'] and bug['priority'] is not '':
                            bug_basic_fields_feed.append('* {}'.format(bug['priority']))
                        else:
                            bug_basic_fields_feed.append('* The priority of the bug is not defined.')
                        # Product
                        bug_basic_fields_feed.append('=== Product')
                        if bug['product'] and bug['product'] is not '':
                            bug_basic_fields_feed.append('* {}'.format(bug['product']))
                        else:
                            bug_basic_fields_feed.append('* No product information is available.')
                        # QA Contact
                        bug_basic_fields_feed.append('=== QA Contact')
                        if bug['qa_contact'] and bug['qa_contact'] is not '':
                            bug_basic_fields_feed.append('* {}:'.format(bug['qa_contact']))
                            # qa_contact_detail
                            bug_basic_fields_feed.append('=== QA Contact Information')
                            bug_basic_fields_feed.append('* Email: {}'.format(bug['qa_contact_detail']['email']))
                            bug_basic_fields_feed.append('* ID: {}'.format(bug['qa_contact_detail']['id']))
                            bug_basic_fields_feed.append('* Name: {}'.format(bug['qa_contact_detail']['name']))
                            bug_basic_fields_feed.append('* Nickname: {}'.format(bug['qa_contact_detail']['nick']))
                            bug_basic_fields_feed.append('* Real Name: {}'
                                                         .format(bug['qa_contact_detail']['real_name']))
                        else:
                            bug_basic_fields_feed.append('*  There is no QA Contact available.')
                        # Regressed by
                        bug_basic_fields_feed.append('=== Regressed By')
                        regressed_by_list = bug['regressed_by']
                        if len(regressed_by_list) > 0:
                            counter_regressed_by_list = 1
                            for regressed_by_item in regressed_by_list:
                                bug_basic_fields_feed.append('* Regressed by {}'.format(counter_regressed_by_list))
                                bug_basic_fields_feed.append('** {}'.format(regressed_by_item))
                                counter_regressed_by_list += 1
                        else:
                            bug_basic_fields_feed.append('* No listed items.')
                        # Regressions
                        bug_basic_fields_feed.append('=== Regressions')
                        regressions_list = bug['regressions']
                        if len(regressions_list) > 0:
                            counter_regressions_list = 1
                            for regression_item in regressions_list:
                                bug_basic_fields_feed.append('* Regression {}'.format(counter_regressions_list))
                                bug_basic_fields_feed.append('** {}'.format(regression_item))
                                counter_regressions_list += 1
                        else:
                            bug_basic_fields_feed.append('* No listed items.')
                        # Resolution
                        bug_basic_fields_feed.append('=== Resolution')
                        if bug['resolution'] and bug['resolution'] is not '':
                            bug_basic_fields_feed.append('* {}'.format(bug['resolution']))
                        else:
                            bug_basic_fields_feed.append('* No resolution is defined.')
                        # See Also
                        bug_basic_fields_feed.append('=== See Also')
                        see_also_list = bug['see_also']
                        if len(see_also_list) > 0:
                            counter_see_also_list = 1
                            for see_item in see_also_list:
                                bug_basic_fields_feed.append('* See {}'.format(counter_see_also_list))
                                bug_basic_fields_feed.append('** {}'.format(see_item))
                                counter_see_also_list += 1
                        else:
                            bug_basic_fields_feed.append('* No listed items.')
                        # Severity
                        bug_basic_fields_feed.append('=== Severity')
                        if bug['severity'] and bug['severity'] is not '':
                            bug_basic_fields_feed.append('* {}'.format(bug['severity']))
                        else:
                            bug_basic_fields_feed.append('* Severity is not defined.')
                        # Status
                        bug_basic_fields_feed.append('=== Status')
                        if bug['status'] and bug['status'] is not '':
                            bug_basic_fields_feed.append('* {}'.format(bug['status']))
                        else:
                            bug_basic_fields_feed.append('* Status is not available.')
                        # Target Milestone
                        bug_basic_fields_feed.append('=== Target Milestone')
                        if bug['target_milestone'] and bug['target_milestone'] is not '---':
                            bug_basic_fields_feed.append('* {}'.format(bug['target_milestone']))
                        else:
                            bug_basic_fields_feed.append('* No target milestone is available.')
                        # Type
                        bug_basic_fields_feed.append('=== Type')
                        if bug['type'] and bug['type'] is not '':
                            bug_basic_fields_feed.append('* {}'.format(bug['type']))
                        else:
                            bug_basic_fields_feed.append('* No bug type is available.')
                        # Update Token
                        bug_basic_fields_feed.append('=== Update Token')
                        if bug['update_token'] and bug['update_token'] is not '':
                            bug_basic_fields_feed.append('* {}'.format(bug['update_token']))
                        else:
                            bug_basic_fields_feed.append('* Update token is not available')
                        # URL
                        bug_basic_fields_feed.append('=== URL')
                        if bug['url'] and bug['url'] is not '':
                            bug_basic_fields_feed.append('* {}'.format(bug['url']))
                        else:
                            bug_basic_fields_feed.append('* No URL is defined')
                        # version
                        bug_basic_fields_feed.append('=== Version')
                        if bug['version'] and bug['version'] is not '':
                            bug_basic_fields_feed.append('* {}'.format('* {}'.format(bug['version'])))
                        else:
                            bug_basic_fields_feed.append('* No version is defined')
                        # votes
                        bug_basic_fields_feed.append('=== Votes')
                        if bug['votes']:
                            bug_basic_fields_feed.append('* {}'.format(bug['votes']))
                        else:
                            bug_basic_fields_feed.append('* No votes are defined.')
                        # whiteboard
                        bug_basic_fields_feed.append('=== Whiteboard')
                        if bug['whiteboard'] and bug['whiteboard'] is not '':
                            bug_basic_fields_feed.append('* {}'.format(bug['whiteboard']))
                        else:
                            bug_basic_fields_feed.append('* Whiteboard is not available')
                        # alias
                        bug_basic_fields_feed.append('=== Alias')
                        if bug['alias'] and bug['alias'] is not None:
                            bug_basic_fields_feed.append('* {}'.format(bug['alias']))
                        else:
                            bug_basic_fields_feed.append('* No alias is specified')
                        print('Countered Basic Fields:', counter_keys_basic)
                        print('---')
                        # CUSTOM FIELDS
                        print('CUSTOM FIELDS')
                        bug_basic_fields_feed.append('== Custom Fields')
                        counter_keys_cf = 0
                        for key in bug_keys_list:
                            if key.startswith('cf'):
                                bug_basic_fields_feed.append('* {}'.format(key) + ': {}'.format(bug.get(key)))
                                counter_keys_cf += 1
                        print('Countered Custom Fields:', counter_keys_cf)
                        # print()
                        # for item in bug_basic_fields_feed:
                        #     print(item)
                        #     print()
                elif bugs != 'bugs' and bugs != 'faults':
                    # In case of error
                    # pprint(data_fetched)
                    bug_basic_fields_feed.append(data_fetched)
        return bug_basic_fields_feed


""" CLASS: Getting all comments for a single bug """


class Comments:
    def __init__(self, bug_id):
        self.bug_id = bug_id

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
        # url = 'https://bugzilla.mozilla.org/rest/bug/{}/comment'.format(self.bug_id)
        url = 'https://bugzilla.mozilla.org/rest/bug/{}/comment'.format(self.bug_id)
        u = url + "?token={}".format(api_key)
        r = requests.get(u)
        data = r.json()
        # pprint(data)
        # print(data.keys())
        bug_comments_list = []
        for bugs in data.keys():
            if bugs == 'bugs':
                real_documents = data[bugs][str(self.bug_id)]['comments']
                counter_comments = 1
                bug_comments_list.append('== Comments')
                for item in real_documents:
                    bug_comments_list.append('=== Comment {}'.format(counter_comments))
                    bug_comments_list.append('* Text:')
                    bug_comments_list.append('** {}'.format(item['text']))
                    bug_comments_list.append('* Author: {}'.format(item['author']))
                    bug_comments_list.append('* Created at: {}'.format(item['creation_time']))
                    bug_comments_list.append('* Bug ID: {}'.format(item['bug_id']))
                    counter_comments += 1
                print('Comments No.:', counter_comments - 1)
            elif bugs != 'bugs' and bugs != 'comments':
                bug_comments_list.append('* {}'.format(data))
            else:
                # In case of returning nothing
                bug_comments_list.append('* No comments are available at this time.')
        # print()
        # for item in bug_comments_list:
        #     print(item)
        #     print()
        return bug_comments_list


""" CLASS: Getting history of all metadata changes for a single bug """


class History:
    def __init__(self, bug_id):
        self.bug_id = bug_id

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

        history_list = []
        print()
        print('Bug ID:', self.bug_id)
        print('------------------')
        # url = 'https://bugzilla.mozilla.org/rest/bug/{}/history'.format(self.bug_id)
        url = 'https://bugzilla.mozilla.org/rest/bug/{}/history'.format(self.bug_id)
        u = url + "?token={}".format(api_key)
        r = requests.get(u)
        data = r.json()
        # print(data.keys())
        history_list.append('== History')
        for bugs in data.keys():
            if bugs == 'bugs':
                real_documents = data['bugs'][0]['history']
                counter_history = 1
                for item in real_documents:
                    history_list.append('=== History {}'.format(counter_history))
                    history_list.append('* Datetime: {}'.format( item['when']))
                    # CHANGES
                    changes = item['changes']
                    counter_changes = 0
                    for sub_item in changes:
                        history_list.append('* Change {}'.format(counter_changes))
                        history_list.append('** removed: {}'.format(sub_item['removed']))
                        history_list.append('** added: {}'.format(sub_item['added']))
                        history_list.append('** field name: {}'.format(sub_item['field_name']))
                        counter_changes += 1
                    # WHO
                    history_list.append('* Who: {}'.format(item['who']))
                    counter_history += 1
                print('Countered histories:', counter_history - 1)
                history_list.append('\n')
                history_list.append('\n')
                history_list.append('Countered histories: {}'.format(counter_history - 1))
            else:
                # In case of error
                history_list.append('* {}'.format(data))
                # print()
        # for item in history_list:
        #     print(item)
        #     print()
        return history_list


""" CLASS: Getting data for all the bugs assigned to a particular user  """


class UserBugs:
    def __init__(self, user):
        self.user = user

    def getting_user_bugs(self):
        print()
        print('User:', self.user)
        print('------------------')
        url = 'https://bugzilla.mozilla.org/rest/bug?assigned_to={}'.format(self.user)
        r = requests.get(url)
        data = r.json()
        # pprint(data)
        bug_basic_fields_feed = []
        print()
        for bugs in data.keys():
            if bugs == 'bugs':
                bugs_counter = 1
                for item in data[bugs]:
                    bug_basic_fields_feed.append('= User Bug: {}'.format(bugs_counter))
                    # print(item.keys())
                    item_keys_list = item.keys()
                    counter_keys_basic = 0
                    # BASIC FIELDS
                    for key in item_keys_list:
                        if not key.startswith('cf'):
                            # print(key + ':', item.get(key))
                            counter_keys_basic += 1

                    bug_basic_fields_feed.append('== Basic Fields')
                    # Summary
                    bug_basic_fields_feed.append('=== Summary')
                    if item['summary'] and item['summary'] is not '':
                        bug_basic_fields_feed.append('* Summary: {}'.format(item['summary']))
                    else:
                        bug_basic_fields_feed.append('* No summary is available')
                    # Assigned to
                    bug_basic_fields_feed.append('=== Assigned to')
                    if item['assigned_to'] and item['assigned_to'] is not '':
                        # Assigned to Info
                        bug_basic_fields_feed.append('* Email: {}'.format(item['assigned_to_detail']['email']))
                        bug_basic_fields_feed.append('* ID: {}'.format(item['assigned_to_detail']['id']))
                        bug_basic_fields_feed.append('* Name: {}'.format(item['assigned_to_detail']['name']))
                        bug_basic_fields_feed.append('* Nickname: {}'.format(item['assigned_to_detail']['nick']))
                        bug_basic_fields_feed.append('* Real Name: {}'
                                                     .format(item['assigned_to_detail']['real_name']))
                    else:
                        bug_basic_fields_feed.append('No assigned user.')
                    # blocks
                    bug_basic_fields_feed.append('=== Blocks')
                    list_blocks = item['blocks']
                    if len(list_blocks) > 0:
                        counter_list_blocks = 1
                        for block_item in list_blocks:
                            bug_basic_fields_feed.append('* Block Item {}:'.format(counter_list_blocks) + ' {}'
                                                         .format(block_item))
                            counter_list_blocks += 1
                    else:
                        bug_basic_fields_feed.append('* No blocks listed at this time.')
                    # CC
                    bug_basic_fields_feed.append('=== CC')
                    list_cc = item['cc']
                    if len(list_cc) > 0:
                        counter_list_cc = 1
                        for cc in list_cc:
                            bug_basic_fields_feed.append('* CC {}:'.format(counter_list_cc) + ' {}'.format(cc))
                            counter_list_cc += 1
                        # CC Detail
                        bug_basic_fields_feed.append('=== CC Information')
                        list_cc_detail = item['cc_detail']
                        if len(list_cc_detail) > 0:
                            counter_cc_detail = 1
                            for cc_item in list_cc_detail:
                                bug_basic_fields_feed.append('* CC {} Information:'.format(counter_cc_detail))
                                bug_basic_fields_feed.append('** Email: {}'.format(cc_item['email']))
                                bug_basic_fields_feed.append('** ID: {}'.format(cc_item['id']))
                                bug_basic_fields_feed.append('** Name: {}'.format(cc_item['name']))
                                bug_basic_fields_feed.append('** Nickname: {}'.format(cc_item['nick']))
                                bug_basic_fields_feed.append('** Real Name: {}'.format(cc_item['real_name']))
                                counter_cc_detail += 1
                    else:
                        bug_basic_fields_feed.append('* No CC listed at this time.')
                    # classification
                    bug_basic_fields_feed.append('=== Classification')
                    if item['classification'] and item['classification'] is not '':
                        bug_basic_fields_feed.append('* {}'.format(item['classification']))
                    else:
                        bug_basic_fields_feed.append('* No Classification is defined at this time.')
                    # comment_count
                    bug_basic_fields_feed.append('=== Comments Counted')
                    if item['comment_count']:
                        bug_basic_fields_feed.append('* Count: ' + str(item['comment_count']))
                    else:
                        bug_basic_fields_feed.append('* No Comments are available at this time.')
                    # component
                    bug_basic_fields_feed.append('=== Component')
                    if item['component'] and item['component'] is not '':
                        bug_basic_fields_feed.append('* {}'.format(item['component']))
                    else:
                        bug_basic_fields_feed.append('* No Component is defined.')
                    # creation_time
                    bug_basic_fields_feed.append('=== Creation Time')
                    if item['creation_time'] and item['creation_time'] is not '':
                        bug_basic_fields_feed.append('* {}'.format(item['creation_time']))
                    else:
                        bug_basic_fields_feed.append('* No time of creation is available.')
                    # creator
                    bug_basic_fields_feed.append('=== Creator')
                    if item['creator'] and item['creator'] is not '':
                        bug_basic_fields_feed.append('* {}'.format(item['creator']))
                        # creator_detail
                        bug_basic_fields_feed.append('* Creator Information:')
                        bug_basic_fields_feed.append('** Email: {}'.format(item['creator_detail']['email']))
                        bug_basic_fields_feed.append('** ID: {}'.format(item['creator_detail']['id']))
                        bug_basic_fields_feed.append('** Name: {}'.format(item['creator_detail']['name']))
                        bug_basic_fields_feed.append('** Nickname: {}'.format(item['creator_detail']['nick']))
                        bug_basic_fields_feed.append('** Real Name: {}'.format(item['creator_detail']['real_name']))
                    else:
                        bug_basic_fields_feed.append('* Creator is not defined.')
                    # Depends On
                    bug_basic_fields_feed.append('=== Depends On')
                    depends_on_list = item['depends_on']
                    if len(depends_on_list) > 0:
                        counter_depends_on_list = 1
                        for depends_item in depends_on_list:
                            bug_basic_fields_feed.append('* Dependency {}'.format(counter_depends_on_list))
                            bug_basic_fields_feed.append('** {}'.format(depends_item))
                            counter_depends_on_list += 1
                    else:
                        bug_basic_fields_feed.append('* No dependencies were found.')
                    # dupe of
                    bug_basic_fields_feed.append('=== Dupe of')
                    if item['dupe_of'] and item['dupe_of'] is not None:
                        bug_basic_fields_feed.append('* {}'.format(item['dupe_of']))
                    else:
                        bug_basic_fields_feed.append('* No Dupe of information at this time.')
                    # Duplicates
                    bug_basic_fields_feed.append('=== Duplicates')
                    duplicates_list = item['duplicates']
                    if len(duplicates_list) > 0:
                        counter_duplicates_list = 1
                        for duplicates_item in duplicates_list:
                            bug_basic_fields_feed.append('* Duplicate {}'.format(counter_duplicates_list))
                            bug_basic_fields_feed.append('** {}'.format(duplicates_item))
                            counter_duplicates_list += 1
                    else:
                        bug_basic_fields_feed.append('* No listed items.')
                    # Flags
                    flags_list = item['flags']
                    bug_basic_fields_feed.append('=== Flags')
                    if len(flags_list) > 0:
                        counter_flags_list = 1
                        for flags_item in flags_list:
                            bug_basic_fields_feed.append('* Flag {}'.format(counter_flags_list))
                            bug_basic_fields_feed.append('** {}'.format(flags_item))
                            counter_flags_list += 1
                    else:
                        bug_basic_fields_feed.append('* No listed items.')
                    # Groups
                    bug_basic_fields_feed.append('=== Groups')
                    groups_list = item['groups']
                    if len(groups_list) > 0:
                        counter_groups_list = 1
                        for group_item in groups_list:
                            bug_basic_fields_feed.append('* Group {}'.format(counter_groups_list))
                            bug_basic_fields_feed.append('** {}'.format(group_item))
                            counter_groups_list += 1
                    else:
                        bug_basic_fields_feed.append('* No listed items.')
                    # ID
                    bug_basic_fields_feed.append('=== ID')
                    if item['id'] and item['id'] is not None:
                        bug_basic_fields_feed.append('* {}'.format(item['id']))
                    else:
                        bug_basic_fields_feed.append('* No ID available.')
                    # is_cc_accessible
                    bug_basic_fields_feed.append('=== Is CC Accessble')
                    bug_basic_fields_feed.append('* {}'.format(item['is_cc_accessible']))
                    # is_confirmed
                    bug_basic_fields_feed.append('=== Is Confirmed')
                    bug_basic_fields_feed.append('* {}'.format(item['is_confirmed']))
                    # is_creator_accessible
                    bug_basic_fields_feed.append('=== Is Creator Accessible')
                    bug_basic_fields_feed.append('* {}'.format(item['is_creator_accessible']))
                    # is_open
                    bug_basic_fields_feed.append('=== Is Open')
                    bug_basic_fields_feed.append('* {}'.format(item['is_open']))
                    # Keywords
                    keywords_list = item['keywords']
                    bug_basic_fields_feed.append('=== Keywords')
                    if len(keywords_list) > 0:
                        counter_keywords_list = 1
                        for keyword_item in keywords_list:
                            bug_basic_fields_feed.append('* Keyword {}'.format(counter_keywords_list))
                            bug_basic_fields_feed.append('** {}'.format(keyword_item))
                            counter_keywords_list += 1
                    else:
                        bug_basic_fields_feed.append('* No listed keywords.')
                    # last_change_time
                    bug_basic_fields_feed.append('=== Last Change Time')
                    if item['last_change_time'] and item['last_change_time'] is not '':
                        bug_basic_fields_feed.append('* {}'.format(item['last_change_time']))
                    else:
                        bug_basic_fields_feed.append('* No Last Change Time is available.')
                    # Mentors
                    bug_basic_fields_feed.append('=== Mentors Information')
                    mentors_detail_list = item['mentors_detail']
                    if len(mentors_detail_list) > 0:
                        counter_mentors_detail_list = 1
                        for mentor_item in mentors_detail_list:
                            bug_basic_fields_feed.append('* Mentor {}'.format(counter_mentors_detail_list))
                            bug_basic_fields_feed.append('** Email: {}'.format(mentor_item['email']))
                            bug_basic_fields_feed.append('** ID: {}'.format(mentor_item['id']))
                            bug_basic_fields_feed.append('** Name: {}'.format(mentor_item['name']))
                            bug_basic_fields_feed.append('** Nickname: {}'.format(mentor_item['nick']))
                            bug_basic_fields_feed.append('** Real Name: {}'.format(mentor_item['real_name']))
                            counter_mentors_detail_list += 1
                    else:
                        bug_basic_fields_feed.append('* No listed Mentors.')
                    # op_sys
                    bug_basic_fields_feed.append('=== Operation System')
                    if item['op_sys'] and item['op_sys'] is not '':
                        bug_basic_fields_feed.append('* {}'.format(item['op_sys']))
                    else:
                        bug_basic_fields_feed.append('* The operating system is not defined.')
                    # platform
                    bug_basic_fields_feed.append('=== Platform')
                    if item['platform'] and item['platform'] is not '':
                        bug_basic_fields_feed.append('* {}'.format(item['platform']))
                    else:
                        bug_basic_fields_feed.append('* The platform is not defined.')
                    # priority
                    bug_basic_fields_feed.append('=== Priority')
                    if item['priority'] and item['priority'] is not '':
                        bug_basic_fields_feed.append('* {}'.format(item['priority']))
                    else:
                        bug_basic_fields_feed.append('* The priority of the bug is not defined.')
                    # product
                    bug_basic_fields_feed.append('=== Product')
                    if item['product'] and item['product'] is not '':
                        bug_basic_fields_feed.append('* {}'.format(item['product']))
                    else:
                        bug_basic_fields_feed.append('* No product information is available.')
                    # qa_contact
                    bug_basic_fields_feed.append('=== QA Contact')
                    if item['qa_contact'] and item['qa_contact'] is not '':
                        bug_basic_fields_feed.append('* {}:'.format(item['qa_contact']))
                        # qa_contact_detail
                        bug_basic_fields_feed.append('=== QA Contact Information')
                        bug_basic_fields_feed.append('* Email: {}'.format(item['qa_contact_detail']['email']))
                        bug_basic_fields_feed.append('* ID: {}'.format(item['qa_contact_detail']['id']))
                        bug_basic_fields_feed.append('* Name: {}'.format(item['qa_contact_detail']['name']))
                        bug_basic_fields_feed.append('* Nickname: {}'.format(item['qa_contact_detail']['nick']))
                        bug_basic_fields_feed.append('* Real Name: {}'
                                                     .format(item['qa_contact_detail']['real_name']))
                    else:
                        bug_basic_fields_feed.append('*  There is no QA Contact available.')
                    # Regressed By
                    bug_basic_fields_feed.append('=== Regressed By')
                    regressed_by_list = item['regressed_by']
                    if len(regressed_by_list) > 0:
                        counter_regressed_by_list = 1
                        for regressed_by_item in regressed_by_list:
                            bug_basic_fields_feed.append('* Regressed by {}'.format(counter_regressed_by_list))
                            bug_basic_fields_feed.append('** {}'.format(regressed_by_item))
                            counter_regressed_by_list += 1
                    else:
                        bug_basic_fields_feed.append('* No listed items.')
                    # regressions
                    bug_basic_fields_feed.append('=== Regressions')
                    regressions_list = item['regressions']
                    if len(regressions_list) > 0:
                        counter_regressions_list = 1
                        for regression_item in regressions_list:
                            bug_basic_fields_feed.append('* Regression {}'.format(counter_regressions_list))
                            bug_basic_fields_feed.append('** {}'.format(regression_item))
                            counter_regressions_list += 1
                    else:
                        bug_basic_fields_feed.append('* No listed items.')
                    # resolution
                    bug_basic_fields_feed.append('=== Resolution')
                    if item['resolution'] and item['resolution'] is not '':
                        bug_basic_fields_feed.append('* {}'.format(item['resolution']))
                    else:
                        bug_basic_fields_feed.append('* No resolution is defined.')
                    # see also
                    bug_basic_fields_feed.append('=== See Also')
                    see_also_list = item['see_also']
                    if len(see_also_list) > 0:
                        counter_see_also_list = 1
                        for see_item in see_also_list:
                            bug_basic_fields_feed.append('* See {}'.format(counter_see_also_list))
                            bug_basic_fields_feed.append('** {}'.format(see_item))
                            counter_see_also_list += 1
                    else:
                        bug_basic_fields_feed.append('* No listed items.')
                    # severity
                    bug_basic_fields_feed.append('=== Severity')
                    if item['severity'] and item['severity'] is not '':
                        bug_basic_fields_feed.append('* {}'.format(item['severity']))
                    else:
                        bug_basic_fields_feed.append('* Severity is not defined.')
                    # status
                    bug_basic_fields_feed.append('=== Status')
                    if item['status'] and item['status'] is not '':
                        bug_basic_fields_feed.append('* {}'.format(item['status']))
                    else:
                        bug_basic_fields_feed.append('* Status is not available.')
                    # Target milestone
                    bug_basic_fields_feed.append('=== Target Milestone')
                    if item['target_milestone'] and item['target_milestone'] is not '---':
                        bug_basic_fields_feed.append('* {}'.format(item['target_milestone']))
                    else:
                        bug_basic_fields_feed.append('* No target milestone is available.')
                    # type
                    bug_basic_fields_feed.append('=== Type')
                    if item['type'] and item['type'] is not '':
                        bug_basic_fields_feed.append('* {}'.format(item['type']))
                    else:
                        bug_basic_fields_feed.append('* No bug type is available.')
                    # url
                    bug_basic_fields_feed.append('=== URL')
                    if item['url'] and item['url'] is not '':
                        bug_basic_fields_feed.append('* {}'.format(item['url']))
                    else:
                        bug_basic_fields_feed.append('* No URL is defined')
                    # version
                    bug_basic_fields_feed.append('=== Version')
                    if item['version'] and item['version'] is not '':
                        bug_basic_fields_feed.append('* {}'.format('* {}'.format(item['version'])))
                    else:
                        bug_basic_fields_feed.append('* No version is defined')
                    # votes
                    bug_basic_fields_feed.append('=== Votes')
                    if item['votes']:
                        bug_basic_fields_feed.append('* {}'.format(item['votes']))
                    else:
                        bug_basic_fields_feed.append('* No votes are defined.')
                    # whiteboard
                    bug_basic_fields_feed.append('=== Whiteboard')
                    if item['whiteboard'] and item['whiteboard'] is not '':
                        bug_basic_fields_feed.append('* {}'.format(item['whiteboard']))
                    else:
                        bug_basic_fields_feed.append('* Whiteboard is not available')
                    # alias
                    bug_basic_fields_feed.append('=== Alias')
                    if item['alias'] and item['alias'] is not None:
                        bug_basic_fields_feed.append('* {}'.format(item['alias']))
                    else:
                        bug_basic_fields_feed.append('* No alias is specified')
                    # print('Countered Basic Fields:', counter_keys_basic)
                    # print('--')
                    # CUSTOM FIELDS
                    bug_basic_fields_feed.append('== Custom Fields')
                    counter_keys_cf = 0
                    for key in item_keys_list:
                        if key.startswith('cf'):
                            bug_basic_fields_feed.append('* {}'.format(key) + ': {}'.format(item.get(key)))
                            counter_keys_cf += 1
                    # print()
                    # print('Countered Custom Fields:', counter_keys_cf)
                    bugs_counter += 1
                print('Bugs counted:', bugs_counter - 1)
                print()
            else:
                # in case of error
                # print(data)
                bug_basic_fields_feed.append(data)
        # print()
        # for item in bug_basic_fields_feed:
        #     print(item)
        #     print()
        # print()
        return bug_basic_fields_feed


"""CLASS: Getting data for a user """


class UserInfo:
    def __init__(self, user):
        self.user = user

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
        url = 'https://bugzilla.mozilla.org/rest/user?names={}'.format(self.user)
        # u = url + "?token={}".format(self.key)
        r = requests.get(url)
        data = r.json()
        # pprint(data)
        user_info_list.append('== User Information')
        for user in data.keys():
            if user == 'users':
                for item in data[user]:
                    print('User Info')
                    user_info_list.append('=== User')
                    keys_list = item.keys()
                    for field in keys_list:
                        print('\t' + field + ':', item.get(field))
                        user_info_list.append('* {}'.format(field) + ': {}'.format(item.get(field)))
            else:
                pprint(data)
                user_info_list.append('* {}'.format(data))
        # print()
        # for item in user_info_list:
        #     print(item)
        #     print()
        return user_info_list
