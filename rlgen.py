import logging
import sys
import configparser
from argparse import ArgumentParser

from trackers.bugzilla_requester import BugRetriever
from trackers.bugzilla_requester import Comments
from trackers.bugzilla_requester import History
from trackers.bugzilla_requester import UserBugs
from trackers.bugzilla_requester import UserInfo

from trackers.jira_requester import BasicDataRetriever
from trackers.jira_requester import CustomFieldDataRetriever

from asciidoc_generator import GeneratorJira
from asciidoc_generator import GeneratorBugzillaBug
from asciidoc_generator import GeneratorBugzillaBugComments
from asciidoc_generator import GeneratorBugzillaBugHistory
from asciidoc_generator import GeneratorBugzillaUserBugs
from asciidoc_generator import GeneratorBugzillaUserInfo

from conf.configuration import BugzillaReadConfigurationBasicAuth

# create and configure a logger
LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging_file = logging.basicConfig(filename='log/rlgen.log', level=logging.DEBUG, format=LOG_FORMAT, filemode='w')

# root logger (without name)
logger_rlgen = logging.getLogger()


""" USER CHOICE OF ISSUE TRACKING PLATFORM """


class UserTrackerChoice:
    def __init__(self, tracker, issue, user, custom_field_name, custom_field_id, bug_function, user_operation):
        self.tracker = tracker
        self.issue = issue
        self.user = user
        self.custom_field_name = custom_field_name
        self.custom_field_id = custom_field_id
        self.bug_function = bug_function
        self.user_operation = user_operation

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
            config.read('conf/config.conf')
            user_name = config['jira_basic_auth']['username']
            first_name = config['author']['firstname']
            last_name = config['author']['lastname']
            email = config['author']['email']
            path = config['path']['directory']
            if path is '':
                path = None

            # BASIC DATA RETRIEVER
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
            else:
                print('Please define an issue to search for..')
                logger_rlgen.warning('Please define an issue with the -i argument.')
                raise Exception('Please define an issue with the -i argument.')

        # BUGZILLA
        elif self.tracker is 'B' or self.tracker is 'b':
            logger_rlgen.debug('---------------------------------------BUGZILLA----------------------------------------')
            print('Entered Bugzilla environment')
            config = configparser.ConfigParser()
            config.read('conf/config.conf')
            user_name = config['bugzilla_basic_auth']['username']
            first_name = config['author']['firstname']
            last_name = config['author']['lastname']
            email = config['author']['email']
            path = config['path']['directory']
            if path is '':
                path = None

            # creating the objects for retrieving the information from the API and printing the fetched data
            if self.issue is None and self.user is None:
                print('Please define an issue or a user to search for..')
                raise Exception('Please define an issue with the -i argument OR a user with the -u argument.')
            else:
                # BUG INFO
                # BUG FUNCTIONS
                # Bug ID test to searching for in the REST API: 1144467
                if self.issue is not None:
                    if self.bug_function is not None:
                        if self.bug_function is 'i' or self.bug_function is 'I':
                            # bug data
                            bug_fetcher = BugRetriever(bug_id=self.issue)
                            # bug doc
                            doc_bug = GeneratorBugzillaBug(user=user_name,
                                                           bug=self.issue,
                                                           firstname=first_name,
                                                           lastname=last_name,
                                                           email_account=email,
                                                           data_basic=bug_fetcher.data_retriever(),
                                                           path=path)
                            doc_bug.generating_doc_bugzilla()
                        elif self.bug_function is 'c' or self.bug_function is 'C':
                            # bug comments
                            get_comments = Comments(bug_id=self.issue)
                            # bug comments doc
                            doc_bug_comments = GeneratorBugzillaBugComments(user=user_name,
                                                                            bug=self.issue,
                                                                            firstname=first_name,
                                                                            lastname=last_name,
                                                                            email_account=email,
                                                                            data_comments=get_comments.getting_comments(),
                                                                            path=path)
                            doc_bug_comments.generating_doc_bug_comments()

                        elif self.bug_function is 'h' or self.bug_function is 'H':
                            # bug history
                            get_history = History(bug_id=self.issue)
                            # bug history doc
                            doc_bug_history = GeneratorBugzillaBugHistory(user=user_name,
                                                                          bug=self.issue,
                                                                          firstname=first_name,
                                                                          lastname=last_name,
                                                                          email_account=email,
                                                                          data_bug_history=get_history.getting_history(),
                                                                          path=path)
                            doc_bug_history.generating_doc_bug_history()
                        else:
                            print('Please enter a valid letter for function:\n'
                                  '-f i: Bug Issue ID\n'
                                  '-f c: Bug Comments\n'
                                  '-f h: Bug History')
                            raise Exception('Enter a valid value for that argument.')

                # USER INFO
                # USER OPERATIONS
                # user_name test to searching for in the REST API: lhenry@mozilla.com
                if self.user is not None:
                    if self.user_operation is not None:
                        if self.user_operation is 'b' or self.user_operation is 'B':
                            # bugs related to a user
                            user_bugs = UserBugs(user='lhenry@mozilla.com')
                            # user bugs doc
                            doc_user_bugs = GeneratorBugzillaUserBugs(user=self.user,
                                                                      firstname=first_name,
                                                                      lastname=last_name,
                                                                      email_account=email,
                                                                      data_bugs_user=user_bugs.getting_user_bugs(),
                                                                      path=path)
                            doc_user_bugs.generating_doc_user_bugs()
                        elif self.user_operation is 'i' or self.user_operation is 'I':
                            # user information
                            user_info = UserInfo(user=self.user)
                            # user information
                            doc_user_info = GeneratorBugzillaUserInfo(user=self.user,
                                                                      firstname=first_name,
                                                                      lastname=last_name,
                                                                      email_account=email,
                                                                      data_user=user_info.getting_user_info(),
                                                                      path=path)
                            doc_user_info.generating_doc_user_info()
                        else:
                            print('Please enter a valid letter for User operation:\n'
                                  '-o b: User Bugs\n'
                                  '-o i: User Information\n')
                            logger_rlgen.warning('Please enter a valid letter for User operation:\n'
                                                 '-o b: User Bugs\n'
                                                 '-o i: User Information\n')
                            raise Exception('Enter a valid value for that argument.')

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
                        help="Define the customfield name - <Required> Set flag",
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
            'user_operation': arguments.operation}


if __name__ == '__main__':
    logger_rlgen.debug('Hello Tracker!')
    tracker_issue_selection = user_input(sys.argv[1:])
    # User Choice
    tracker_choice = UserTrackerChoice(tracker_issue_selection['tracker'],
                                       tracker_issue_selection['issue'],
                                       tracker_issue_selection['user'],
                                       tracker_issue_selection['custom_field_name'],
                                       tracker_issue_selection['custom_field_id'],
                                       tracker_issue_selection['bug_function'],
                                       tracker_issue_selection['user_operation'])
    tracker_choice.tracker_selection()
    print()
    print('Terminating..')


