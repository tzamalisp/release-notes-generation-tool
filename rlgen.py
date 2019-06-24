from datetime import datetime

from bugzilla_requester import BugRetriever
from bugzilla_requester import Comments
from bugzilla_requester import History
from bugzilla_requester import UserBugs
from bugzilla_requester import UserInfo

from jira_requester import Connector
from jira_requester import BasicDataRetriever
from jira_requester import CustomFieldConfCreation
from jira_requester import CustomFieldListFile
from jira_requester import CustomFieldDataRetriever

from asciidoc_generator import GeneratorJira
from asciidoc_generator import GeneratorBugzillaBug
from asciidoc_generator import GenratorBugzillaBugComments
from asciidoc_generator import GeneratorBugzillaBugHistory
from asciidoc_generator import GeneratorBugzillaUserBugs
from asciidoc_generator import GeneratorBuzillaUserInfo


if __name__ == '__main__':

    """ BUGZILLA """
    print()
    print('-----------------------------------------BUGZILLA------------------------------------------')
    print()
    # Bug ID to searching for in the REST API
    bug_id_in_api = 1144467
    user_name = 'lhenry@mozilla.com'
    # Access key provided by the Bugzilla API Service
    # https://bugzilla.mozilla.org/home
    # An account is necessary, and the API Access Key can be generated here:
    # https://bugzilla.mozilla.org/userprefs.cgi?tab=apikey
    api_key = 'JjuxII3hzJBzpzxZ1erGO2vNMnqz5FigqMeTLdzw'
    first_name = 'Pantelis'
    last_name = 'Tzamalis'
    email = 'tzamalis@ceid.upatras.gr'

    # creating the objects for retrieving the information from the API and printing the fetched data

    # bug data
    bug_fetcher = BugRetriever(bug_id=str(bug_id_in_api), key=api_key)

    # bug comments
    get_comments = Comments(bug_id=bug_id_in_api, key=api_key)

    # bug history
    get_history = History(bug_id=bug_id_in_api, key=api_key)

    # bugs related to a user
    user_bugs = UserBugs(user='lhenry@mozilla.com', key=api_key)

    # user information
    user_info = UserInfo(user=user_name, key=api_key)

    # DOCS
    # bug
    doc_bug = GeneratorBugzillaBug(user=user_name, bug=bug_id_in_api, firstname=first_name, lastname=last_name,
                                   email_account=email, data_basic=bug_fetcher.data_retriever())
    doc_bug.generating_doc_bugzilla()

    # bug comments
    doc_bug_comments = GenratorBugzillaBugComments(user=user_name, bug=bug_id_in_api, firstname=first_name,
                                                   lastname=last_name, email_account=email,
                                                   data_comments=get_comments.getting_comments())
    doc_bug_comments.generating_doc_bug_comments()

    # bug history
    doc_bug_history = GeneratorBugzillaBugHistory(user=user_name, bug=bug_id_in_api, firstname=first_name,
                                                  lastname=last_name, email_account=email,
                                                  data_bug_history=get_history.getting_history())
    doc_bug_history.generating_doc_bug_history()

    # user bugs
    doc_user_bugs = GeneratorBugzillaUserBugs(user=user_name, firstname=first_name, lastname=last_name,
                                              email_account=email, data_bugs_user=user_bugs.getting_user_bugs())
    doc_user_bugs.generating_doc_user_bugs()

    # user information
    doc_user_info = GeneratorBuzillaUserInfo(user=user_name, firstname=first_name, lastname=last_name,
                                             email_account=email, data_user=user_info.getting_user_info())
    doc_user_info.generating_doc_user_info()

    """JIRA"""
    print()
    print('---------------------------JIRA------------------------------------')
    print()
    issue_name = 'JBCS-535'
    name_field_id_name = 'Target Release'
    field_id = 12311240
    bug_id = issue_name.lower()
    username = 'tzamalisp'
    first_name = 'Pantelis'
    last_name = 'Tzamalis'
    email = 'tzamalis@ceid.upatras.gr'

    # CONNECTION TO JIRA
    print('CONNECTION TO JIRA')
    print()
    # test_connector = Connector()
    # test_connector.jira_connector()

    print()
    print('---------------------------------------------')
    print('---------------------------------------------')
    print()

    # ADDING CUSTOM FIELD - CREATION OF THE JSON CONFIGURATION FILE
    print('ADDING CUSTOM FIELD - CREATION OF THE JSON CONFIGURATION FILE')
    print()
    # new__custom_field = CustomFieldConfCreation('xxx', 'customfield_12310220')
    # new__custom_field.custom_field_configuration_creation()

    print()
    print('---------------------------------------------')
    print('---------------------------------------------')
    print()

    # DASHBOARD'S CUSTOM FIELDS AVAILABLE - CONFIGURATION JSON FILE CREATION
    print("DASHBOARD'S CUSTOM FIELDS AVAILABLE - CONFIGURATION JSON FILE CREATION")
    print()
    dashboard_custom_field_list = CustomFieldListFile(issue_name)
    dashboard_custom_field_list.list_file_generator()

    print()
    print('---------------------------------------------')
    print('---------------------------------------------')
    print()

    # BASIC DATA RETRIEVER
    print('BASIC DATA RETRIEVER')
    print()
    jira_basic_data = BasicDataRetriever(issue_name)
    # jira_basic_data.data_retriever()

    print()
    print('---------------------------------------------')
    print('---------------------------------------------')
    print()

    # CUSTOM FIELD DATA RETRIEVER
    print('CUSTOM FIELD DATA RETRIEVER')
    print()
    jira_custom_field_data = CustomFieldDataRetriever(issue_name, name_field_id_name, field_id)
    # jira_custom_field_data.data_retriever()
    print()
    print()
    print('----')
    report_time = datetime.now()
    print('Report time:', report_time)
    print('----')
    print()
    print()
    print('>>> Calling JIRA API and printing Issue parts is now completed successfully!')
    print()
    print()

    # doc basic fields
    doc_basic = GeneratorJira(user=username, bug=bug_id, firstname=first_name, lastname=last_name, email_account=email,
                              data_basic=jira_basic_data.data_retriever(),
                              data_custom=jira_custom_field_data.data_retriever())
    doc_basic.generating_doc_jira()

    print('---')
    print('Report time:', datetime.now())
    print()
