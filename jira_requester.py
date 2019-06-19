from jira import JIRA
import json
import requests
import os
from datetime import datetime
from pprint import pprint
from asciidoc_generator import Generator

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
            print('\tProject JSON URL:', project_url + '[{}]'.format(self.issue_name_input))
            bug_ascii_data.append('* Project JSON URL: ' + project_url + '[{}]'.format(self.issue_name_input))
            print('\tProject Key:', issue.fields.project.key)  # 'JRA'
            bug_ascii_data.append('* Project Key: {}'.format(issue.fields.project.key))
            print('\tProject Name:', issue.fields.project.name)
            bug_ascii_data.append('* Project Name: {}'.format(issue.fields.project.name))
            print('\tProject ID:', issue.fields.project.id)
            bug_ascii_data.append('* Project ID: {}'.format(issue.fields.project.id))
            print('\tProject Category Name:', issue.fields.project.projectCategory.name)
            bug_ascii_data.append('* Project Category Name: {}'.format(issue.fields.project.projectCategory.name))
            print('\tProject Category Description:', issue.fields.project.projectCategory.description)
            bug_ascii_data.append('* Project Category Description: {}'.
                                  format(issue.fields.project.projectCategory.description))
            r = requests.get(project_url)
            data = r.json()
            print('\tProject Avatar:', data['avatarUrls']['48x48'])
            bug_ascii_data.append('* Project Avatar: {}'.format(data['avatarUrls']['48x48']))
        else:
            print('Nothing to show.')
            bug_ascii_data.append('* No information to show about the Project.')
        print()
        # Issue type
        print('Issue Type:')
        bug_ascii_data.append('=== Issue Type')
        if issue.fields.issuetype.name and issue.fields.issuetype.name is not None:
            print('\tName:', issue.fields.issuetype.name)  # 'New Feature'
            bug_ascii_data.append('* Name: {}'.format(issue.fields.issuetype.name))
            print('\tDescription:', issue.fields.issuetype.description)
            bug_ascii_data.append('* Description: {}'.format(issue.fields.issuetype.description))
            print('\tAvatar:', issue.fields.issuetype.iconUrl)
            bug_ascii_data.append('* Avatar: {}'.format(issue.fields.issuetype.iconUrl))
        else:
            print('\tThere is no Type defined for the Issue --> {}'.format(self.issue_name_input))
            bug_ascii_data.append('* There is no Type defined for the Issue --> {}'.format(self.issue_name_input))
        print()
        # Reporter Display Name
        print('Reporter Display Name:')
        bug_ascii_data.append('=== Reporter Display Name')
        if issue.fields.reporter.displayName and issue.fields.reporter.displayName is not None:
            print('Reporter Display name:', issue.fields.reporter.displayName)  # 'Mike Cannon-Brookes [Atlassian]'
            bug_ascii_data.append('* Display Name: {}'.format(issue.fields.reporter.displayName))
        else:
            print('Reporter Display name: There is no Display Name for the Issue --> {}'.format(self.issue_name_input))
            bug_ascii_data.append('* There is no Display Name for the Issue --> {}'.
                                  format(self.issue_name_input))
        print()
        # Created datetime
        print('Created datetime:')
        bug_ascii_data.append('=== Created DateTime')
        if issue.fields.created and issue.fields.created is not None:
            print('Created at:', issue.fields.created)
            bug_ascii_data.append('* Created at: {}'.format(issue.fields.created))
        else:
            print('Created at: There is no DateTime value stored for the Issue --> {}'.format(self.issue_name_input))
            bug_ascii_data.append('* There is no DateTime value stored for the Issue --> {}'
                                  .format(self.issue_name_input))
        print()
        # Assignee
        print('Assignee:')
        bug_ascii_data.append('=== Assignee')
        if issue.fields.assignee and issue.fields.assignee is not None:
            print('\tDisplay Name:', issue.fields.assignee.displayName)
            bug_ascii_data.append('* Display Name: {}'.format(issue.fields.assignee.displayName))
            print('\tName:', issue.fields.assignee.name)
            bug_ascii_data.append('* Name: {}'.format(issue.fields.assignee.name))
            print('\tKey:', issue.fields.assignee.key)
            bug_ascii_data.append('* Key: {}'.format(issue.fields.assignee.key))
            print('\tActive:', issue.fields.assignee.active)
            bug_ascii_data.append('* Active: {}'.format('issue.fields.assignee.active'))
            print('\ttimeZone:', issue.fields.assignee.timeZone)
            bug_ascii_data.append('* TimeZone: {}'.format(issue.fields.assignee.timeZone))
        else:
            print('Assignee: Assignee is not stored for the Issue --> {}'.format(self.issue_name_input))
            bug_ascii_data.append('* Assignee is not stored for the Issue --> {}'
                                  .format(self.issue_name_input))
        print()
        # Issue description
        print('Issue description:')
        bug_ascii_data.append('=== Issue Description')
        if issue.fields.description and issue.fields.description is not None:
            print('Description:', issue.fields.description)
            bug_ascii_data.append('* Description: {}'.format(issue.fields.description))
        else:
            print('Issue Description: Description is not available for that Issue --> {}'.format(self.issue_name_input))
            bug_ascii_data.append('* Description is not available for that Issue --> {}'
                                  .format(self.issue_name_input))
        print()
        # Current Status
        print('Status:')
        bug_ascii_data.append('=== Status')
        if issue.fields.status and issue.fields.status is not None:
            print('\tName:', issue.fields.status.name)
            bug_ascii_data.append('* Name: {}'.format(issue.fields.status.name))
            print('\tDescription:', issue.fields.status.description)
            bug_ascii_data.append('* Description: {}'.format(issue.fields.status.description))
            print('\tStatus Category Name:', issue.fields.status.statusCategory.name)
            bug_ascii_data.append('* Status Category Name: {}'.format(issue.fields.status.statusCategory.name))
            print('\tIcon:', issue.fields.status.iconUrl)
            bug_ascii_data.append('* Icon: {}'.format(issue.fields.status.iconUrl))
        else:
            print('Status: No status is set for the Issue --> {}'.format(self.issue_name_input))
            bug_ascii_data.append('* No Status is set for the Issue --> {}'.format(self.issue_name_input))
        print()
        # Aggregate progress
        print('Aggregate Progress:')
        bug_ascii_data.append('=== Aggregate Progress')
        if issue.fields.aggregateprogress:
            print('\tProgress:', issue.fields.aggregateprogress.progress)
            bug_ascii_data.append('* Progress: {}'.format(issue.fields.aggregateprogress.progress))
            print('\tTotal:', issue.fields.aggregateprogress.total)
            bug_ascii_data.append('* Total: {}'.format(issue.fields.aggregateprogress.total))
        else:
            bug_ascii_data.append('* No information about Aggregate Progress is available.')
        print()
        # Aggregate time estimate
        print('Aggregate time estimate:')
        bug_ascii_data.append('=== Aggregate Time Estimate')
        if issue.fields.aggregatetimeestimate and issue.fields.aggregatetimeestimate is not None:
            print('Aggregate Time Estimate:', issue.fields.aggregatetimeestimate)
            bug_ascii_data.append('* Estimate: {}'.format(issue.fields.aggregatetimeestimate))
        else:
            print('Aggregate Time Estimate: No Aggregate time estimate is available for the Issue --> {}'
                  .format(self.issue_name_input))
            bug_ascii_data.append('* No Aggregate Time Estimate is available for the Issue --> {}'
                                  .format(self.issue_name_input))
        print()
        # Aggregate time original estimate
        print('Aggregate time original estimate:')
        bug_ascii_data.append('=== Aggregate Time Original Estimate')
        if issue.fields.aggregatetimeoriginalestimate and issue.fields.aggregatetimeoriginalestimate is not None:
            print('Estimate:', issue.fields.aggregatetimeoriginalestimate)
            bug_ascii_data.append('* Estimate: {}'.format(issue.fields.aggregatetimeoriginalestimate))
        else:
            print('Aggregate Time Original Estimate: No Aggregate time estimate is available for the Issue --> {}'
                  .format(self.issue_name_input))
            bug_ascii_data.append('* No Aggregate Time Estimate is available for the Issue --> {}'
                                  .format(self.issue_name_input))
        print()
        # Aggregate time spent
        print('Aggregate time spent:')
        bug_ascii_data.append('=== Aggregate Time Spent')
        if issue.fields.aggregatetimespent and issue.fields.aggregatetimespent is not None:
            print('Aggregate Time Spent:', issue.fields.aggregatetimespent)
            bug_ascii_data.append('* Time Spent: {}'.format(issue.fields.aggregatetimespent))
        else:
            print('Aggregate Time Spent: No Aggregate time spent is available for the Issue --> {}'
                  .format(self.issue_name_input))
            bug_ascii_data.append('* No Aggregate Time Spent is available for the Issue --> {}'
                                  .format(self.issue_name_input))
        print()
        # Attachments list
        print('Attachments:')
        bug_ascii_data.append('=== Attachments')
        if issue.fields.attachment:
            attachment_list = issue.fields.attachment
            if len(attachment_list) > 0:
                counter_attachment_list = 1
                for item in attachment_list:
                    print('\tAttachments Item {}:'.format(counter_attachment_list), item)
                    bug_ascii_data.append('* Attachments Item {}:'.format(counter_attachment_list) + ' {}'.format(item))
                    counter_attachment_list += 1
            else:
                print('\tThere are no listed attachments for the Issue --> {}'.format(self.issue_name_input))
                bug_ascii_data.append('* There are no listed attachments for the Issue --> {}'
                                      .format(self.issue_name_input))
        print()
        # Comment object
        print('Comments')
        bug_ascii_data.append('=== Comments')
        if issue.fields.comment.comments:
            comments_object_list = issue.fields.comment.comments
            if len(comments_object_list) > 0:
                counter_comments_object_list = 1
                for item in comments_object_list:
                    print('\tComment {}:'.format(counter_comments_object_list), item.body)
                    bug_ascii_data.append('* Comment {}:'.format(counter_comments_object_list) + ' {}'.format(item.body))
                    counter_comments_object_list += 1
            else:
                print('There are no listed comments for the Issue --> {}'.format(self.issue_name_input))
                bug_ascii_data.append('* There are no listed comments for the Issue --> {}'
                                      .format(self.issue_name_input))
        print()
        # Components Name
        print('Components:')
        bug_ascii_data.append('=== Components')
        if issue.fields.components:
            components_list = issue.fields.components
            if len(components_list) > 0:
                counter_components_list = 1
                for item in components_list:
                    print('\tComponent {}'.format(counter_components_list))
                    bug_ascii_data.append('* Component {}'.format(counter_components_list))
                    print('\t\tName:', item.name)
                    bug_ascii_data.append('** Name: {}'.format(item.name))
                    print('\t\tDescription:', item.description)
                    bug_ascii_data.append('** Description: {}'.format(item.description))
                    print('\t\tID:', item.id)
                    bug_ascii_data.append('** ID: {}'.format(item.id))
                    counter_components_list += 1
            else:
                print('Components Name: There is no Component list available for the Issue --> {}'
                      .format(self.issue_name_input))
                bug_ascii_data.append('* There is no Component list available for the Issue --> {}'
                                      .format(self.issue_name_input))
        print()
        # Environment
        print('Environment:')
        bug_ascii_data.append('=== Environment')
        if issue.fields.environment and issue.fields.environment is not None:
            print('Environment:', issue.fields.environment)
            bug_ascii_data.append('* Environment: {}'.format(issue.fields.environment))
        else:
            print('Environment: There is no Environment set for the Issue --> {}'.format(self.issue_name_input))
            bug_ascii_data.append('* There is no Environment set for the Issue --> {}'.format(self.issue_name_input))
        print()
        # Fix versions
        print('Fix Versions List:')
        bug_ascii_data.append('=== Fix Versions List')
        # if issue.fields.fixVersions:
        fix_versions_list = issue.fields.fixVersions
        if len(fix_versions_list) > 0:
            counter_fix_versions_list = 1
            for item in fix_versions_list:
                print('\tVersion Item {}:'.format(counter_fix_versions_list), item)
                bug_ascii_data.append('* Version Item {}:'.format(counter_fix_versions_list) + ' {}'.format(item))
                counter_fix_versions_list += 1
        else:
            print('\tThere are no listed fixed versions for the Issue --> {}'.format(self.issue_name_input))
            bug_ascii_data.append('* There are no listed fixed versions for the Issue --> {}'
                                  .format(self.issue_name_input))
        print()
        # Issue links
        print('Issue Links List:')
        bug_ascii_data.append('=== Issue Links List')
        if issue.fields.issuelinks:
            issue_links_list = issue.fields.issuelinks
            if len(issue_links_list) > 0:
                counter_issue_links_list = 1
                for item in issue_links_list:
                    print('\tIssue Link Item {}:'.format(counter_issue_links_list), item)
                    bug_ascii_data.append('* Issue Link Item {}:'.format(counter_issue_links_list) + ' {}'.format(item))
                    counter_issue_links_list += 1
            else:
                print('\tThere are no listed issue links for the Issue --> {}'.format(self.issue_name_input))
                bug_ascii_data.append('* There are no listed issue links for the Issue --> {}'
                                      .format(self.issue_name_input))
        print()
        # Labels
        print('Labels List:')
        bug_ascii_data.append('=== Labels List')
        if issue.fields.labels:
            labels_list = issue.fields.labels
            if len(labels_list) > 0:
                counter_labels_list = 1
                for item in labels_list:
                    print('\tLabel Item {}:'.format(counter_labels_list), item)
                    bug_ascii_data.append('* Label Item {}:'.format(counter_labels_list) + ' {}'.format(item))
                    counter_labels_list += 1
            else:
                print('\tThere are not listed labels for the Issue --> {}'.format(self.issue_name_input))
                bug_ascii_data.append('* There are not listed labels for the Issue --> {}'
                                      .format(self.issue_name_input))
        print()
        # Mro
        # print('Mro:', issue.fields.mro)  # ??????????????????????
        # print()
        # Progress object
        print('Progress Object:')
        bug_ascii_data.append('=== Progress')
        if issue.fields.progress:
            print('\tProgress:', issue.fields.progress.progress)
            bug_ascii_data.append('* Progress: {}'.format(issue.fields.progress.progress))
            print('\tTotal:', issue.fields.progress.total)
            bug_ascii_data.append('* Total: {}'.format(issue.fields.progress.total))
        else:
            bug_ascii_data.append('* No information about Progress is available.')
        print()
        # Reporter
        print('Reporter:')
        bug_ascii_data.append('=== Reporter')
        if issue.fields.reporter and issue.fields.reporter is not None:
            print('\tDisplay Name:', issue.fields.reporter.displayName)
            bug_ascii_data.append('* Display Name: {}'.format(issue.fields.reporter.displayName))
            print('\tActive:', issue.fields.reporter.active)
            bug_ascii_data.append('* Active: {}'.format(issue.fields.reporter.active))
            print('\tName:', issue.fields.reporter.name)
            bug_ascii_data.append('* Name: {}'.format(issue.fields.reporter.name))
            print('\tKey:', issue.fields.reporter.key)
            bug_ascii_data.append('* Key: {}'.format(issue.fields.reporter.key))
            print('\tTimezone:', issue.fields.reporter.timeZone)
            bug_ascii_data.append('* Timezone: {}'.format(issue.fields.reporter.timeZone))
        else:
            print('Reporter: The is no reporter set for the Issue --> {}'.format(self.issue_name_input))
            bug_ascii_data.append('*  The is no Reporter set for the Issue --> {}'.format(self.issue_name_input))
        print()
        # Resolution
        print('Resolution:')
        bug_ascii_data.append('=== Resolution')
        if issue.fields.resolution and issue.fields.resolution is not None:
            print('Resolution:', issue.fields.resolution)
            bug_ascii_data.append('* Resolution: {}'.format(issue.fields.resolution))
        else:
            print('Resolution: No resolution is stored at this time for the Issue --> {}'.format(self.issue_name_input))
            bug_ascii_data.append('* No Resolution is stored at this time for the Issue --> {}'
                                  .format(self.issue_name_input))
        print()
        # Resolution date
        print('Resolution date:')
        bug_ascii_data.append('=== Resolution Date')
        if issue.fields.resolutiondate and issue.fields.resolutiondate is not None:
            print('Date:', issue.fields.resolutiondate)
            bug_ascii_data.append('* Date: {}'.format(issue.fields.resolutiondate))
        else:
            print('No resolution date is stored at this time for the Issue --> {}'
                  .format(self.issue_name_input))
            bug_ascii_data.append('* No resolution date is stored at this time for the Issue --> {}'
                                  .format(self.issue_name_input))
        print()
        # Sub-tasks
        print('Sub-tasks List:')
        bug_ascii_data.append('=== Sub-tasks')
        if issue.fields.subtasks:
            sub_tasks_list = issue.fields.subtasks
            if len(sub_tasks_list) > 0:
                counter_sub_tasks = 1
                for item in sub_tasks_list:
                    print('\tSub-task {}:'.format(counter_sub_tasks), issue.fields.subtasks[item])
                    bug_ascii_data.append('* Sub-task {}:'.format(counter_sub_tasks) +
                                          ' {}'.format(issue.fields.subtasks[item]))
                    counter_sub_tasks += 1
            else:
                print('\tThere are no listed sub-tasks at this time for the Issue --> {}'.format(self.issue_name_input))
                bug_ascii_data.append('There are no listed sub-tasks at this time for the Issue --> {}'
                                      .format(self.issue_name_input))
        print()
        # Summary
        print('Summary:')
        bug_ascii_data.append('=== Summary')
        if issue.fields.summary and issue.fields.summary is not None:
            print('Summary:', issue.fields.summary)
            bug_ascii_data.append('* Summary: {}'.format(issue.fields.summary))
        else:
            print('No summary is available now for the Issue --> {}'.format(self.issue_name_input))
            bug_ascii_data.append('* No summary is available now for the Issue --> {}'.format(self.issue_name_input))
        print()
        # Time estimate
        print('Time estimate:')
        bug_ascii_data.append('=== Time Estimate')
        if issue.fields.timeestimate and issue.fields.timeestimate is not None:
            print('Estimate:', issue.fields.timeestimate)
            bug_ascii_data.append('* Estimate: {}'.format(issue.fields.timeestimate))
        else:
            print('No time-estimate is now available fo the Issue --> {}'.format(self.issue_name_input))
            bug_ascii_data.append('* No time-estimate is now available fo the Issue --> {}'.format(self.issue_name_input))
        print()
        # Time original estimate
        print('Time original estimate:')
        bug_ascii_data.append('=== Time Original Estimate')
        if issue.fields.timeoriginalestimate and issue.fields.timeoriginalestimate is not None:
            print('Estimate:', issue.fields.timeoriginalestimate)
            bug_ascii_data.append('* Estimate: {}'.format(issue.fields.timeoriginalestimate))
        else:
            print('No time-original-estimate is now available for the Issue --> {}'
                  .format(self.issue_name_input))
            bug_ascii_data.append('* No time-original-estimate is now available for the Issue --> {}'
                                  .format(self.issue_name_input))
        print()
        # Time spent
        print('Time spent:')
        bug_ascii_data.append('=== Time Spent')
        if issue.fields.timespent and issue.fields.timespent is not None:
            print('Time:', issue.fields.timespent)
            bug_ascii_data.append('* Time: {}'.format(issue.fields.timespent))
        else:
            print('No time-spent is now available for the Issue --> {}'.format(self.issue_name_input))
            bug_ascii_data.append('* No time-spent is now available for the Issue --> {}'.format(self.issue_name_input))
        print()
        # Updated Date
        print('Updated Date:')
        bug_ascii_data.append('=== Updated Date')
        if issue.fields.updated and issue.fields.updated is not None:
            print('Date:', issue.fields.updated)
            bug_ascii_data.append('* Date: {}'.format(issue.fields.updated))
        else:
            print('No updated-date is now available for the the Issue -->'.format(self.issue_name_input))
            bug_ascii_data.append('* No updated-date is now available for the the Issue --> {}'
                                  .format(self.issue_name_input))
        print()
        # Versions list
        print('Versions:')
        bug_ascii_data.append('=== Versions')
        if issue.fields.versions:
            versions_list = issue.fields.versions
            if len(versions_list) > 0:
                counter_versions_list = 1
                for item in versions_list:
                    print('\tVersion {}'.format(counter_versions_list))
                    bug_ascii_data.append('* Version {}'.format(counter_versions_list))
                    print('\t\tID:', item.id)
                    bug_ascii_data.append('** ID: {}'.format(item.id))
                    print('\t\tName:', item.name)
                    bug_ascii_data.append('** Name: {}'.format(item.name))
                    print('\t\tDescription:', item.description)
                    bug_ascii_data.append('** Description: {}'.format(item.description))
                    print('\t\tArchived:', item.archived)
                    bug_ascii_data.append('** Archived: {}'.format(item.archived))
                    print('\t\tReleased:', item.released)
                    bug_ascii_data.append('** Released: {}'.format(item.released))
                    print('\t\tRelease Date', item.releaseDate)
                    bug_ascii_data.append('** Release Date: {}'.format(item.releaseDate))
                    counter_versions_list += 1
            else:
                print('\tThe are no listed versions for the Issue --> {}'.format(self.issue_name_input))
                bug_ascii_data.append('* The are no listed versions for the Issue --> {}'.format(self.issue_name_input))
        print()
        # Votes
        print('Votes:')
        bug_ascii_data.append('=== Votes')
        if issue.fields.votes:
            print('\tVotes No.:', issue.fields.votes.votes)
            bug_ascii_data.append('* Votes No.: {}'.format(issue.fields.votes.votes))
            print('\thas Voted:', issue.fields.votes.hasVoted)
            bug_ascii_data.append('* has Voted: {}'.format(issue.fields.votes.hasVoted))
        else:
            bug_ascii_data.append('* Votes are not available at this time.')
        print()
        # Watchers object
        print('Watchers:')
        bug_ascii_data.append('=== Watchers')
        if issue.fields.watches.watchCount and issue.fields.watches.watchCount is not None:
            print('\tWatches:', issue.fields.watches.watchCount)
            bug_ascii_data.append('* Watches: {}'.format(issue.fields.watches.watchCount))
            print('\tWatching:', issue.fields.watches.isWatching)
            bug_ascii_data.append('* Watching: {}'.format(issue.fields.watches.isWatching))
        else:
            print('\tNo watches are available until now for the Issue: --> {}'.format(self.issue_name_input))
            bug_ascii_data.append('No watches are available until now for the Issue: --> {}'
                                  .format(self.issue_name_input))
        print()
        # Work Ratio
        print('Work Ratio:')
        bug_ascii_data.append('=== Work Ratio')
        if issue.fields.workratio:
            print('Work Ratio:', issue.fields.workratio)
            bug_ascii_data.append('* Ratio: {}'.format(issue.fields.workratio))
        else:
            bug_ascii_data.append('* No Work Ratio available.')
        print()
        print('Issue Work-logs:')
        bug_ascii_data.append('=== Issue Work-logs')
        if issue.fields.worklog:
            print('\tStart at:', issue.fields.worklog.startAt)
            bug_ascii_data.append('* Start at: {}'.format(issue.fields.worklog.startAt))
            print('\tMax Results:', issue.fields.worklog.maxResults)
            bug_ascii_data.append('* Max Results: {}'.format(issue.fields.worklog.maxResults))
            print('\tTotal:', issue.fields.worklog.total)
            bug_ascii_data.append('* Total: {}'.format(issue.fields.worklog.total))
            work_logs_list = issue.fields.worklog.worklogs
            bug_ascii_data.append('* Work-logs List:')
            if len(work_logs_list) > 0:
                counter_work_logs = 1
                for item in work_logs_list:
                    print('\tWork-logs Item {}:'.format(counter_work_logs), work_logs_list[item])
                    bug_ascii_data.append('** Work-logs Item {}:'.format(counter_work_logs) + ' {}'.
                                          format(work_logs_list[item]))
                    counter_work_logs += 1
            else:
                print('\tThere are no listed work-logs at this time for the Issue --> {}'.format(self.issue_name_input))
                bug_ascii_data.append('** There are no listed work-logs at this time for the Issue --> {}'
                                      .format(self.issue_name_input))
        print()
        print('------------------------------------')
        print()
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
            customfields_json = 'customfields_list.json'
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

        # Target Release (Custom Field)
        with open('customfields_list.json') as json_file:
            data = json.load(json_file)
        custom_search = 'customfield_' + str(field_id)
        custom_fields_list_read = data['custom_fields']
        for item in custom_fields_list_read:
            if item == custom_search:
                print(self.custom_field_name + ' custom field found!')
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
    jira_basic_data.data_retriever()

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

    doc_basic = Generator(user=username, bug=bug_id, firstname=first_name, lastname=last_name, email_account=email,
                          data=jira_basic_data.data_retriever())
    doc_basic.generating_doc_jira()

