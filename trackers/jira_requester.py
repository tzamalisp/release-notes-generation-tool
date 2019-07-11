from jira import JIRA
import json
import requests
import os
from datetime import datetime
from pprint import pprint
from asciidoc_generator import GeneratorJira

from conf.configuration import JiraReadConfigurationServer
from conf.configuration import JiraReadConfigurationBasicAuth
from conf.configuration import JiraReadConfigurationOAuth
from conf.configuration import JiraReadConfigurationKerberos


"""CLASS FOR RETRIEVING BASIC ISSUE INFORMATION FROM JIRA API"""


class Connector:

    def jira_connector(self):
        """ JIRA Connection"""
        # JIRA connection credentials
        jira_connection = JiraReadConfigurationServer()
        server_value = jira_connection.read_server_conf()['server']

        jira_basic_auth = JiraReadConfigurationBasicAuth()
        username_value = jira_basic_auth.read_user_basic_auth()['username']
        username_reason = jira_basic_auth.read_user_basic_auth()['username_reason']
        print(username_reason)
        password_value = jira_basic_auth.read_user_basic_auth()['password']

        jira_oauth = JiraReadConfigurationOAuth()
        access_token_value = jira_oauth.read_oauth()['access_token']
        access_token_secret_value = jira_oauth.read_oauth()['access_token_secret']
        consumer_key_value = jira_oauth.read_oauth()['consumer_key']
        # code for key cert here:
        key_cert_data = None
        # with open(key_cert, 'r') as key_cert_file:
        #     key_cert_data = key_cert_file.read()

        jira_kerberos = JiraReadConfigurationKerberos()
        kerberos_value = bool(jira_kerberos.read_kerberos_auth()['kerberos'])
        kerberos_mutual_authentication_value = jira_kerberos.read_kerberos_auth()['kerberos_options']

        options = {
            'server': server_value,
            'basic_auth': (username_value, password_value),
            'oauth': {
                'access_token': access_token_value,
                'access_token_secret': access_token_secret_value,
                'consumer_key': consumer_key_value,
                'key_cert': key_cert_data
            },
            'kerberos': kerberos_value,
            'kerberos_options': {'mutual_authentication': kerberos_mutual_authentication_value}
        }

        # JIRA object for connecting to the API
        print('Connecting to the JIRA API..')
        jira_auth_connection = JIRA(options)
        print('Connected to JIRA API successfully!')
        return jira_auth_connection


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
        bug_ascii_data.append('== Bug ID: {}'.format(self.issue_name_input))

        # Retrieving selected fields of a JIRA issue and printing them
        print('PRINTING SELECTED FIELDS')
        print()
        # Project key
        print('Project Object:')
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
        for item in bug_ascii_data:
            print(item)
            print('\n')
        return bug_ascii_data


"""CLASS FOR CREATING CONFIGURATION FILE WITH USER'S WANTED CUSTOM FIELDS"""


class CustomFieldConfCreation:
    def __init__(self, name, field_id):
        self.name = name
        self.field_id = field_id

    def custom_field_configuration_creation(self):
        file_name = 'trackers/jira_user_custom_fields.json'
        user_custom_fields_list = []
        custom_field_entry = {self.name:  self.field_id}
        print('Writing wanted custom fields configuration file..')
        if not os.path.isfile(file_name):
            user_custom_fields_list.append(custom_field_entry)
            with open(file_name, mode='w', encoding='utf-8') as f:
                f.write(json.dumps(user_custom_fields_list, indent=4))
            print('Wanted custom fields configuration file is created successfully!')
        else:
            with open(file_name, encoding='utf-8') as feeds_json:
                feeds = json.load(feeds_json)

            feeds.append(custom_field_entry)
            with open(file_name, mode='w', encoding='utf-8') as f:
                f.write(json.dumps(feeds, indent=4))
            print('Wanted custom fields configuration file is updated successfully!')


"""CLASS FOR CREATING CUSTOM FIELDS LIST CONFIGURATION FILE FROM JIRA API"""


class CustomFieldListFile:
    def __init__(self, issue_name_input):
        self.issue_name_input = issue_name_input

    def list_file_generator(self):
        # JIRA API connection and connector object creation
        jira_connection_obj = Connector()
        jira = jira_connection_obj.jira_connector()

        # creating an issue object to fetch information later on from JIRA API
        print('Creating the custom fields issue object..')
        issue = jira.issue(self.issue_name_input)
        print()

        print('CUSTOM FIELDS JSON FILE CREATION:')
        custom_fields_counter = 0
        custom_fields_list = []
        for field_name in issue.raw['fields']:
            if field_name.startswith('customfield_'):
                custom_fields_counter += 1
                # print("Field:", field_name)
                custom_fields_list.append(field_name)
        if len(custom_fields_list) > 0:
            print('Custom Fields Number in JBOSS found:', custom_fields_counter)
            print('Writing custom fields list JSON file..')
            print('Writing..')
            custom_fields_list = {'custom_fields': custom_fields_list}
            customfields_json = 'trackers/jira_customfields_list.json'
            with open(customfields_json, 'w') as f:  # writing JSON object
                json.dump(custom_fields_list, f)
            print(
                'Configuration JSON file with the name "{}", which is related to custom fields, '
                'was created successfully!'.
                format(customfields_json))
            print()
        else:
            print('No custom fields were found to that issue.')


"""CLASS FOR RETRIEVING CUSTOM FIELDS ISSUE INFORMATION FROM JIRA API"""


class CustomFieldDataRetriever:
    def __init__(self, issue_name_input, custom_field_name, custom_field_id):
        self.issue_name_input = issue_name_input
        self.custom_field_name = custom_field_name
        self.custom_field_id = custom_field_id

    def data_retriever(self):
        # JIRA API connection and connector object creation
        jira_connection_obj = Connector()
        jira = jira_connection_obj.jira_connector()

        """Issue Definition"""
        # creating an issue object to fetch information later on from JIRA API
        print('Creating the custom fields issue object..')
        issue = jira.issue(self.issue_name_input)
        print()

        bug_custom_fields_list_feed = []

        # Target Release (Custom Field)
        with open('trackers/jira_customfields_list.json') as json_file:
            data = json.load(json_file)
        custom_search = 'customfield_' + str(self.custom_field_id)
        custom_fields_list_read = data['custom_fields']
        for item in custom_fields_list_read:
            if item == custom_search:
                print(self.custom_field_name + ' custom field found!')
                print(self.custom_field_name + ':')
                print('Name:', self.custom_field_name, '-', 'Custom Field ID =', str(self.custom_field_id))
                bug_custom_fields_list_feed.append('=== ' + self.custom_field_name)
                new_var = 'issue.fields.customfield_' + str(self.custom_field_id)
                command = 'global temp; temp = ' + new_var
                # print(command)
                exec(command)
                if temp is not None:
                    print('\tDescription:', temp.description)
                    bug_custom_fields_list_feed.append('* Description: {}'.format(temp.description))
                    print('\tName:', temp.name)
                    bug_custom_fields_list_feed.append('* Name: {}'.format(temp.name))
                    print('\tArchived:', temp.archived)
                    bug_custom_fields_list_feed.append('* Archived: {}'.format(temp.archived))
                    print('\tReleased:', temp.released)
                    bug_custom_fields_list_feed.append('* Released: {}'.format(temp.released))
                    print()
                # else:
                #     print(self.custom_field_name + ': There is no ' + self.custom_field_name + ' for the Issue --> {}'
                #           .format(self.issue_name_input))
                #
                #     print()
        print()
        for item in bug_custom_fields_list_feed:
            print(item)
            print()

        return bug_custom_fields_list_feed
