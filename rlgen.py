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

from logger_creation import LoggerSetup

current_d = os.getcwd()
# print(current_d)
directories_list = current_d.split('/')
conf_path = 'conf/'

""" USER CHOICE OF ISSUE TRACKING PLATFORM """


class UserTrackerChoice:
    def __init__(self, tracker, issue, release_note, order, user, field_name, field_id, terms,
                 bug_function, output_path, debug_level, time):
        self.tracker = tracker
        self.issue = issue
        self.user = user
        self.field_name = field_name
        self.field_id = field_id
        self.terms = terms
        self.bug_function = bug_function
        self.release_note = release_note
        self.order = order
        self.output_path = output_path
        self.debug_level = debug_level
        self.time = time

    def tracker_selection(self):
        # JIRA
        if self.tracker is 'J' or self.tracker is 'j':
            logger_rlgen_main.info('---------------------------JIRA------------------------------------')
            print('Entered JIRA environment')
            logger_rlgen_main.info('Entered JIRA environment.')

            # JIRA user authentication configuration file reading
            logger_rlgen_main.info('JIRA - Reading user information in configuration file.')
            config = configparser.ConfigParser()
            config.read('{}config.conf'.format(conf_path))
            user_name = config['jira_basic_auth']['username']
            first_name = config['author']['firstname']
            last_name = config['author']['lastname']
            email = config['author']['email']
            logger_rlgen_main.debug('JIRA - Username: {}'.format(user_name))
            logger_rlgen_main.debug('JIRA - First Name: {}'.format(first_name))
            logger_rlgen_main.debug('JIRA - Last Name: {}'.format(last_name))
            logger_rlgen_main.debug('JIRA - Email: {}'.format(email))

            # JIRA search terms configuration file reading
            logger_rlgen_main.info('JIRA - API field name reading for Target Release in configuration file.')
            search_terms_config = configparser.ConfigParser()
            search_terms_config.read('conf/search_terms.conf')
            release_name = search_terms_config['jira_target_release']['name']
            logger_rlgen_main.debug('JIRA - Release Name: {}'.format(release_name))
            # RELEASE NAME
            if release_name is '':
                release_name = None

            # PATH value from user
            logger_rlgen_main.debug(
                'JIRA - PATH value from user (if exists in configuration file or as an input from command prompt)')
            path = None
            print('Path input from user:', self.output_path)
            logger_rlgen_main.debug('Path input from user: {}'.format(self.output_path))
            if self.output_path is not None:
                path = self.output_path
            else:
                if config['path']['directory'] is '':
                    path = None
                elif config['path']['directory'] is not '':
                    path = config['path']['directory']
            print('Final path value:', path)
            logger_rlgen_main.debug('JIRA - Final path value: {}'.format(path))

            # calling the class for making the the Target Release notes object
            # self.release_note is type of list
            logger_rlgen_main.info(
                'JIRA - Calling the class for making the object for the Target Release notes report.')
            logger_rlgen_main.debug('self.release_note class argument is type of list')
            release_notes = TargetReleaseJira(release_name=release_name,
                                              release=self.release_note,
                                              order=self.order,
                                              debug_level=self.debug_level)

            # calling the basic class for collecting the corresponding data from the Bugzilla REST API
            # functions: bug info, bug comments
            logger_rlgen_main.info(
                'JIRA - Calling the basic class for collecting the corresponding issue data from the JIRA REST API.')
            logger_rlgen_main.debug('JIRA - Functions that can be executed: bug info (--function b), '
                                    'bug comments (--function c)')
            issue_object = IssueDataRetrieverJira(issue=self.issue,
                                                  terms=self.terms,
                                                  cf_name=self.field_name,
                                                  cf_id=self.field_id,
                                                  debug_level=self.debug_level)

            report_field = 'No report field is specified.'
            data_report = ['* No data were fetched from the REST API.']

            # JIRA RELEASE NOTES
            if self.bug_function is 'r' or self.bug_function is 'R':
                logger_rlgen_main.info('JIRA - Executing Target Releases functionality.')
                if release_name is not None and self.release_note is not None:
                    print(self.release_note)
                    logger_rlgen_main.info('JIRA - Release Notes set in command prompt:  {}'
                                           .format(str(self.release_note)))
                    report_field = 'TargetReleases'
                    release_notes_data = release_notes.get_release_notes()
                    data_report = release_notes_data
                    logger_rlgen_main.info(
                        "JIRA - Check the 'jira_target_releases.log' file inside 'log' directory of the RLGen tool for "
                        "getting information about the Target Release functionality execution.")
                else:
                    if self.release_note is None:
                        print('Please define at least a Release Note to search for..')
                        logger_rlgen_main.error("JIRA - Please define at least a Release Note with the '--release' "
                                                "argument.")
                        # raise Exception('Please define at least a Release Note with the -r argument.')
                    elif release_name is None:
                        print(
                            'Please define the Release Name field of the custom field of JIRA inside the configuration '
                            'file.')
                        logger_rlgen_main.error('JIRA - Please define the Release Name field of the custom field of '
                                                'JIRA inside the configuration file.')
                        # raise Exception('Please define the Release Name field of the custom field of JIRA inside the '
                        #                 'configuration file')
                    else:
                        print('Both Release Name and Release notes fields are note defined.')
                        logger_rlgen_main.error('JIRA - Both Release Name (in configuration file '
                                                '([jira_target_release] -> name)) and Release Notes (in command '
                                                'prompt) fields are note defined.')
            elif self.bug_function is 'b' or self.bug_function is 'B':
                logger_rlgen_main.info('JIRA - Executing Issue Information functionality.')
                if self.issue is not None:
                    report_field = 'BugInfo'
                    issue_data = issue_object.get_data()
                    issue_info_data = issue_object.get_basic_issue_data(issue_data)
                    data_report = issue_info_data
                    logger_rlgen_main.info(
                        "JIRA - Check the 'jira_issue_data.log' file inside 'log' directory of the RLGen tool "
                        "for getting information about the Bug Information functionality execution.")
                else:
                    print('JIRA - Please define an issue.')
                    logger_rlgen_main.error('JIRA - Please define an issue.')
            elif self.bug_function is 'c' or self.bug_function is 'C':
                logger_rlgen_main.info('JIRA - Executing Issue Comments functionality.')
                if self.issue is not None:
                    report_field = 'BugComments'
                    issue_data = issue_object.get_data()
                    issue_comments_data = issue_object.getting_comments_data(issue_data)
                    data_report = issue_comments_data
                    logger_rlgen_main.info(
                        "JIRA - Check the 'jira_issue_data.log' file inside 'log' directory of the RLGen tool "
                        "for getting information about the Bug Comments functionality execution.")
                else:
                    print('JIRA - Please define an issue.')
                    logger_rlgen_main.error('JIRA - Please define an issue.')
            else:
                print('Please enter a valid letter for function:\n'
                      '--function r: Release Note\n'
                      '--function c: Bug Comments\n'
                      '--function b: Bug Information\n')
                logger_rlgen_main.error('JIRA - Please enter a valid letter for function:\n '
                                        '--function r: Release Note\n '
                                        '--function c: Bug Comments\n '
                                        '--function b: Bug Information\n ')
            # MAKING DOC REPORT -> ASCIIDOC
            print('Generating DOC..')
            logger_rlgen_main.info('JIRA - Executing the AsciiDoc File Generation functionality.')
            logger_rlgen_main.info('JIRA - Generating AsciiDoc file..')
            doc_basic = GeneratorJira(kind_of_report=report_field,
                                      releases=self.release_note,
                                      user=user_name,
                                      bug=self.issue,
                                      firstname=first_name,
                                      lastname=last_name,
                                      email_account=email,
                                      data_basic=data_report,
                                      path=path,
                                      time=self.time)
            doc_basic.generating_doc_jira()
            logger_rlgen_main.info('JIRA - AsciiDoc file created..')
            logger_rlgen_main.info(
                "JIRA - Check the 'asciidoc_generator.log' file inside 'log' directory of the RLGen tool "
                "for getting information about the AsciiDoc File Generation functionality execution.")

        # BUGZILLA
        elif self.tracker is 'B' or self.tracker is 'b':
            logger_rlgen_main.info('---------------------------------BUGZILLA------------------------------------')
            print('Entered Bugzilla environment')
            logger_rlgen_main.info('Entered Bugzilla environment.')

            # Bugzilla user authentication configuration file reading
            logger_rlgen_main.info('BUGZILLA - Reading user information in configuration file.')
            config = configparser.ConfigParser()
            config.read('{}config.conf'.format(conf_path))
            user_name = config['bugzilla_basic_auth']['username']
            first_name = config['author']['firstname']
            last_name = config['author']['lastname']
            email = config['author']['email']
            logger_rlgen_main.debug('BUGZILLA - Username: {}'.format(user_name))
            logger_rlgen_main.debug('BUGZILLA - First Name: {}'.format(first_name))
            logger_rlgen_main.debug('BUGZILLA - Last Name: {}'.format(last_name))
            logger_rlgen_main.debug('BUGZILLA - Email: {}'.format(email))

            # PATH value from user
            logger_rlgen_main.debug(
                'BUGZILLA - PATH value from user (if exists in configuration file or as an input from command prompt)')
            path = None
            print('Path input from user:', self.output_path)
            if self.output_path is not None:
                path = self.output_path
            else:
                if config['path']['directory'] is '':
                    path = None
                elif config['path']['directory'] is not '':
                    path = config['path']['directory']
            print('Final path value:', path)
            logger_rlgen_main.debug('BUGZILLA - Final path value: {}'.format(path))

            # calling the class for making the the Target Release notes object
            # self.release_note is type of list
            logger_rlgen_main.info(
                'BUGZILLA - Calling the class for making the object for the Target Release notes report.')
            logger_rlgen_main.debug('self.release_note class argument is type of list')
            release_notes = TargetReleaseBugzilla(releases=self.release_note,
                                                  terms=self.field_name,
                                                  debug_level=self.debug_level)

            # calling the basic class for collecting the corresponding data from the bugzilla rest api
            # functions: bug info, bug comments, bug history, user info, user assigned bugs
            logger_rlgen_main.info(
                'BUGZILLA - Calling the basic class for collecting the corresponding issue or user related data from '
                'the Bugzilla REST API.')
            logger_rlgen_main.debug('BUGZILLA - Functions that can be executed: bug information (--function b), '
                                    'bug comments (--function c), bug history (--function h), '
                                    'user assigned bugs (--function -a), user information (--function u)')
            data_object = DataRetriever(bug_id=self.issue,
                                        terms=self.field_name,
                                        user=self.user,
                                        debug_level=self.debug_level)

            report_field = 'No report field is specified.'
            data_report = ['* No data were fetched from the REST API.']

            # FUNCTIONS: -f --function
            # release notes
            if self.bug_function is 'r' or self.bug_function is 'R':
                logger_rlgen_main.info('BUGZILLA - Executing Target Releases functionality.')
                if self.release_note is not None:
                    report_field = 'TargetReleases'
                    release_notes_data = release_notes.getting_target_release_notes()
                    # bug release notes
                    data_report = release_notes_data
                    logger_rlgen_main.info(
                        "BUGZILLA - Check the 'bugzilla_target_releases.log' file inside 'log' directory of the "
                        "RLGen tool for getting information about the Target Release functionality execution.")
                else:
                    print('BUGZILLA - Please define a release note.')
                    logger_rlgen_main.error('BUGZILLA - Please define a release note.')
            # bug info
            elif self.bug_function is 'b' or self.bug_function is 'b':
                logger_rlgen_main.info('BUGZILLA - Executing Bug Information functionality.')
                if self.issue is not None:
                    report_field = 'BugInfo'
                    bug_info = data_object.getting_bug_info()
                    bug_info_data = data_object.data_retriever(bug_info['retrieve'],
                                                               bug_info['data_output'],
                                                               bug_info['search_list_output'],
                                                               bug_info['ascii_bug_info_list'])
                    # bug info
                    data_report = bug_info_data
                    logger_rlgen_main.info(
                        "BUGZILLA - Check the 'bugzilla_exec_function.log' and the 'bugzilla_data_retriever.log' files "
                        "inside 'log' directory of the RLGen tool for getting information about the Bug Information "
                        "functionality execution.")
                else:
                    print('BUGZILLA - Please define a correct Bug ID.')
                    logger_rlgen_main.error('BUGZILLA - Please define a correct Bug ID.')
            # user assigned bugs
            elif self.bug_function is 'a' or self.bug_function is 'A':
                logger_rlgen_main.info('BUGZILLA - Executing User Assigned Bugs functionality.')
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
                    logger_rlgen_main.info(
                        "BUGZILLA - Check the 'bugzilla_exec_function.log' and the 'bugzilla_data_retriever.log' files "
                        "inside 'log' directory of the RLGen tool for getting information about the User Assigned Bugs "
                        "functionality execution.")
                else:
                    print('BUGZILLA - Please define a username or user email.')
                    logger_rlgen_main.error('BUGZILLA - Please define a correct username or user email.')
            # user info
            elif self.bug_function is 'u' or self.bug_function is 'U':
                logger_rlgen_main.info('BUGZILLA - Executing User Information functionality.')
                if self.user is not None:
                    report_field = 'UserInfo'
                    user_info = data_object.getting_user_info()
                    user_info_data = data_object.data_retriever(retrieval=user_info['retrieve'],
                                                                data=user_info['data_output'],
                                                                search_list=user_info['search_list_output'],
                                                                ascii_doc_data=user_info['ascii_user_info_list'])
                    # user info doc
                    data_report = user_info_data
                    logger_rlgen_main.info(
                        "BUGZILLA - Check the 'bugzilla_exec_function.log' and the 'bugzilla_data_retriever.log' files "
                        "inside 'log' directory of the RLGen tool for getting information about the User Information "
                        "functionality execution.")
                else:
                    print('BUGZILLA - Please define a username or user email.')
                    logger_rlgen_main.error('BUGZILLA - Please define a correct username or user email.')
            # bug comments
            elif self.bug_function is 'c' or self.bug_function is 'C':
                logger_rlgen_main.info('BUGZILLA - Executing Bug Comments functionality.')
                if self.issue is not None:
                    report_field = 'BugComments'
                    bug_comments = data_object.getting_bug_comments()
                    bug_comments_data = data_object.data_retriever(retrieval=bug_comments['retrieve'],
                                                                   data=bug_comments['data_output'],
                                                                   search_list=bug_comments['search_list_output'],
                                                                   ascii_doc_data=bug_comments['ascii_bug_comments_list'])
                    # bug comments doc
                    data_report = bug_comments_data
                    logger_rlgen_main.info(
                        "BUGZILLA - Check the 'bugzilla_exec_function.log' and the 'bugzilla_data_retriever.log' files "
                        "inside 'log' directory of the RLGen tool for getting information about the Bug Comments "
                        "functionality execution.")
                else:
                    print('BUGZILLA - Please define a correct Bug ID.')
                    logger_rlgen_main.error('BUGZILLA - Please define a correct Bug ID.')
            # bug history
            elif self.bug_function is 'h' or self.bug_function is 'H':
                logger_rlgen_main.info('BUGZILLA - Executing Bug History functionality.')
                if self.issue is not None:
                    report_field = 'BugHistory'
                    bug_history = data_object.getting_bug_history()
                    bug_history_data = data_object.data_retriever(retrieval=bug_history['retrieve'],
                                                                  data=bug_history['data_output'],
                                                                  search_list=bug_history['search_list_output'],
                                                                  ascii_doc_data=bug_history['ascii_bug_history_list'])
                    # bug history doc
                    data_report = bug_history_data
                    logger_rlgen_main.info(
                        "BUGZILLA - Check the 'bugzilla_exec_function.log' and the 'bugzilla_data_retriever.log' files "
                        "inside 'log' directory of the RLGen tool for getting information about the Bug History "
                        "functionality execution.")
                else:
                    print('Please define a correct Bug ID.')
                    logger_rlgen_main.error('Please define a correct Bug ID.')
            else:
                print('Please enter a valid letter for function:\n'
                      '--function r: Release Note\n'
                      '--function u: User Information\n'
                      '--function b: Bug Information\n'
                      '--function c: Bug Comments\n'
                      '--function h: Bug History\n'
                      '--function a: Bugs Assigned to a User\n')
                logger_rlgen_main.error('BUGZILLA -Please enter a valid letter for function:\n '
                                        '--function r: Release Note\n '
                                        '--function u: User Information\n '
                                        '--function b: Bug Information\n '
                                        '--function c: Bug Comments\n '
                                        '--function h: Bug History\n '
                                        '--function a: Bugs Assigned to a User\n')

            # MAKING DOC REPORT
            print('Generating DOC..')
            logger_rlgen_main.info('BUGZILLA - Executing the AsciiDoc File Generation functionality.')
            logger_rlgen_main.info('BUGZILLA - Generating AsciiDoc file..')
            report = GeneratorBugzillaReport(kind_of_report=report_field,
                                             releases=self.release_note,
                                             bug=self.issue,
                                             user=self.user,
                                             username=user_name,
                                             firstname=first_name,
                                             lastname=last_name,
                                             email_account=email,
                                             data_basic=data_report,
                                             path=path,
                                             time=self.time)
            report.generating_doc_bugzilla()
            logger_rlgen_main.info('BUGZILLA - AsciiDoc file created..')
            logger_rlgen_main.info(
                "BUGZILLA - Check the 'asciidoc_generator.log' file inside 'log' directory of the RLGen tool "
                "for getting information about the AsciiDoc File Generation functionality execution.")
        else:
            print('Please press a valid letter ("J" or "j" for JIRA / "B" or "b" for Bugzilla) '
                  'for choosing your tracker.')
            logger_rlgen_main.error('Please press a valid letter ("J" or "j" for JIRA / "B" or "b" for Bugzilla) '
                                    'for choosing your tracker.')


""" USER TERMINAL INPUTS """


def user_input(argv):

    parser = ArgumentParser()

    parser.add_argument("-t", "--tracker",
                        dest="tracker",
                        help="Add the tracker you want to search for the issue: 'j' or 'J' for Jira | "
                             "'b' or 'B' for Bugzilla",
                        metavar="<TRACKER>",
                        required=True)
    parser.add_argument("-r", "--release",
                        dest="release_note",
                        nargs='+',
                        help="Add each Target Release Name inside quotes, separated with the SPACE character "
                             "(e.g.: --release '5.backlog.GA' 'httpd 2.4.backlog.GA'). This argument"
                             "returns a list of the releases defined by the user. It can be used with the 'releases' "
                             "function (--function r) both for JIRA and Bugzilla Tracking Systems.",
                        metavar="<TARGET_RELEASE_NAME>",
                        type=str)
    parser.add_argument("-i", "--issue",
                        dest="issue",
                        help="Add the issue ID. It can be used with the following functions for each Tracking System: "
                             "1) Bugzilla -> 'bug information' (--function b), "
                             "'bug comments' (--function c), "
                             "'bug history' (--function h)\n. "
                             "2) JIRA -> 'bug information' (--function b), "
                             "'bug comments' (--function c).",
                        metavar="<ISSUE_ID>")
    parser.add_argument("-n", "--name",
                        dest="field_name",
                        action='append',
                        help="Besides the configuration file, using this argument you can define the field name/s to "
                             "search for in Bugzilla/JIRA API. 1) Bugzilla: Define the Fields you want to search for "
                             "in Bug Information or the Bugs' Details for each Target Release. "
                             "This argument can be used with the 'bug information' "
                             "function (--function b) or the 'releases' function (--function r). "
                             "Each Custom Field Name must be inside quotes with the '--name' declaration in front "
                             "of it (e.g.: --name 'resolution' --name 'qa_contact'). If a field/term that is defined "
                             "by the user in prompt is not a part of the fields that are included in bug "
                             "report (of Bugzilla API) then it will not be exported in the AsciiDoc file. "
                             " Please check the Wiki in Github repository of the RLGen tool for the"
                             "available Bug Field names.\n"
                             " 2) JIRA: Define the Custom Field Name you want to search for in Bug Information. "
                             "It must be accompanied by the relevant Custom Field ID which can be declared by "
                             "the '--customid' argument and it is unique. Each Custom Field Name must be inside quotes"
                             "with the '--name' declaration in front of it "
                             "(e.g.: --name 'TestFieldUserInput' --name 'TestFieldUserInput2'). "
                             "This argument can be used with the 'bug information' function (--function b). "
                             "Please see the relevant argument documentation (--function)",
                        metavar="<FIELD_NAME>")
    parser.add_argument("-c", "--customid",
                        dest="field_id",
                        nargs='+',
                        help="NOTE: ONLY FOR JIRA TRACKER.\n"
                             "You have to know the Custom Field ID number in JIRA API (when it is necessary), so you "
                             "can declare this argument. Furthermore, each Custom Field ID must be accompanied by the "
                             "corresponding name which can be defined by the '--name' argument. The ID must be an "
                             "integer. This value is the unique number of the custom field ID created automatically "
                             "by the JIRA API. If a Custom Field ID that is defined by the user in prompt is not a "
                             "part of the fields that are included in bug reports (of JIRA API) then it "
                             "will not be exported in the AsciiDoc file. Each Custom Field ID has to be separated with"
                             "the SPACE character from the next one (e.g.: --customid 12311940 12310840). "
                             "This argument can be used with the 'bug information' function (--function b). "
                             "Please see the relevant argument documentation (--function)",
                        metavar="<CUSTOM_FIELD_ID>",
                        type=int)
    parser.add_argument("-s", "--searchterms",
                        dest="search_terms",
                        nargs='+',
                        help="NOTE: ONLY FOR JIRA TRACKER. "
                             "Define the Fields you want to search for in Bug "
                             "Information. Each field must be in quotes and separated by the SPACE character from the "
                             "next one (e.g.: --searchterms 'worklog' 'progress'). If a field/term that is defined by "
                             "the user in prompt is not a part of the fields that are included in bug "
                             "report (of JIRA API) then it will not be exported in the AsciiDoc file. Each search "
                             "field must be inside quotes and separated with the SPACE character from the next "
                             "one (e.g.: --searchterms 'worklog' 'progress').",
                        metavar="<SEARCH_TERMS>")
    parser.add_argument("-u", "--user",
                        dest="user",
                        help="NOTE: ONLY FOR BUGZILLA TRACKER. "
                             "Add the user (username/user email) you want to search for. This argument must be used "
                             "with the 'user information' and the 'user assigned bugs' functions (see the '--function' "
                             "argument).",
                        metavar="<USER_NAME>")
    parser.add_argument("-f", "--function",
                        dest="function",
                        help="Add the function you want to use for each Tracking System: \n "
                             "1) Bugzilla -> r: releases, b: bug information, c: bug comments, h: bug history, "
                             "u: user information, a: user assigned bugs. \n"
                             "2) JIRA -> r: releases, b: bug information, c: bug comments",
                        metavar="<BUG_FUNCTION>",
                        required=True)
    parser.add_argument("-a", "--ascending",
                        dest="order_ascending",
                        help="NOTE: ONLY FOR JIRA TRACKER.\n "
                             "OPTIONAL: Add the operation you want to be executed "
                             "for ascending/descending order classification of the release note results "
                             "which are retrieved from the JIRA API -> a: ascending, d: descending. ",
                        metavar="<ASC/DESC_ORDER>")
    parser.add_argument("-o", "--output",
                        dest="output_path",
                        help="OPTIONAL: Add the full path directory you want to save the AsciiDoc exported file.",
                        metavar="<OUTPUT_PATH>")
    parser.add_argument("-z", "--zonetime",
                        dest="zone_time",
                        help="OPTIONAL: Enable/Disable the Report Time mode -> 0: Disable, 1: Enable.\n By default is "
                             "Disabled",
                        metavar="<ZONE_TIME>",
                        type=int)
    parser.add_argument("-l", "--loglevel",
                        dest="debug_level",
                        help="OPTIONAL: Define the level of debugging (0: DEBUG, 1: INFO, 2: WARNING, 3: ERROR, "
                             "4: CRITICAL).",
                        metavar="<DEBUG_LEVEL>",
                        type=int)

    # ARGUMENTS --> extra
    parser.add_argument("-q", "--quiet",
                        action="store_false",
                        dest="verbose",
                        default=True,
                        help="don't print status messages to stdout")

    # arguments parser creation object
    arguments = parser.parse_args()
    # print(">>>> Print when a value is empty:", arguments.user)
    # print('Print custom field names', arguments.field_name)
    # print('>>>> Print list customfield IDs:', arguments.field_id)
    return {'tracker': arguments.tracker,
            'issue': arguments.issue,
            'user': arguments.user,
            'field_name': arguments.field_name,
            'field_id': arguments.field_id,
            'search_terms': arguments.search_terms,
            'bug_function': arguments.function,
            'order_ascending': arguments.order_ascending,
            'release_note': arguments.release_note,
            'output_path': arguments.output_path,
            'debug_level': arguments.debug_level,
            'zone_time': arguments.zone_time}


if __name__ == '__main__':
    print('Starting RLGen Tool')
    tracker_issue_selection = user_input(sys.argv[1:])
    logging_rlgen = LoggerSetup(name='main_logger',
                                log_file='log/rlgen_main.log',
                                level=tracker_issue_selection['debug_level'])

    logger_rlgen_main = logging_rlgen.setup_logger()

    logger_rlgen_main.info('Entering the RLGen Tool')

    # User Choice
    tracker_choice = UserTrackerChoice(tracker=tracker_issue_selection['tracker'],
                                       issue=tracker_issue_selection['issue'],
                                       user=tracker_issue_selection['user'],
                                       field_name=tracker_issue_selection['field_name'],
                                       field_id=tracker_issue_selection['field_id'],
                                       terms=tracker_issue_selection['search_terms'],
                                       bug_function=tracker_issue_selection['bug_function'],
                                       order=tracker_issue_selection['order_ascending'],
                                       release_note=tracker_issue_selection['release_note'],
                                       output_path=tracker_issue_selection['output_path'],
                                       debug_level=tracker_issue_selection['debug_level'],
                                       time=tracker_issue_selection['zone_time'])

    tracker_choice.tracker_selection()
    print()
    print('Terminating..')
    logger_rlgen_main.info('Terminating..')


