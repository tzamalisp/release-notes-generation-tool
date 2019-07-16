from jira import JIRA
import requests
from pprint import pprint

from conf.confparse import JiraReadConfigurationServer
from conf.confparse import JiraReadConfigurationBasicAuth
from conf.confparse import JiraReadConfigurationOAuth
from conf.confparse import JiraReadConfigurationKerberos


"""CLASS FOR RETRIEVING BASIC ISSUE INFORMATION FROM JIRA API"""


class Connector:

    def jira_connector(self):
        """ JIRA Connection"""
        # JIRA connection options dictionary
        options = {}
        # JIRA connection credentials
        server_connection = JiraReadConfigurationServer()
        server_auth = server_connection.read_server_conf()['server_auth']
        if server_auth is True:
            server_value = server_connection.read_server_conf()['server']
            options['server'] = server_value
        else:
            server_reason_value = server_connection.read_server_conf()['server_reason']
            raise Exception(server_reason_value)

        # Authentication objects
        jira_basic_auth = JiraReadConfigurationBasicAuth()
        jira_oauth = JiraReadConfigurationOAuth()
        jira_kerberos = JiraReadConfigurationKerberos()

        basic_auth = jira_basic_auth.read_user_basic_auth()['basic_auth']
        oauth = jira_oauth.read_oauth()['oauth']
        kerberos_auth = jira_kerberos.read_kerberos_auth()['kerberos_auth']
        # code for key cert here
        key_cert_data = None
        # with open(key_cert, 'r') as key_cert_file:
        #     key_cert_data = key_cert_file.read()
        key_cert_data = 'To be added'

        # Structure of 'options' value authentication
        # options = {
        #     'server': server_value,
        #     'basic_auth': (username_value, password_value),
        #     'oauth': {
        #         'access_token': access_token_value,
        #         'access_token_secret': access_token_secret_value,
        #         'consumer_key': consumer_key_value,
        #         'key_cert': key_cert_data
        #     },
        #     'kerberos': kerberos_value,
        #     'kerberos_options': {'mutual_authentication': kerberos_mutual_authentication_value}
        # }

        if basic_auth is True or oauth is True or kerberos_auth is True:
            if basic_auth is True:
                basic_auth_reason_value = jira_basic_auth.read_user_basic_auth()['basic_auth_reason']
                username_value = jira_basic_auth.read_user_basic_auth()['username']
                username_reason_value = jira_basic_auth.read_user_basic_auth()['username_reason']
                password_value = jira_basic_auth.read_user_basic_auth()['password']
                password_reason_value = jira_basic_auth.read_user_basic_auth()['password_reason']
                options['basic_auth'] = (username_value, password_value)
            elif oauth is True:
                oauth_reason_value = jira_oauth.read_oauth()['oauth_reason']
                access_token_value = jira_oauth.read_oauth()['access_token']
                access_token_reason_value = jira_oauth.read_oauth()['access_token_reason']
                access_token_secret_value = jira_oauth.read_oauth()['access_token_secret']
                access_token_secret_reason_value = jira_oauth.read_oauth()['access_token_secret_reason']
                consumer_key_value = jira_oauth.read_oauth()['consumer_key']
                consumer_key_reason_value = jira_oauth.read_oauth()['consumer_key_reason']
                # (TO DEFINE THE IF STATEMENT HERE):
                if key_cert_data is not None:
                    options['oauth'] = {'access_token': access_token_value,
                                        'access_token_secret': access_token_secret_value,
                                        'consumer_key': consumer_key_value,
                                        'key_cert': key_cert_data}
                else:
                    raise Exception('Please add the key certification data.')
            elif kerberos_auth is True:
                kerberos_auth_value_reason = jira_kerberos.read_kerberos_auth('kerberos_auth_reason')
                kerberos_value = bool(jira_kerberos.read_kerberos_auth('kerberos'))
                kerberos_reason_value = jira_kerberos.read_kerberos_auth('kerberos_reason')
                kerberos_mutual_authentication_value = jira_kerberos.read_kerberos_auth('kerberos_options')
                kerberos_options_reason_value = jira_kerberos.read_kerberos_auth('kerberos_options_reason')
                options['kerberos'] = kerberos_value
                options['kerberos_options'] = {'mutual_authentication': kerberos_mutual_authentication_value}
        else:
            if basic_auth is False:
                basic_auth_reason_value = jira_basic_auth.read_user_basic_auth()['basic_auth_reason']
                username_reason_value = jira_basic_auth.read_user_basic_auth()['username_reason']
                password_reason_value = jira_basic_auth.read_user_basic_auth()['password_reason']
                print(basic_auth_reason_value)
                print(username_reason_value)
                print(password_reason_value)
                raise Exception('Basic Authentication failed.')
            elif oauth is False:
                oauth_reason_value = jira_oauth.read_oauth()['oauth_reason']
                access_token_reason_value = jira_oauth.read_oauth()['access_token_reason']
                access_token_secret_reason_value = jira_oauth.read_oauth()['access_token_secret_reason']
                consumer_key_reason_value = jira_oauth.read_oauth()['consumer_key_reason']
                print(oauth_reason_value)
                print(access_token_reason_value)
                print(access_token_secret_reason_value)
                print(consumer_key_reason_value)
                raise Exception('OAuth Authentication failed.')
            elif kerberos_auth is False:
                kerberos_auth_value_reason = jira_kerberos.read_kerberos_auth('kerberos_auth_reason')
                kerberos_reason_value = jira_kerberos.read_kerberos_auth('kerberos_reason')
                kerberos_options_reason_value = jira_kerberos.read_kerberos_auth('kerberos_options_reason')
                print(kerberos_auth_value_reason)
                print(kerberos_reason_value)
                print(kerberos_options_reason_value)
                raise Exception('Kerberos Authentication failed.')

        # JIRA object for connecting to the API
        print('Options Authentication:')
        pprint(options)
        print()
        print('Connecting to the JIRA API..')
        try:
            jira_auth_connection = JIRA(options)
            print('Connected to JIRA API successfully!')
            return jira_auth_connection
        except Exception as e:
            print('The connection failed:', e)
            return None


"""JIRA BUG DATA RETRIEVE"""


class BasicDataRetriever:
    def __init__(self, issue_name_input):
        self.issue_name_input = issue_name_input

    def data_retriever(self):

        bug_ascii_data = []

        # JIRA API connection and connector object creation
        jira_connection_obj = Connector()
        jira = jira_connection_obj.jira_connector()
        """Issue Definition"""
        # creating an issue object to fetch information later on from JIRA API
        print('Creating the issue object..')
        issue = jira.issue(self.issue_name_input)
        print('BUG ID:', issue)
        if issue:
            bug_ascii_data.append('== Bug ID: {}'.format(self.issue_name_input))
            # Retrieving selected fields of a JIRA issue and printing them
            # Project key
            bug_ascii_data.append('=== Project Object')
            if issue.fields.project.self:
                project_url = issue.fields.project.self
                bug_ascii_data.append('* Project JSON URL: ' + project_url + '[{}]'.format(self.issue_name_input))
                bug_ascii_data.append('* Project Key: {}'.format(issue.fields.project.key))
                bug_ascii_data.append('* Project Name: {}'.format(issue.fields.project.name))
                bug_ascii_data.append('* Project ID: {}'.format(issue.fields.project.id))
                bug_ascii_data.append('* Project Category Name: {}'.format(issue.fields.project.projectCategory.name))
                bug_ascii_data.append('* Project Category Description: {}'.
                                      format(issue.fields.project.projectCategory.description))
                r = requests.get(project_url)
                data = r.json()
                bug_ascii_data.append('* Project Avatar: {}'.format(data['avatarUrls']['48x48']))
            else:
                bug_ascii_data.append('* No information to show about the Project.')
            # Issue type
            bug_ascii_data.append('=== Issue Type')
            if issue.fields.issuetype.name and issue.fields.issuetype.name is not None:
                bug_ascii_data.append('* Name: {}'.format(issue.fields.issuetype.name))
                bug_ascii_data.append('* Description: {}'.format(issue.fields.issuetype.description))
                bug_ascii_data.append('* Avatar: {}'.format(issue.fields.issuetype.iconUrl))
            else:
                bug_ascii_data.append('* There is no Type defined for the Issue --> {}'.format(self.issue_name_input))
            # Reporter Display Name
            bug_ascii_data.append('=== Reporter Display Name')
            if issue.fields.reporter.displayName and issue.fields.reporter.displayName is not None:
                bug_ascii_data.append('* Display Name: {}'.format(issue.fields.reporter.displayName))
            else:
                bug_ascii_data.append('* There is no Display Name for the Issue --> {}'.
                                      format(self.issue_name_input))
            # Created datetime
            bug_ascii_data.append('=== Created DateTime')
            if issue.fields.created and issue.fields.created is not None:
                bug_ascii_data.append('* Created at: {}'.format(issue.fields.created))
            else:
                bug_ascii_data.append('* There is no DateTime value stored for the Issue --> {}'
                                      .format(self.issue_name_input))
            # Assignee
            bug_ascii_data.append('=== Assignee')
            if issue.fields.assignee and issue.fields.assignee is not None:
                bug_ascii_data.append('* Display Name: {}'.format(issue.fields.assignee.displayName))
                bug_ascii_data.append('* Name: {}'.format(issue.fields.assignee.name))
                bug_ascii_data.append('* Key: {}'.format(issue.fields.assignee.key))
                bug_ascii_data.append('* Active: {}'.format('issue.fields.assignee.active'))
                bug_ascii_data.append('* TimeZone: {}'.format(issue.fields.assignee.timeZone))
            else:
                bug_ascii_data.append('* Assignee is not stored for the Issue --> {}'
                                      .format(self.issue_name_input))
            # Issue description
            bug_ascii_data.append('=== Issue Description')
            if issue.fields.description and issue.fields.description is not None:
                bug_ascii_data.append('* Description: {}'.format(issue.fields.description))
            else:
                bug_ascii_data.append('* Description is not available for that Issue --> {}'
                                      .format(self.issue_name_input))
            # Current Status
            bug_ascii_data.append('=== Status')
            if issue.fields.status and issue.fields.status is not None:
                bug_ascii_data.append('* Name: {}'.format(issue.fields.status.name))
                bug_ascii_data.append('* Description: {}'.format(issue.fields.status.description))
                bug_ascii_data.append('* Status Category Name: {}'.format(issue.fields.status.statusCategory.name))
                bug_ascii_data.append('* Icon: {}'.format(issue.fields.status.iconUrl))
            else:
                bug_ascii_data.append('* No Status is set for the Issue --> {}'.format(self.issue_name_input))
            # Aggregate progress
            bug_ascii_data.append('=== Aggregate Progress')
            if issue.fields.aggregateprogress:
                bug_ascii_data.append('* Progress: {}'.format(issue.fields.aggregateprogress.progress))
                bug_ascii_data.append('* Total: {}'.format(issue.fields.aggregateprogress.total))
            else:
                bug_ascii_data.append('* No information about Aggregate Progress is available.')
            # Aggregate time estimate
            bug_ascii_data.append('=== Aggregate Time Estimate')
            if issue.fields.aggregatetimeestimate and issue.fields.aggregatetimeestimate is not None:
                bug_ascii_data.append('* Estimate: {}'.format(issue.fields.aggregatetimeestimate))
            else:
                bug_ascii_data.append('* No Aggregate Time Estimate is available for the Issue --> {}'
                                      .format(self.issue_name_input))
            # Aggregate time original estimate
            bug_ascii_data.append('=== Aggregate Time Original Estimate')
            if issue.fields.aggregatetimeoriginalestimate and issue.fields.aggregatetimeoriginalestimate is not None:
                bug_ascii_data.append('* Estimate: {}'.format(issue.fields.aggregatetimeoriginalestimate))
            else:
                bug_ascii_data.append('* No Aggregate Time Estimate is available for the Issue --> {}'
                                      .format(self.issue_name_input))
            # Aggregate time spent
            bug_ascii_data.append('=== Aggregate Time Spent')
            if issue.fields.aggregatetimespent and issue.fields.aggregatetimespent is not None:
                bug_ascii_data.append('* Time Spent: {}'.format(issue.fields.aggregatetimespent))
            else:
                bug_ascii_data.append('* No Aggregate Time Spent is available for the Issue --> {}'
                                      .format(self.issue_name_input))
            # Attachments list
            bug_ascii_data.append('=== Attachments')
            if issue.fields.attachment:
                attachment_list = issue.fields.attachment
                if len(attachment_list) > 0:
                    counter_attachment_list = 1
                    for item in attachment_list:
                        bug_ascii_data.append('* Attachments Item {}:'.format(counter_attachment_list) + ' {}'.format(item))
                        counter_attachment_list += 1
                else:
                    bug_ascii_data.append('* There are no listed attachments for the Issue --> {}'
                                          .format(self.issue_name_input))
            # Comment object
            bug_ascii_data.append('=== Comments')
            if issue.fields.comment.comments:
                comments_object_list = issue.fields.comment.comments
                if len(comments_object_list) > 0:
                    counter_comments_object_list = 1
                    for item in comments_object_list:
                        bug_ascii_data.append('* Comment {}:'.format(counter_comments_object_list) + ' {}'.format(item.body))
                        counter_comments_object_list += 1
                else:
                    bug_ascii_data.append('* There are no listed comments for the Issue --> {}'
                                          .format(self.issue_name_input))
            # Components Name
            bug_ascii_data.append('=== Components')
            if issue.fields.components:
                components_list = issue.fields.components
                if len(components_list) > 0:
                    counter_components_list = 1
                    for item in components_list:
                        bug_ascii_data.append('* Component {}'.format(counter_components_list))
                        bug_ascii_data.append('** Name: {}'.format(item.name))
                        bug_ascii_data.append('** Description: {}'.format(item.description))
                        bug_ascii_data.append('** ID: {}'.format(item.id))
                        counter_components_list += 1
                else:
                    bug_ascii_data.append('* There is no Component list available for the Issue --> {}'
                                          .format(self.issue_name_input))
            # Environment
            bug_ascii_data.append('=== Environment')
            if issue.fields.environment and issue.fields.environment is not None:
                bug_ascii_data.append('* Environment: {}'.format(issue.fields.environment))
            else:
                bug_ascii_data.append('* There is no Environment set for the Issue --> {}'.format(self.issue_name_input))
            # Fix versions
            bug_ascii_data.append('=== Fix Versions List')
            # if issue.fields.fixVersions:
            fix_versions_list = issue.fields.fixVersions
            if len(fix_versions_list) > 0:
                counter_fix_versions_list = 1
                for item in fix_versions_list:
                    bug_ascii_data.append('* Version Item {}:'.format(counter_fix_versions_list) + ' {}'.format(item))
                    counter_fix_versions_list += 1
            else:
                bug_ascii_data.append('* There are no listed fixed versions for the Issue --> {}'
                                      .format(self.issue_name_input))
            # Issue links
            bug_ascii_data.append('=== Issue Links List')
            if issue.fields.issuelinks:
                issue_links_list = issue.fields.issuelinks
                if len(issue_links_list) > 0:
                    counter_issue_links_list = 1
                    for item in issue_links_list:
                        bug_ascii_data.append('* Issue Link Item {}:'.format(counter_issue_links_list) + ' {}'.format(item))
                        counter_issue_links_list += 1
                else:
                    bug_ascii_data.append('* There are no listed issue links for the Issue --> {}'
                                          .format(self.issue_name_input))
            # Labels
            bug_ascii_data.append('=== Labels List')
            if issue.fields.labels:
                labels_list = issue.fields.labels
                if len(labels_list) > 0:
                    counter_labels_list = 1
                    for item in labels_list:
                        bug_ascii_data.append('* Label Item {}:'.format(counter_labels_list) + ' {}'.format(item))
                        counter_labels_list += 1
                else:
                    bug_ascii_data.append('* There are not listed labels for the Issue --> {}'
                                          .format(self.issue_name_input))
            # Mro
            # print('Mro:', issue.fields.mro)  # ??????????????????????
            # print()
            # Progress object
            bug_ascii_data.append('=== Progress')
            if issue.fields.progress:
                bug_ascii_data.append('* Progress: {}'.format(issue.fields.progress.progress))
                bug_ascii_data.append('* Total: {}'.format(issue.fields.progress.total))
            else:
                bug_ascii_data.append('* No information about Progress is available.')
            # Reporter
            bug_ascii_data.append('=== Reporter')
            if issue.fields.reporter and issue.fields.reporter is not None:
                bug_ascii_data.append('* Display Name: {}'.format(issue.fields.reporter.displayName))
                bug_ascii_data.append('* Active: {}'.format(issue.fields.reporter.active))
                bug_ascii_data.append('* Name: {}'.format(issue.fields.reporter.name))
                bug_ascii_data.append('* Key: {}'.format(issue.fields.reporter.key))
                bug_ascii_data.append('* Timezone: {}'.format(issue.fields.reporter.timeZone))
            else:
                bug_ascii_data.append('*  The is no Reporter set for the Issue --> {}'.format(self.issue_name_input))
            # Resolution
            bug_ascii_data.append('=== Resolution')
            if issue.fields.resolution and issue.fields.resolution is not None:
                bug_ascii_data.append('* Resolution: {}'.format(issue.fields.resolution))
            else:
                bug_ascii_data.append('* No Resolution is stored at this time for the Issue --> {}'
                                      .format(self.issue_name_input))
            # Resolution date
            bug_ascii_data.append('=== Resolution Date')
            if issue.fields.resolutiondate and issue.fields.resolutiondate is not None:
                bug_ascii_data.append('* Date: {}'.format(issue.fields.resolutiondate))
            else:
                bug_ascii_data.append('* No resolution date is stored at this time for the Issue --> {}'
                                      .format(self.issue_name_input))
            # Sub-tasks
            bug_ascii_data.append('=== Sub-tasks')
            if issue.fields.subtasks:
                sub_tasks_list = issue.fields.subtasks
                if len(sub_tasks_list) > 0:
                    counter_sub_tasks = 1
                    for item in sub_tasks_list:
                        bug_ascii_data.append('* Sub-task {}:'.format(counter_sub_tasks) +
                                              ' {}'.format(issue.fields.subtasks[item]))
                        counter_sub_tasks += 1
                else:
                    bug_ascii_data.append('There are no listed sub-tasks at this time for the Issue --> {}'
                                          .format(self.issue_name_input))
            # Summary
            bug_ascii_data.append('=== Summary')
            if issue.fields.summary and issue.fields.summary is not None:
                bug_ascii_data.append('* Summary: {}'.format(issue.fields.summary))
            else:
                bug_ascii_data.append('* No summary is available now for the Issue --> {}'.format(self.issue_name_input))
            # Time estimate
            bug_ascii_data.append('=== Time Estimate')
            if issue.fields.timeestimate and issue.fields.timeestimate is not None:
                bug_ascii_data.append('* Estimate: {}'.format(issue.fields.timeestimate))
            else:
                bug_ascii_data.append('* No time-estimate is now available fo the Issue --> {}'.format(self.issue_name_input))
            # Time original estimate
            bug_ascii_data.append('=== Time Original Estimate')
            if issue.fields.timeoriginalestimate and issue.fields.timeoriginalestimate is not None:
                bug_ascii_data.append('* Estimate: {}'.format(issue.fields.timeoriginalestimate))
            else:
                bug_ascii_data.append('* No time-original-estimate is now available for the Issue --> {}'
                                      .format(self.issue_name_input))
            # Time spent
            bug_ascii_data.append('=== Time Spent')
            if issue.fields.timespent and issue.fields.timespent is not None:
                bug_ascii_data.append('* Time: {}'.format(issue.fields.timespent))
            else:
                bug_ascii_data.append('* No time-spent is now available for the Issue --> {}'.format(self.issue_name_input))
            # Updated Date
            bug_ascii_data.append('=== Updated Date')
            if issue.fields.updated and issue.fields.updated is not None:
                bug_ascii_data.append('* Date: {}'.format(issue.fields.updated))
            else:
                bug_ascii_data.append('* No updated-date is now available for the the Issue --> {}'
                                      .format(self.issue_name_input))
            # Versions list
            bug_ascii_data.append('=== Versions')
            if issue.fields.versions:
                versions_list = issue.fields.versions
                if len(versions_list) > 0:
                    counter_versions_list = 1
                    for item in versions_list:
                        bug_ascii_data.append('* Version {}'.format(counter_versions_list))
                        bug_ascii_data.append('** ID: {}'.format(item.id))
                        bug_ascii_data.append('** Name: {}'.format(item.name))
                        bug_ascii_data.append('** Description: {}'.format(item.description))
                        bug_ascii_data.append('** Archived: {}'.format(item.archived))
                        bug_ascii_data.append('** Released: {}'.format(item.released))
                        bug_ascii_data.append('** Release Date: {}'.format(item.releaseDate))
                        counter_versions_list += 1
                else:
                    bug_ascii_data.append('* The are no listed versions for the Issue --> {}'.format(self.issue_name_input))
            # Votes
            bug_ascii_data.append('=== Votes')
            if issue.fields.votes:
                bug_ascii_data.append('* Votes No.: {}'.format(issue.fields.votes.votes))
                bug_ascii_data.append('* has Voted: {}'.format(issue.fields.votes.hasVoted))
            else:
                bug_ascii_data.append('* Votes are not available at this time.')
            # Watchers object
            bug_ascii_data.append('=== Watchers')
            if issue.fields.watches.watchCount and issue.fields.watches.watchCount is not None:
                bug_ascii_data.append('* Watches: {}'.format(issue.fields.watches.watchCount))
                bug_ascii_data.append('* Watching: {}'.format(issue.fields.watches.isWatching))
            else:
                bug_ascii_data.append('No watches are available until now for the Issue: --> {}'
                                      .format(self.issue_name_input))
            # Work Ratio
            bug_ascii_data.append('=== Work Ratio')
            if issue.fields.workratio:
                bug_ascii_data.append('* Ratio: {}'.format(issue.fields.workratio))
            else:
                bug_ascii_data.append('* No Work Ratio available.')
            # Issue Work-logs
            bug_ascii_data.append('=== Issue Work-logs')
            if issue.fields.worklog:
                bug_ascii_data.append('* Start at: {}'.format(issue.fields.worklog.startAt))
                bug_ascii_data.append('* Max Results: {}'.format(issue.fields.worklog.maxResults))
                bug_ascii_data.append('* Total: {}'.format(issue.fields.worklog.total))
                work_logs_list = issue.fields.worklog.worklogs
                bug_ascii_data.append('* Work-logs List:')
                if len(work_logs_list) > 0:
                    counter_work_logs = 1
                    for item in work_logs_list:
                        bug_ascii_data.append('** Work-logs Item {}:'.format(counter_work_logs) + ' {}'.
                                              format(work_logs_list[item]))
                        counter_work_logs += 1
                else:
                    bug_ascii_data.append('** There are no listed work-logs at this time for the Issue --> {}'
                                          .format(self.issue_name_input))
            # print the list of asciidoc data
            # for item in bug_ascii_data:
            #     print(item)
            #     print('\n')
            return bug_ascii_data
        else:
            bug_ascii_data.append('== Bug ID: {}'.format(self.issue_name_input))
            bug_ascii_data.append('* There is no Bug with that ID.')


"""CLASS FOR RETRIEVING CUSTOM FIELDS ISSUE INFORMATION FROM JIRA API"""


class CustomFieldDataRetriever:
    def __init__(self, issue_name_input, custom_field_name, custom_field_id):
        self.issue_name_input = issue_name_input
        self.custom_field_name = custom_field_name
        self.custom_field_id = custom_field_id

    def data_retriever(self):
        bug_custom_fields_list_feed = []
        if self.issue_name_input is not None and self.custom_field_name is not None and self.custom_field_id is not None:
            bug_custom_fields_list_feed.append('== Custom Fields Section')
            if len(self.custom_field_name) == len(self.custom_field_id):
                customfield_list = zip(self.custom_field_name, self.custom_field_id)
                # JIRA API connection and connector object creation
                # connection to JIRA (again :) )
                jira_connection_obj = Connector()
                jira = jira_connection_obj.jira_connector()
                """Issue Definition"""
                # creating an issue object to fetch information later on from JIRA API
                print('Creating the custom fields issue object..')
                issue = jira.issue(self.issue_name_input)
                # taking custom fields to a list
                print('CUSTOM FIELDS JSON FILE CREATION')
                custom_fields_counter = 0
                custom_fields_list_from_api = []
                for field_name in issue.raw['fields']:
                    if field_name.startswith('customfield_'):
                        custom_fields_counter += 1
                        # print("Field:", field_name)
                        custom_fields_list_from_api.append(field_name)

                if len(custom_fields_list_from_api) > 0:
                    for item_id_search in customfield_list:
                        # Target Release (Custom Field)
                        custom_search = 'customfield_' + str(item_id_search[1])
                        for item_custom_field_api in custom_fields_list_from_api:
                            counter_match_found = 0
                            if item_custom_field_api == custom_search:
                                counter_match_found += 1
                                if counter_match_found > 0:
                                    print(item_id_search[0] + ' custom field found!')
                                    print('Name:', item_id_search[0], '-', 'Custom Field ID =', str(item_id_search[1]))
                                    bug_custom_fields_list_feed.append('=== ' + item_id_search[0])
                                    new_var = 'issue.fields.customfield_' + str(item_id_search[1])
                                    command = 'global temp; temp = ' + new_var
                                    exec(command)
                                    temp_doc_output = '* ' + item_id_search[0] + ': ' + str(temp)
                                    print(temp_doc_output)
                                    bug_custom_fields_list_feed.append(temp_doc_output)
                                    # temp_object = dir(temp)
                                    # print(type(temp_object))
                                    # print(temp_object)
                                    # dict_keys = temp.__dict__.keys()
                                    # print(dict_keys)
                                    # for item in dict_keys:
                                    #     if not item.startswith('_'):
                                    #         print('Index: ' + dict_keys.index(item))
                                    # print()
                                    # print()
                                    # print()
                                    # print()
                                    # print()
                                    # bug_custom_fields_list_feed.append('* Description: {}'.format(temp.description))
                                    # bug_custom_fields_list_feed.append('* Name: {}'.format(temp.name))
                                    # bug_custom_fields_list_feed.append('* Archived: {}'.format(temp.archived))
                                    # bug_custom_fields_list_feed.append('* Released: {}'.format(temp.released))
                                else:
                                    print(item_id_search[0] + ': There is no ' + item_id_search[0] +
                                          ' for the Issue --> {}'.format(self.issue_name_input))
                                    bug_custom_fields_list_feed.append(item_id_search[0] + ': There is no ' +
                                                                       item_id_search[0] + ' for the Issue --> {}'
                                                                       .format(self.issue_name_input))
                    print()
                    for item in bug_custom_fields_list_feed:
                        print(item)
                        print()

                    return bug_custom_fields_list_feed

        elif self.custom_field_id is None or self.custom_field_name is None:
            bug_custom_fields_list_feed.append('== Custom Fields Section')
            nothing_right_selected = '* No ID for custom field or custom field Name are selected.'
            print(nothing_right_selected)
            bug_custom_fields_list_feed.append(nothing_right_selected)
            return bug_custom_fields_list_feed

        else:
            bug_custom_fields_list_feed.append('== Custom Fields Section')
            nothing_found = '*  Something is not set right for the custom fields.'
            print(nothing_found)
            bug_custom_fields_list_feed.append(nothing_found)
            return bug_custom_fields_list_feed
