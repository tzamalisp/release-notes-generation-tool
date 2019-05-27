from jira import JIRA


"""FUNCTION FOR RETRIEVING ISSUE INFORMATION FROM JIRA API"""


def requester():
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
    print()

    # creating an issue object to fetch information later on from JIRA API
    print('Creating the issue object..')
    issue = jira.issue('JBCS-535')
    print()

    # splitting the string to separate the JIRA-Project Key and the Issue ID
    print('Splitting the issue string:')
    issue_fields = 'JBCS-535'.split('-')
    print(issue_fields)
    print()
    print()
    print()

    # Retrieving selected fields of a JIRA issue and printing them
    print('PRINT SELETECTED FIELDS')
    print()

    # Project key
    print('Project Key', issue.fields.project.key)  # 'JRA'

    # Issue type
    print('Issue Type:', issue.fields.issuetype.name)  # 'New Feature'

    # Reporter display name
    print('Reporter Display name', issue.fields.reporter.displayName)  # 'Mike Cannon-Brookes [Atlassian]'

    # Created datetime
    print('Created-datetime:', issue.fields.created)

    # Assignee
    print('Assignee:', issue.fields.assignee)

    # Issue description
    print('Issue Description', issue.fields.description)

    # Status
    print('Status:', issue.fields.status)

    # Aggregate progress
    print('Aggregate progress:', issue.fields.aggregateprogress)

    # Aggregate time estimate
    print('Aggregate time estimate:', issue.fields.aggregatetimeestimate)

    # Aggregate time original estimate
    print('Aggregate time original estimate:', issue.fields.aggregatetimeoriginalestimate)

    # Aggregate time spent
    print('Aggregate time spent:', issue.fields.aggregatetimespent)

    # Attachments list
    print('Attachments list:', issue.fields.attachment)

    # Comment object
    print('Comments object:', issue.fields.comment)

    # Components Name
    print('Components --> Name:', issue.fields.components[0])

    # Environment
    print('Environment:', issue.fields.environment)

    # Fix versions
    print('Fix Versions list:', issue.fields.fixVersions)

    # Issue links
    print('Issue links list:', issue.fields.issuelinks)

    # Issue Type object
    print('Issue type:', issue.fields.issuetype)

    # Labels
    print('Labels list:', issue.fields.labels)

    # Mro
    print('Mro:', issue.fields.mro)

    # Progress object
    print('Progress object:', issue.fields.progress)

    # Project name
    print('Project name:', issue.fields.project)

    # Reporter
    print('Reporter:', issue.fields.reporter)

    # Resolution
    print('Resolution:', issue.fields.resolution)

    # Resolution date
    print('Resolution date:', issue.fields.resolutiondate)

    # Current status
    print('Status:', issue.fields.status)

    # Sub-tasks
    print('Sub-tasks:', issue.fields.subtasks)

    # Summary
    print('Summary:', issue.fields.summary)

    # Time estimate
    print('Time estimate:', issue.fields.timeestimate)

    # Time original estimate
    print('Time original estimate:', issue.fields.timeoriginalestimate)

    # Time spent
    print('Time spent:', issue.fields.timespent)

    # Updated Date
    print('Updated date:', issue.fields.updated)

    # Versions array
    print('Versions:', issue.fields.versions)

    # Votes
    print('Votes:', issue.fields.votes)

    # Watchers object
    print('Watchers object:', issue.fields.watches)

    # Work Ratio
    print('Work Ratio:', issue.fields.workratio)

    # Target Release (Custom Field)
    print('ISSUE CUSTOM FIELDS ---> TARGET RELEASE')
    if issue.fields.customfield_12311240 is not None:
        print('Target Release:', issue.fields.customfield_12311240)
    else:
        print('> There is no Target Release for that Issue!')

    print()
    print()
    print()

    # print()
    # print('JIRA PROJECTS')
    # print(jira.projects())

    print('Issue Work-logs:')
    print(issue.fields.worklog.worklogs)

    print()
    print()
    print()

    print('PROJECT:')
    print('Creating project object..')
    jra = jira.project(issue_fields[0])
    print('Project name', jra.name)                         # 'JBCS'
    print('Project display name', jra.lead.displayName)             # 'John Doe [ACME Inc.]'

    print()
    print()
    print()

    print('PROJECT COMPONENTS')
    components = jira.project_components(jra)
    for component in components:
        print(component)

    print()
    print()
    print()

    print('PROJECT VERSIONS:')
    versions = jira.project_versions(jra)
    for version in versions:
        print(version)


if __name__ == '__main__':
    requester()
