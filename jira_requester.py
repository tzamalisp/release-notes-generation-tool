from jira import JIRA
import json
import requests
import os


"""CLASS FOR CREATING CONFIGURATION FILE WITH USER'S CUSTOM FIELDS"""


class CustomFieldConfCreation:
    def __init__(self, name, field_id):
        self.name = name
        self.field_id = field_id

    def custom_field_configuration_creation(self):
        file_name = 'user_custom_fields.json'
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


"""CLASS FOR RETRIEVING BASIC ISSUE INFORMATION FROM JIRA API"""


class Connector:
    def jira_connector(self):
        """ JIRA Connection"""
        # JIRA connection credentials
        options = {
            'server': 'https://issues.jboss.org/',
            'basic_auth': ('<username>', '<password>'),
            'oauth': {
                'access_token': '',
                'access_token_secret': '',
                'consumer_key': '',
                'key_cert': ''
            }
        }

        # JIRA object for connecting to the API
        print('Connecting to the JIRA API..')
        jira = JIRA(options)
        print('Connected to JIRA API successfully!')
        return jira


class BasicDataRetriever:
    def __init__(self, issue_name_input):
        self.issue_name_input = issue_name_input

    def data_retriever(self):
        # JIRA API connection and connector object creation
        jira_connection_obj = Connector()
        jira = jira_connection_obj.jira_connector()

        """Issue Definition"""
        # creating an issue object to fetch information later on from JIRA API
        print('Creating the issue object..')
        issue = jira.issue(self.issue_name_input)
        print()

        # Retrieving selected fields of a JIRA issue and printing them
        print('PRINTING SELECTED FIELDS')
        print()
        # Project key
        print('Project Object:')
        project_url = issue.fields.project.self
        print('\tProject JSON:', project_url)
        print('\tProject Key:', issue.fields.project.key)  # 'JRA'
        print('\tProject Name:', issue.fields.project.name)
        print('\tProject ID:', issue.fields.project.id)
        print('\tProject Category Name:', issue.fields.project.projectCategory.name)
        print('\tProject Category Description:', issue.fields.project.projectCategory.description)
        r = requests.get(project_url)
        data = r.json()
        print('\tProject Avatar:', data['avatarUrls']['48x48'])
        print()
        # Issue type
        print('Issue Type:')
        if issue.fields.issuetype.name is not None:
            print('\tName:', issue.fields.issuetype.name)  # 'New Feature'
            print('\tDescription:', issue.fields.issuetype.description)
            print('\tAvatar:', issue.fields.issuetype.iconUrl)
        else:
            print('\tThere is no Type defined for the Issue --> {}'.format(self.issue_name_input))
        print()
        # Reporter display name
        if issue.fields.reporter.displayName is not None:
            print('Reporter Display name:', issue.fields.reporter.displayName)  # 'Mike Cannon-Brookes [Atlassian]'
        else:
            print('Reporter Display name: There is no Display Name for the Issue --> {}'.format(self.issue_name_input))
        print()
        # Created datetime
        if issue.fields.created is not None:
            print('Created at:', issue.fields.created)
        else:
            print('Created at: There is no Date-Time value stored for the Issue --> {}'.format(self.issue_name_input))
        print()
        # Assignee
        print('Assignee:')
        if issue.fields.assignee is not None:
            print('\tDisplay Name:', issue.fields.assignee.displayName)
            print('\tName:', issue.fields.assignee.name)
            print('\tKey:', issue.fields.assignee.key)
            print('\tActive:', issue.fields.assignee.active)
            print('\ttimeZone:', issue.fields.assignee.timeZone)
        else:
            print('Assignee: Assignee is not stored for the Issue --> {}'.format(self.issue_name_input))
        print()
        # Issue description
        if issue.fields.description is not None:
            print('Issue Description:', issue.fields.description)
        else:
            print('Issue Description: Description is not available for that Issue --> {}'.format(self.issue_name_input))
        print()
        # Current Status
        print('Status:')
        if issue.fields.status is not None:
            print('\tName:', issue.fields.status.name)
            print('\tDescription:', issue.fields.status.description)
            print('\tStatus Category Name:', issue.fields.status.statusCategory.name)
            print('\tIcon:', issue.fields.status.iconUrl)
        else:
            print('Status: No status is set for the Issue --> {}'.format(self.issue_name_input))
        print()
        # Aggregate progress
        print('Aggregate progress:')
        print('\tProgress:', issue.fields.aggregateprogress.progress)
        print('\tTotal:', issue.fields.aggregateprogress.total)
        print()
        # Aggregate time estimate
        if issue.fields.aggregatetimeestimate is not None:
            print('Aggregate Time Estimate:', issue.fields.aggregatetimeestimate)
        else:
            print('Aggregate Time Estimate: No Aggregate time estimate is available for the Issue --> {}'
                  .format(self.issue_name_input))
        print()
        # Aggregate time original estimate
        if issue.fields.aggregatetimeoriginalestimate is not None:
            print('Aggregate Time Original Estimate:', issue.fields.aggregatetimeoriginalestimate)
        else:
            print('Aggregate Time Original Estimate: No Aggregate time estimate is available for the Issue --> {}'
                  .format(self.issue_name_input))
        print()
        # Aggregate time spent
        if issue.fields.aggregatetimespent is not None:
            print('Aggregate Time Spent:', issue.fields.aggregatetimespent)
        else:
            print('Aggregate Time Spent: No Aggregate time spent is available for the Issue --> {}'
                  .format(self.issue_name_input))
        print()
        # Attachments list
        print('Attachments List:')
        attachment_list = issue.fields.attachment
        if len(attachment_list) > 0:
            counter_attachment_list = 1
            for item in attachment_list:
                print('\tAttachments Item {}:'.format(counter_attachment_list), item)
                counter_attachment_list += 1
        else:
            print('\tThere are no listed attachments for the Issue --> {}'.format(self.issue_name_input))
        print()
        # Comment object
        print('Comments Object')
        comments_object_list = issue.fields.comment.comments
        if len(comments_object_list) > 0:
            counter_comments_object_list = 1
            for item in comments_object_list:
                print('\tComment {}'.format(counter_comments_object_list), item.body)
                counter_comments_object_list += 1
        else:
            print('There are no listed comments for the Issue --> {}'.format(self.issue_name_input))
        print()
        # Components Name
        print('Components:')
        components_list = issue.fields.components
        if len(components_list) > 0:
            counter_components_list = 1
            for item in components_list:
                print('\tComponent {}'.format(counter_components_list))
                print('\t\tName:', item.name)
                print('\t\tDescription:', item.description)
                print('\t\tID:', item.id)
                counter_components_list += 1
        else:
            print('Components Name: There is no Component list available for the Issue --> {}'.format(self.issue_name_input))
        print()
        # Environment
        if issue.fields.environment is not None:
            print('Environment:', issue.fields.environment)
        else:
            print('Environment: There is no Environment set for the Issue --> {}'.format(self.issue_name_input))
        print()
        # Fix versions
        print('Fix Versions List:')
        fix_versions_list = issue.fields.fixVersions
        if len(fix_versions_list) > 0:
            counter_fix_versions_list = 1
            for item in fix_versions_list:
                print('\tVersion Item {}:'.format(counter_fix_versions_list), item)
                counter_fix_versions_list += 1
        else:
            print('\tThere are no listed fixed versions for the Issue --> {}'.format(self.issue_name_input))
        print()
        # Issue links
        print('Issue Links List:')
        issue_links_list = issue.fields.issuelinks
        if len(issue_links_list) > 0:
            counter_issue_links_list = 1
            for item in issue_links_list:
                print('\tIssue Link Item {}:'.format(counter_issue_links_list), item)
                counter_issue_links_list += 1
        else:
            print('\tThere are no listed issue links for the Issue --> {}'.format(self.issue_name_input))
        print()
        # Issue Type object
        if issue.fields.issuetype is not None:
            print('Issue Type:', issue.fields.issuetype)
        else:
            print('Issue Type: No issue type is defined for the Issue --> {}'.format(self.issue_name_input))
        print()
        # Labels
        print('Labels List:')
        labels_list = issue.fields.labels
        if len(labels_list) > 0:
            counter_labels_list = 1
            for item in labels_list:
                print('\tLabel Item {}:'.format(counter_labels_list), item)
                counter_labels_list += 1
        else:
            print('\tThere are not listed labels for the Issue --> {}'.format(self.issue_name_input))
        print()
        # Mro
        print('Mro:', issue.fields.mro)  # ??????????????????????
        print()
        # Progress object
        print('Progress Object:')
        print('\tProgress:', issue.fields.progress.progress)
        print('\tTotal:', issue.fields.progress.total)
        print()
        # Project name
        print('Project name:', issue.fields.project.name)
        print()
        # Reporter
        print('Reporter:')
        if issue.fields.reporter is not None:
            print('\tDisplay Name:', issue.fields.reporter.displayName)
            print('\tActive:', issue.fields.reporter.active)
            print('\tName:', issue.fields.reporter.name)
            print('\tKey:', issue.fields.reporter.key)
            print('\tTimezone:', issue.fields.reporter.timeZone)
        else:
            print('Reporter: The is no reporter set for the Issue --> {}'.format(self.issue_name_input))
        print()
        # Resolution
        if issue.fields.resolution is not None:
            print('Resolution:', issue.fields.resolution)
        else:
            print('Resolution: No resolution is stored at this time for the Issue --> {}'.format(self.issue_name_input))
        print()
        # Resolution date
        if issue.fields.resolutiondate is not None:
            print('Resolution date:', issue.fields.resolutiondate)
        else:
            print('Resolution date: No resolution date is stored at this time for the Issue --> {}'
                  .format(self.issue_name_input))
        print()
        # Sub-tasks
        print('Sub-tasks List:')
        sub_tasks_list = issue.fields.subtasks
        if len(sub_tasks_list) > 0:
            counter_sub_tasks = 1
            for item in sub_tasks_list:
                print('\tSub-task {}:'.format(counter_sub_tasks), issue.fields.subtasks[item])
                counter_sub_tasks += 1
        else:
            print('\tThere are no listed sub-tasks at this time for the Issue --> {}'.format(self.issue_name_input))
        print()
        # Summary
        if issue.fields.summary is not None:
            print('Summary:', issue.fields.summary)
        else:
            print('Summary: No summary is available now for the Issue -->'.format(self.issue_name_input))
        print()
        # Time estimate
        if issue.fields.timeestimate is not None:
            print('Time Estimate:', issue.fields.timeestimate)
        else:
            print('Time Estimate: No time-estimate is now available fo the Issue -->'.format(self.issue_name_input))
        print()
        # Time original estimate
        if issue.fields.timeoriginalestimate is not None:
            print('Time Original Estimate:', issue.fields.timeoriginalestimate)
        else:
            print('Time Original Estimate: No time-original-estimate is now available for the Issue -->'
                  .format(self.issue_name_input))
        print()
        # Time spent
        if issue.fields.timespent is not None:
            print('Time Spent:', issue.fields.timespent)
        else:
            print('Time Spent: No time-spent is now available for the Issue -->'.format(self.issue_name_input))
        print()
        # Updated Date
        if issue.fields.updated is not None:
            print('Updated Date:', issue.fields.updated)
        else:
            print('Updated Date: No updated-date is now available for the the Issue -->'.format(self.issue_name_input))
        print()
        # Versions array
        print('Versions:')
        versions_list = issue.fields.versions
        if len(versions_list) > 0:
            counter_versions_list = 1
            for item in versions_list:
                print('\tVersion {}'.format(counter_versions_list))
                print('\t\tid:', item.id)
                print('\t\tName:', item.name)
                print('\t\tDescription:', item.description)
                print('\t\tArchived:', item.archived)
                print('\t\tReleased:', item.released)
                print('\t\tRelease Date', item.releaseDate)
                counter_versions_list += 1
        else:
            print('\tThe are no listed versions for the Issue --> {}'.format(self.issue_name_input))
        print()
        # Votes
        print('Votes:')
        print('\tVotes No.:', issue.fields.votes.votes)
        print('\thas Voted:', issue.fields.votes.hasVoted)
        print()
        # Watchers object
        print('Watchers:')
        if issue.fields.watches.watchCount is not None:
            print('\tWatches:', issue.fields.watches.watchCount)
            print('\tWatching:', issue.fields.watches.isWatching)
        else:
            print('\tNo watches are available until now for the Issue: --> {}'.format(self.issue_name_input))
        print()
        # Work Ratio
        print('Work Ratio:', issue.fields.workratio)
        print()
        print('Issue Work-logs:')
        print('\tStart at:', issue.fields.worklog.startAt)
        print('\tMax Results:', issue.fields.worklog.maxResults)
        print('\tTotal:', issue.fields.worklog.total)
        work_logs_list = issue.fields.worklog.worklogs
        if len(work_logs_list) > 0:
            counter_work_logs = 1
            for item in work_logs_list:
                print('\tWork-logs Item {}:'.format(counter_work_logs), work_logs_list[item])
                counter_work_logs += 1
        else:
            print('\tWork-logs List: There are no listed work-logs at this time for the Issue'.format(self.issue_name_input))
        print()


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
        print('Custom Fields Number in JBOSS found:', custom_fields_counter)
        print('Writing custom fields list JSON file..')
        print('Writing..')
        custom_fields_list = {'custom_fields': custom_fields_list}
        customfields_json = 'customfields_list.json'
        with open(customfields_json, 'w') as f:  # writing JSON object
            json.dump(custom_fields_list, f)
        print(
            'Configuration JSON file with the name "{}", which is related to custom fields, was created successfully!'.
            format(customfields_json))
        print()


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

        # Target Release (Custom Field)
        with open('customfields_list.json') as json_file:
            data = json.load(json_file)
        custom_search = 'customfield_' + str(field_id)
        custom_fields_list_read = data['custom_fields']
        for item in custom_fields_list_read:
            if item == custom_search:
                print(self.custom_field_name + ' customfield found!')
                print(self.custom_field_name + ':')
                print('Name:', self.custom_field_name, '-', 'Custom Field ID =', str(self.custom_field_id))
                new_var = 'issue.fields.customfield_' + str(field_id)
                command = 'global temp; temp = ' + new_var
                # print(command)
                exec(command)
                if temp is not None:
                    print('\tDescription:', temp.description)
                    print('\tName:', temp.name)
                    print('\tArchived:', temp.archived)
                    print('\tReleased:', temp.released)
                    print()
                else:
                    print(self.custom_field_name + ': There is no ' + self.custom_field_name + ' for the Issue --> {}'
                          .format(self.issue_name_input))
                    print()


if __name__ == '__main__':
    issue_name = 'JBCS-535'
    name_field_id_name = 'Target Release'
    field_id = 12311240

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

    # BASIC DATA RETRIEVER
    print('BASIC DATA RETRIEVER')
    print()
    jira_basic_data = BasicDataRetriever(issue_name)
    jira_basic_data.data_retriever()

    print()
    print('---------------------------------------------')
    print('---------------------------------------------')
    print()

    # CUSTOM FIELD DATA RETRIEVER
    print('CUSTOM FIELD DATA RETRIEVER')
    print()
    jira_custom_field_data = CustomFieldDataRetriever(issue_name, name_field_id_name, field_id)
    jira_custom_field_data.data_retriever()

    print()
    print()
    print('>>> Calling JIRA API and printing Issue parts is now completed successfully!')
