import logging
import sys
import configparser
from argparse import ArgumentParser
import os

from trackers.bugzilla_requester import BugRetriever
from trackers.bugzilla_requester import Comments
from trackers.bugzilla_requester import History
from trackers.bugzilla_requester import UserBugs
from trackers.bugzilla_requester import UserInfo

from trackers.bugzilla_requester_new import TargetReleaseBugzilla
from trackers.bugzilla_requester_new import DataRetriever

from trackers.jira_requester_issue import BasicDataRetriever
from trackers.jira_requester_issue import CustomFieldDataRetriever
from trackers.jira_requester_release_notes import TargetRelease

from asciidoc_generator import GeneratorJiraReleaseNotes
from asciidoc_generator import GeneratorJira
from asciidoc_generator import GeneratorBugzillaReleaseNotes
from asciidoc_generator import GeneratorBugzillaBug
from asciidoc_generator import GeneratorBugzillaBugComments
from asciidoc_generator import GeneratorBugzillaBugHistory
from asciidoc_generator import GeneratorBugzillaUserBugs
from asciidoc_generator import GeneratorBugzillaUserInfo



# create and configure a logger
LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging_file = logging.basicConfig(filename='log/rlgen.log',
                                   level=logging.DEBUG,
                                   format=LOG_FORMAT,
                                   filemode='w')

# root logger (without name)
logger_rlgen = logging.getLogger()

current_d = os.getcwd()
# print(current_d)
directories_list = current_d.split('/')
# print(directories_list)
# print(directories_list[1:4])
basic_desktop_path = directories_list[1:4]
new_path = 'conf/'
basic_desktop_path.append(new_path)
conf_path = '/' + '/'.join(basic_desktop_path)


""" USER CHOICE OF ISSUE TRACKING PLATFORM """


class UserTrackerChoice:
    def __init__(self, tracker, issue, release_note, order, user, custom_field_name, custom_field_id,
                 bug_function, user_operation):
        self.tracker = tracker
        self.issue = issue
        self.user = user
        self.custom_field_name = custom_field_name
        self.custom_field_id = custom_field_id
        self.bug_function = bug_function
        self.user_operation = user_operation
        self.release_note = release_note
        self.order = order

    def tracker_selection(self):
        # JIRA
        if self.tracker is 'J' or self.tracker is 'j':
            logger_rlgen.debug('---------------------------JIRA------------------------------------')
            print('Entered JIRA environment')
            logger_rlgen.debug('Entered JIRA environment')
            # # CONNECTION TO JIRA
            # logger.debug('CONNECTION TO JIRA')
            # test_connector = Connector()
            # test_connector.jira_connector()

            config = configparser.ConfigParser()
            config.read('{}config.conf'.format(conf_path))
            user_name = config['jira_basic_auth']['username']
            first_name = config['author']['firstname']
            last_name = config['author']['lastname']
            email = config['author']['email']
            release_name = config['release']['name']
            if release_name is '':
                release_name = None
            path = config['path']['directory']
            if path is '':
                path = None

            # BASIC JIRA DATA RETRIEVER
            if self.issue is not None:
                logger_rlgen.debug('BASIC DATA RETRIEVER OBJECT')
                jira_basic_data = BasicDataRetriever(self.issue)
                # CUSTOM FIELD DATA RETRIEVER
                logger_rlgen.debug('CUSTOM FIELD DATA RETRIEVER OBJECT')
                jira_custom_field_data = CustomFieldDataRetriever(self.issue,
                                                                  self.custom_field_name,
                                                                  self.custom_field_id)

                # doc basic + custom fields
                logger_rlgen.debug('JIRA Doc including Basic + Custom Fields')
                doc_basic = GeneratorJira(user=user_name,
                                          bug=self.issue,
                                          firstname=first_name,
                                          lastname=last_name,
                                          email_account=email,
                                          data_basic=jira_basic_data.data_retriever(),
                                          data_custom=jira_custom_field_data.data_retriever(),
                                          path=path)
                doc_basic.generating_doc_jira()

                logger_rlgen.debug('>>> Calling JIRA API and printing Issue parts is now completed successfully!')
            elif release_name is not None and self.release_note is not None:
                print(self.release_note)
                jira_release_notes = TargetRelease(release_name=release_name,
                                                   release=self.release_note,
                                                   order=self.order)
                doc_release_notes = GeneratorJiraReleaseNotes(user=user_name,
                                                              release_name=release_name,
                                                              release=self.release_note,
                                                              firstname=first_name,
                                                              lastname=last_name,
                                                              email_account=email,
                                                              data_basic=jira_release_notes.get_release_notes(),
                                                              path=path)
                doc_release_notes.generating_doc_jira()
            else:
                if self.release_note is None:
                    print('Please define at least a Release Note to search for..')
                    logger_rlgen.warning('Please define at least a Release Note with the -r argument.')
                    raise Exception('Please define at least a Release Note with the -r argument.')
                elif release_name is None:
                    print('Please define the Release Name field of the custom field of JIRA inside the configuration '
                          'file.')
                    raise Exception('Please define the Release Name field of the custom field of JIRA inside the '
                                    'configuration file')

        # BUGZILLA
        elif self.tracker is 'B' or self.tracker is 'b':
            logger_rlgen.debug('---------------------------------BUGZILLA------------------------------------')
            print('Entered Bugzilla environment')
            config = configparser.ConfigParser()
            config.read('{}config.conf'.format(conf_path))
            user_name = config['bugzilla_basic_auth']['username']
            first_name = config['author']['firstname']
            last_name = config['author']['lastname']
            email = config['author']['email']
            path = config['path']['directory']
            if path is '':
                path = None

            # calling the class for the Target Releases

            # calling the basic class for collecting the corresponding data from the bugzilla rest api
            data_object = DataRetriever(bug_id=self.issue,
                                        terms=self.custom_field_name,
                                        user=self.user)

            # FUNCTIONS: -f --function
            # release notes
            if self.bug_function is 'r' or self.bug_function is 'R':
                if self.release_note is not None:
                    release_notes = TargetReleaseBugzilla(self.release_note, self.custom_field_name)
                    release_notes_data = release_notes.getting_target_release_notes()
                    doc_release_note = GeneratorBugzillaReleaseNotes(user=user_name,
                                                                     firstname=first_name,
                                                                     lastname=last_name,
                                                                     email_account=email,
                                                                     data_basic=release_notes_data,
                                                                     path=path)
                    doc_release_note.generating_doc_bugzilla()
                else:
                    print('Please define a release note.')
            # bug info
            elif self.bug_function is 'b' or self.bug_function is 'B':
                if self.issue is not None:
                    bug_info = data_object.getting_bug_info()
                    bug_info_data = data_object.data_retriever(bug_info['retrieve'],
                                                               bug_info['data_output'],
                                                               bug_info['search_list_output'],
                                                               bug_info['ascii_bug_info_list'])
                    # bug doc
                    doc_bug = GeneratorBugzillaBug(user=user_name,
                                                   bug=self.issue,
                                                   firstname=first_name,
                                                   lastname=last_name,
                                                   email_account=email,
                                                   data_basic=bug_info_data,
                                                   path=path)
                    doc_bug.generating_doc_bugzilla()
                else:
                    print('Please define a correct Bug ID.')
            # user assigned bugs
            elif self.bug_function is 'a' or self.bug_function is 'A':
                if self.user is not None:
                    user_assigned_bugs = data_object.getting_user_assigned_bugs()
                    user_assigned_bugs_data = data_object.data_retriever(retrieval=user_assigned_bugs['retrieve'],
                                                                         data=user_assigned_bugs['data_output'],
                                                                         search_list=user_assigned_bugs['search_list_output'],
                                                                         ascii_doc_data=user_assigned_bugs['ascii_user_assigned_bugs_list'])
                    doc_user_bugs = GeneratorBugzillaUserBugs(user=self.user,
                                                              firstname=first_name,
                                                              lastname=last_name,
                                                              email_account=email,
                                                              data_bugs_user=user_assigned_bugs_data,
                                                              path=path)
                    doc_user_bugs.generating_doc_user_bugs()
                else:
                    print('Please define a username or user email.')
            # user info
            elif self.bug_function is 'u' or self.bug_function is 'U':
                if self.user is not None:
                    user_info = data_object.getting_user_info()
                    user_info_data = data_object.data_retriever(retrieval=user_info['retrieve'],
                                                                data=user_info['data_output'],
                                                                search_list=user_info['search_list_output'],
                                                                ascii_doc_data=user_info['ascii_user_info_list'])
                    doc_user_info = GeneratorBugzillaUserInfo(user=self.user,
                                                              firstname=first_name,
                                                              lastname=last_name,
                                                              email_account=email,
                                                              data_user=user_info_data,
                                                              path=path)
                    doc_user_info.generating_doc_user_info()
                else:
                    print('Please define a username or user email.')
            # bug comments
            elif self.bug_function is 'c' or self.bug_function is 'C':
                if self.issue is not None:
                    bug_comments = data_object.getting_bug_comments()
                    bug_comments_data = data_object.data_retriever(retrieval=bug_comments['retrieve'],
                                                                   data=bug_comments['data_output'],
                                                                   search_list=bug_comments['search_list_output'],
                                                                   ascii_doc_data=bug_comments['ascii_bug_comments_list'])
                    doc_bug_comments = GeneratorBugzillaBugComments(user=user_name,
                                                                    bug=self.issue,
                                                                    firstname=first_name,
                                                                    lastname=last_name,
                                                                    email_account=email,
                                                                    data_comments=bug_comments_data,
                                                                    path=path)
                    doc_bug_comments.generating_doc_bug_comments()
                else:
                    print('Please define a correct Bug ID.')
            # bug history
            elif self.bug_function is 'h' or self.bug_function is 'H':
                if self.issue is not None:
                    bug_history = data_object.getting_bug_history()
                    bug_history_data = data_object.data_retriever(retrieval=bug_history['retrieve'],
                                                                  data=bug_history['data_output'],
                                                                  search_list=bug_history['search_list_output'],
                                                                  ascii_doc_data=bug_history['ascii_bug_history_list'])
                    doc_bug_history = GeneratorBugzillaBugHistory(user=user_name,
                                                                  bug=self.issue,
                                                                  firstname=first_name,
                                                                  lastname=last_name,
                                                                  email_account=email,
                                                                  data_bug_history=bug_history_data,
                                                                  path=path)
                    doc_bug_history.generating_doc_bug_history()
            else:
                print('Please enter a valid letter for function:\n'
                      '-f r: Release Note\n'
                      '-f u: User Information\n'
                      '-f b: Bug Information\n'
                      '-f c: Bug Comments\n'
                      '-f h: Bug History\n'
                      '-f a: Bugs Assigned to a User')
        else:
            print('Please press a valid letter ("J" or "j" for JIRA / "B" or "b" for Bugzilla) '
                  'for choosing your tracker.')
            logger_rlgen.warning('Please press a valid letter ("J" or "j" for JIRA / "B" or "b" for Bugzilla) '
                                 'for choosing your tracker.')


""" USER TERMINAL INPUTS """


def user_input(argv):

    parser = ArgumentParser()

    parser.add_argument("-t", "--tracker",
                        dest="tracker",
                        help="add the tracker you want to search the issue: 'j' or 'J' for Jira | "
                             "'b' or 'B' for Bugzilla",
                        metavar="<TRACKER_VALUE>")
    parser.add_argument("-i", "--issue",
                        dest="issue",
                        help="add the issue ID",
                        metavar="<ISSUE_ID>")
    parser.add_argument("-n", "--name",
                        dest="custom_field_name",
                        action='append',
                        help="Define the customfield name",
                        # required=True,
                        metavar="<CUSTOMFIELD_NAME>")
    parser.add_argument("-c", "--customfieldid",
                        dest="custom_field_id",
                        nargs='+',
                        help="Define the customfield ID number",
                        metavar="<CUSTOMFIELD_ID>",
                        type=int)
    parser.add_argument("-u", "--user",
                        dest="user",
                        help="add the user you want to search for",
                        metavar="<USER_NAME>")
    parser.add_argument("-o", "--operation",
                        dest="operation",
                        help="add the operation you want to use for Bugzilla User (b: user bugs, i: user information)",
                        metavar="<USER_OPERATION>")
    parser.add_argument("-f", "--function",
                        dest="function",
                        help="add the function you want to use for Bugzilla (i: bug information, c: bug comments, "
                             "h: bug history)",
                        metavar="<BUG_FUNCTION>")
    parser.add_argument("-d", "--debug",
                        dest="debug_level",
                        help="add the level of debugging (0: DEBUG, 1: INFO, 2: WARNING)",
                        metavar="<DEBUG_LEVEL>")
    parser.add_argument("-r", "--release",
                        dest="release_note",
                        nargs='+',
                        help="add the Target Release Name separated with the space character, inside quotes)",
                        metavar="<TARGET_RELEASE_NAME>",
                        type=str)
    parser.add_argument("-a", "--ascending",
                        dest="order_ascending",
                        help="add the operation you want for ascending/descending (a: ascending, b: descending)",
                        metavar="<USER_OPERATION>")

    # parser.add_argument("-p", "--path",
    #                     dest="path",
    #                     help="add the path directory yoy want to save the Asciidoc export files",
    #                     metavar="<PATH>")

    # ARGUMENTS --> extra
    parser.add_argument("-q", "--quiet",
                        action="store_false",
                        dest="verbose",
                        default=True,
                        help="don't print status messages to stdout")

    # arguments parser creation object
    arguments = parser.parse_args()
    # print(">>>> Print when a value is empty:", arguments.user)
    # print('Print custom field names', arguments.custom_field_name)
    # print('>>>> Print list customfield IDs:', arguments.custom_field_id)
    return {'tracker': arguments.tracker,
            'issue': arguments.issue,
            'user': arguments.user,
            'custom_field_name': arguments.custom_field_name,
            'custom_field_id': arguments.custom_field_id,
            'bug_function': arguments.function,
            'user_operation': arguments.operation,
            'debug_level': arguments.debug_level,
            'order_ascending': arguments.order_ascending,
            'release_note': arguments.release_note}


if __name__ == '__main__':
    logger_rlgen.debug('Hello Tracker!')
    tracker_issue_selection = user_input(sys.argv[1:])
    # User Choice
    tracker_choice = UserTrackerChoice(tracker=tracker_issue_selection['tracker'],
                                       issue=tracker_issue_selection['issue'],
                                       user=tracker_issue_selection['user'],
                                       custom_field_name=tracker_issue_selection['custom_field_name'],
                                       custom_field_id=tracker_issue_selection['custom_field_id'],
                                       bug_function=tracker_issue_selection['bug_function'],
                                       user_operation=tracker_issue_selection['user_operation'],
                                       order=tracker_issue_selection['order_ascending'],
                                       release_note=tracker_issue_selection['release_note'])

    tracker_choice.tracker_selection()
    print()
    print('Terminating..')


