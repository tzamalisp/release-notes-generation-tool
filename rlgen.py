import logging
import sys
import configparser
from argparse import ArgumentParser
import os

from trackers.bugzilla_requester import TargetReleaseBugzilla
from trackers.bugzilla_requester import DataRetriever

from trackers.jira_requester import TargetReleaseJira
from trackers.jira_requester import IssueDataRetrieverJira

from asciidoc_generator import GeneratorJira
from asciidoc_generator import GeneratorBugzillaReport



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
                 bug_function):
        self.tracker = tracker
        self.issue = issue
        self.user = user
        self.custom_field_name = custom_field_name
        self.custom_field_id = custom_field_id
        self.bug_function = bug_function
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
            release_name = config['jira_target_release']['name']
            if release_name is '':
                release_name = None
            path = config['path']['directory']
            if path is '':
                path = None

            # calling the class for making the the Target Release notes object
            # self.release_note is type of list
            release_notes = TargetReleaseJira(release_name=release_name,
                                              release=self.release_note,
                                              order=self.order)

            # calling the basic class for collecting the corresponding data from the bugzilla rest api
            # functions: bug info, bug comments, bug history, user info, user assigned bugs
            issue_object = IssueDataRetrieverJira(issue=self.issue,
                                                  terms=None,
                                                  cf_name=None,
                                                  cf_id=None)

            report_field = 'No report field is specified.'
            data_report = ['* No data were fetched from the REST API.']

            # JIRA RELEASE NOTES
            if self.bug_function is 'r' or self.bug_function is 'R':
                if release_name is not None and self.release_note is not None:
                    print(self.release_note)
                    report_field = 'TargetReleases'
                    release_notes_data = release_notes.get_release_notes()
                    data_report = release_notes_data
                else:
                    if self.release_note is None:
                        print('Please define at least a Release Note to search for..')
                        logger_rlgen.warning('Please define at least a Release Note with the -r argument.')
                        raise Exception('Please define at least a Release Note with the -r argument.')
                    elif release_name is None:
                        print(
                            'Please define the Release Name field of the custom field of JIRA inside the configuration '
                            'file.')
                        raise Exception('Please define the Release Name field of the custom field of JIRA inside the '
                                        'configuration file')
                    else:
                        print('Both Release Name and Release notes fields are note defined.')
            elif self.bug_function is 'b' or self.bug_function is 'B':
                if self.issue is not None:
                    report_field = 'BugInfo'
                    issue_data = issue_object.get_data()
                    issue_info_data = issue_object.get_basic_issue_data(issue_data)
                    data_report = issue_info_data
                else:
                    print('Please define an issue.')
            elif self.bug_function is 'c' or self.bug_function is 'C':
                if self.issue is not None:
                    report_field = 'BugComments'
                    issue_data = issue_object.get_data()
                    issue_comments_data = issue_object.getting_comments_data(issue_data)
                    data_report = issue_comments_data
                else:
                    print('Please define an issue.')
            else:
                print('Please enter a valid letter for function:\n'
                      '-f r: Release Note\n'
                      '-f c: Bug Comments\n')
            # MAKING DOC REPORT -> ASCIIDOC
            doc_basic = GeneratorJira(kind_of_report=report_field,
                                      releases=self.release_note,
                                      user=user_name,
                                      bug=self.issue,
                                      firstname=first_name,
                                      lastname=last_name,
                                      email_account=email,
                                      data_basic=data_report,
                                      path=path)
            doc_basic.generating_doc_jira()

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

            # calling the class for making the the Target Release notes object
            # self.release_note is type of list
            release_notes = TargetReleaseBugzilla(self.release_note, self.custom_field_name)

            # calling the basic class for collecting the corresponding data from the bugzilla rest api
            # functions: bug info, bug comments, bug history, user info, user assigned bugs
            data_object = DataRetriever(bug_id=self.issue,
                                        terms=self.custom_field_name,
                                        user=self.user)

            report_field = 'No report field is specified.'
            data_report = ['* No data were fetched from the REST API.']

            # FUNCTIONS: -f --function
            # release notes
            if self.bug_function is 'r' or self.bug_function is 'R':
                if self.release_note is not None:
                    report_field = 'TargetReleases'
                    release_notes_data = release_notes.getting_target_release_notes()
                    # bug release notes
                    data_report = release_notes_data
                else:
                    print('Please define a release note.')
            # bug info
            elif self.bug_function is 'b' or self.bug_function is 'b':
                if self.issue is not None:
                    report_field = 'BugInfo'
                    bug_info = data_object.getting_bug_info()
                    bug_info_data = data_object.data_retriever(bug_info['retrieve'],
                                                               bug_info['data_output'],
                                                               bug_info['search_list_output'],
                                                               bug_info['ascii_bug_info_list'])
                    # bug info
                    data_report = bug_info_data
                else:
                    print('Please define a correct Bug ID.')
            # user assigned bugs
            elif self.bug_function is 'a' or self.bug_function is 'A':
                if self.user is not None:
                    report_field = 'UserAssignedBugs'
                    user_assigned_bugs = data_object.getting_user_assigned_bugs()
                    user_assigned_bugs_data = data_object.data_retriever(
                        retrieval=user_assigned_bugs['retrieve'],
                        data=user_assigned_bugs['data_output'],
                        search_list=user_assigned_bugs['search_list_output'],
                        ascii_doc_data=user_assigned_bugs['ascii_user_assigned_bugs_list'])
                    # user assigned bugs doc
                    data_report = user_assigned_bugs_data
                else:
                    print('Please define a username or user email.')
            # user info
            elif self.bug_function is 'u' or self.bug_function is 'U':
                if self.user is not None:
                    report_field = 'UserInfo'
                    user_info = data_object.getting_user_info()
                    user_info_data = data_object.data_retriever(retrieval=user_info['retrieve'],
                                                                data=user_info['data_output'],
                                                                search_list=user_info['search_list_output'],
                                                                ascii_doc_data=user_info['ascii_user_info_list'])
                    # user info doc
                    data_report = user_info_data
                else:
                    print('Please define a username or user email.')
            # bug comments
            elif self.bug_function is 'c' or self.bug_function is 'C':
                if self.issue is not None:
                    report_field = 'BugComments'
                    bug_comments = data_object.getting_bug_comments()
                    bug_comments_data = data_object.data_retriever(retrieval=bug_comments['retrieve'],
                                                                   data=bug_comments['data_output'],
                                                                   search_list=bug_comments['search_list_output'],
                                                                   ascii_doc_data=bug_comments['ascii_bug_comments_list'])
                    # bug comments doc
                    data_report = bug_comments_data
                else:
                    print('Please define a correct Bug ID.')
            # bug history
            elif self.bug_function is 'h' or self.bug_function is 'H':
                if self.issue is not None:
                    report_field = 'BugHistory'
                    bug_history = data_object.getting_bug_history()
                    bug_history_data = data_object.data_retriever(retrieval=bug_history['retrieve'],
                                                                  data=bug_history['data_output'],
                                                                  search_list=bug_history['search_list_output'],
                                                                  ascii_doc_data=bug_history['ascii_bug_history_list'])
                    # bug history doc
                    data_report = bug_history_data
            else:
                print('Please enter a valid letter for function:\n'
                      '-f r: Release Note\n'
                      '-f u: User Information\n'
                      '-f b: Bug Information\n'
                      '-f c: Bug Comments\n'
                      '-f h: Bug History\n'
                      '-f a: Bugs Assigned to a User')

            report = GeneratorBugzillaReport(kind_of_report=report_field,
                                             releases=self.release_note,
                                             bug=self.issue,
                                             user=self.user,
                                             username=user_name,
                                             firstname=first_name,
                                             lastname=last_name,
                                             email_account=email,
                                             data_basic=data_report,
                                             path=path)
            report.generating_doc_bugzilla()
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
                                       order=tracker_issue_selection['order_ascending'],
                                       release_note=tracker_issue_selection['release_note'])

    tracker_choice.tracker_selection()
    print()
    print('Terminating..')


