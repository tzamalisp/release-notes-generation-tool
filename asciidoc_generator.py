from datetime import datetime


class GeneratorJira:
    def __init__(self, user, bug, firstname, lastname, email_account, data_basic, data_custom):
        self.user = user
        self.bug = bug
        self.firstname = firstname
        self.lastname = lastname
        self.email_account = email_account
        self.data_basic = data_basic
        self.data_custom = data_custom

    def generating_doc_jira(self):
        f = open('release-notes-docs/jira_{}_{}.adoc'.format(self.bug, self.user), 'w+')
        print('Writing file..')
        f.write('= Release Notes Generation Tool (RLGEN)')
        f.write('\n')
        f.write(':author: {} {}'.format(self.firstname, self.lastname))
        f.write('\n')
        f.write(':email: {}'.format(self.email_account))
        f.write('\n')
        f.write('\n')
        if self.data_basic:
            for item in self.data_basic:
                f.write(item)
                f.write('\n')
                f.write('\n')
        f.write('\n')
        f.write('\n')
        if self.data_custom:
            for item in self.data_custom:
                f.write(item)
                f.write('\n')
                f.write('\n')
        f.write('\n')
        f.write('\n')
        f.write('----------\n')
        f.write('Report time: ' + str(datetime.now()))
        f.write('\n')
        f.write('\n')
        f.write('\n')
        f.close()
        print('File AsciiDoc is written successfully!')


class GeneratorBugzillaBug:
    def __init__(self, user, bug, firstname, lastname, email_account, data_basic):
        self.user = user
        self.bug = bug
        self.firstname = firstname
        self.lastname = lastname
        self.email_account = email_account
        self.data_basic = data_basic

    def generating_doc_bugzilla(self):
        f = open('release-notes-docs/bugzilla_{}_{}.adoc'.format(self.bug, self.user), 'w+')
        print('Writing file..')
        f.write('= Release Notes Generation Tool (RLGEN)')
        f.write('\n')
        f.write(':author: {} {}'.format(self.firstname, self.lastname))
        f.write('\n')
        f.write(':email: {}'.format(self.email_account))
        f.write('\n')
        f.write('\n')
        if self.data_basic:
            for item in self.data_basic:
                f.write(item)
                f.write('\n')
                f.write('\n')
        f.write('\n')
        f.write('\n')
        f.write('----------\n')
        f.write('Report time: ' + str(datetime.now()))
        f.write('\n')
        f.write('\n')
        f.write('\n')
        f.close()
        print('File AsciiDoc is written successfully!')


class GenratorBugzillaBugComments:
    def __init__(self, user, bug, firstname, lastname, email_account, data_comments):
        self.user = user
        self.bug = bug
        self.firstname = firstname
        self.lastname = lastname
        self.email_account = email_account
        self.data_comments = data_comments

    def generating_doc_bug_comments(self):
        f = open('release-notes-docs/bugzilla_{}_{}_comments.adoc'.format(self.bug, self.user), 'w+')
        print('Writing file..')
        f.write('= Release Notes Generation Tool (RLGEN)')
        f.write('\n')
        f.write(':author: {} {}'.format(self.firstname, self.lastname))
        f.write('\n')
        f.write(':email: {}'.format(self.email_account))
        f.write('\n')
        f.write('\n')
        if self.data_comments:
            for item in self.data_comments:
                f.write(item)
                f.write('\n')
                f.write('\n')
        f.write('\n')
        f.write('\n')
        f.write('----------\n')
        f.write('Report time: ' + str(datetime.now()))
        f.write('\n')
        f.write('\n')
        f.write('\n')
        f.close()
        print('File AsciiDoc is written successfully!')


class GeneratorBugzillaBugHistory:
    def __init__(self, user, bug, firstname, lastname, email_account, data_bug_history):
        self.user = user
        self.bug = bug
        self.firstname = firstname
        self.lastname = lastname
        self.email_account = email_account
        self.data_bug_history = data_bug_history

    def generating_doc_bug_history(self):
        f = open('release-notes-docs/bugzilla_{}_{}_bug_history.adoc'.format(self.bug, self.user), 'w+')
        print('Writing file..')
        f.write('= Release Notes Generation Tool (RLGEN)')
        f.write('\n')
        f.write(':author: {} {}'.format(self.firstname, self.lastname))
        f.write('\n')
        f.write(':email: {}'.format(self.email_account))
        f.write('\n')
        f.write('\n')
        if self.data_bug_history:
            for item in self.data_bug_history:
                f.write(item)
                f.write('\n')
                f.write('\n')
        f.write('\n')
        f.write('\n')
        f.write('----------\n')
        f.write('Report time: ' + str(datetime.now()))
        f.write('\n')
        f.write('\n')
        f.write('\n')
        f.close()
        print('File AsciiDoc is written successfully!')


class GeneratorBugzillaUserBugs:
    def __init__(self, user, firstname, lastname, email_account, data_bugs_user):
        self.user = user
        self.firstname = firstname
        self.lastname = lastname
        self.email_account = email_account
        self.data_bugs_user = data_bugs_user

    def generating_doc_user_bugs(self):
        f = open('release-notes-docs/bugzilla_{}_user_bugs.adoc'.format(self.user), 'w+')
        print('Writing file..')
        f.write('= Release Notes Generation Tool (RLGEN)')
        f.write('\n')
        f.write(':author: {} {}'.format(self.firstname, self.lastname))
        f.write('\n')
        f.write(':email: {}'.format(self.email_account))
        f.write('\n')
        f.write('\n')
        if self.data_bugs_user:
            for item in self.data_bugs_user:
                f.write(item)
                f.write('\n')
                f.write('\n')
        f.write('\n')
        f.write('\n')
        f.write('----------\n')
        f.write('Report time: ' + str(datetime.now()))
        f.write('\n')
        f.write('\n')
        f.write('\n')
        f.close()
        print('File AsciiDoc is written successfully!')


class GeneratorBuzillaUserInfo:
    def __init__(self, user, firstname, lastname, email_account, data_user):
        self.user = user
        self.firstname = firstname
        self.lastname = lastname
        self.email_account = email_account
        self.data_user = data_user

    def generating_doc_user_info(self):
        f = open('release-notes-docs/bugzilla_{}_user_info.adoc'.format(self.user), 'w+')
        print('Writing file..')
        f.write('= Release Notes Generation Tool (RLGEN)')
        f.write('\n')
        f.write(':author: {} {}'.format(self.firstname, self.lastname))
        f.write('\n')
        f.write(':email: {}'.format(self.email_account))
        f.write('\n')
        f.write('\n')
        if self.data_user:
            for item in self.data_user:
                f.write(item)
                f.write('\n')
                f.write('\n')
        f.write('\n')
        f.write('\n')
        f.write('----------\n')
        f.write('Report time: ' + str(datetime.now()))
        f.write('\n')
        f.write('\n')
        f.write('\n')
        f.close()
        print('File AsciiDoc is written successfully!')
