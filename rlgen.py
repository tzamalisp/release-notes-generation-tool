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
from trackers.jira_requester import Connector

from asciidoc_generator import GeneratorJira
from asciidoc_generator import GeneratorBugzillaBug
from asciidoc_generator import GenratorBugzillaBugComments
from asciidoc_generator import GeneratorBugzillaBugHistory
from asciidoc_generator import GeneratorBugzillaUserBugs
from asciidoc_generator import GeneratorBuzillaUserInfo

from conf.configuration import BugzillaReadConfigurationBasicAuth

# create and configure a logger
LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging_file = logging.basicConfig(filename='log/rlgen.log', level=logging.DEBUG, format=LOG_FORMAT, filemode='w')


""" USER CHOICE OF ISSUE TRACKING PLATFORM """
# root logger (without name)
logger = logging.getLogger()


class UserTrackerChoice:
    def __init__(self, tracker, issue, user, custom_field_name, custom_field_id):
        self.tracker = tracker
        self.issue = issue
        self.user = user
        self.custom_field_name = custom_field_name
        self.custom_field_id = custom_field_id

    def tracker_selection(self):

        if self.tracker is 'J' or self.tracker is 'j':
            print('Entered JIRA environment')
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
            # custom_field_name = config['author']['customfield_name']
            # custom_field_id = int(config['author']['customfield_id'])

            # BASIC DATA RETRIEVER
            logger.debug('BASIC DATA RETRIEVER OBJECT')
            jira_basic_data = BasicDataRetriever(self.issue)
             # CUSTOM FIELD DATA RETRIEVER
            logger.debug('CUSTOM FIELD DATA RETRIEVER OBJECT')
            jira_custom_field_data = CustomFieldDataRetriever(self.issue, self.custom_field_name, self.custom_field_id)

            # doc basic + custom fields
            logger.debug('JIRA Doc including Basic + Custom Fields')
            doc_basic = GeneratorJira(user=user_name,
                                      bug=self.issue,
                                      firstname=first_name,
                                      lastname=last_name,
                                      email_account=email,
                                      data_basic=jira_basic_data.data_retriever(),
                                      data_custom=jira_custom_field_data.data_retriever())
            doc_basic.generating_doc_jira()

            logger.debug('>>> Calling JIRA API and printing Issue parts is now completed successfully!')

        elif self.tracker is 'B' or self.tracker is 'b':
            print('Entered Bugzilla environment')
            bugzilla_basic_auth = BugzillaReadConfigurationBasicAuth()
            print(bugzilla_basic_auth.username)
        else:
            print('Please press a valid letter ("J" or "j" for JIRA / "B" or "b" for Bugzilla) '
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
                        required=True,
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
                        metavar="<USER NAME>")
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
    return {'tracker': arguments.tracker, 'issue': arguments.issue, 'user': arguments.user,
            'custom_field_name': arguments.custom_field_name, 'custom_field_id': arguments.custom_field_id}


if __name__ == '__main__':
    tracker_issue_selection = user_input(sys.argv[1:])
    # User Choice
    tracker_choice = UserTrackerChoice(tracker_issue_selection['tracker'], tracker_issue_selection['issue'],
                                       tracker_issue_selection['user'], tracker_issue_selection['custom_field_name'],
                                       tracker_issue_selection['custom_field_id'])
    tracker_choice.tracker_selection()
    logger.debug('Hello')

    # """ BUGZILLA """
    # logger.debug('-----------------------------------------BUGZILLA------------------------------------------')
    # # Bug ID to searching for in the REST API
    # bug_id_in_api = 1144467
    # user_name = 'lhenry@mozilla.com'
    # # Access key provided by the Bugzilla API Service
    # # https://bugzilla.mozilla.org/home
    # # An account is necessary, and the API Access Key can be generated here:
    # # https://bugzilla.mozilla.org/userprefs.cgi?tab=apikey
    # api_key = 'JjuxII3hzJBzpzxZ1erGO2vNMnqz5FigqMeTLdzw'
    # first_name = 'Pantelis'
    # last_name = 'Tzamalis'
    # email = 'tzamalis@ceid.upatras.gr'
    #
    # # creating the objects for retrieving the information from the API and printing the fetched data
    #
    # # bug data
    # bug_fetcher = BugRetriever(bug_id=str(bug_id_in_api), key=api_key)
    #
    # # bug comments
    # get_comments = Comments(bug_id=bug_id_in_api, key=api_key)
    #
    # # bug history
    # get_history = History(bug_id=bug_id_in_api, key=api_key)
    #
    # # bugs related to a user
    # user_bugs = UserBugs(user='lhenry@mozilla.com', key=api_key)
    #
    # # user information
    # user_info = UserInfo(user=user_name, key=api_key)
    #
    # # DOCS
    # # bug
    # doc_bug = GeneratorBugzillaBug(user=user_name, bug=bug_id_in_api, firstname=first_name, lastname=last_name,
    #                                email_account=email, data_basic=bug_fetcher.data_retriever())
    # doc_bug.generating_doc_bugzilla()
    #
    # # bug comments
    # doc_bug_comments = GenratorBugzillaBugComments(user=user_name, bug=bug_id_in_api, firstname=first_name,
    #                                                lastname=last_name, email_account=email,
    #                                                data_comments=get_comments.getting_comments())
    # doc_bug_comments.generating_doc_bug_comments()
    #
    # # bug history
    # doc_bug_history = GeneratorBugzillaBugHistory(user=user_name, bug=bug_id_in_api, firstname=first_name,
    #                                               lastname=last_name, email_account=email,
    #                                               data_bug_history=get_history.getting_history())
    # doc_bug_history.generating_doc_bug_history()
    #
    # # user bugs
    # doc_user_bugs = GeneratorBugzillaUserBugs(user=user_name, firstname=first_name, lastname=last_name,
    #                                           email_account=email, data_bugs_user=user_bugs.getting_user_bugs())
    # doc_user_bugs.generating_doc_user_bugs()
    #
    # # user information
    # doc_user_info = GeneratorBuzillaUserInfo(user=user_name, firstname=first_name, lastname=last_name,
    #                                          email_account=email, data_user=user_info.getting_user_info())
    # doc_user_info.generating_doc_user_info()
    #
    """JIRA"""

    logger.debug('---------------------------JIRA------------------------------------')

    issue_name = 'JBCS-535'
    bug_id = issue_name.lower()
    print()
    print('Terminating..')


