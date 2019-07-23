from datetime import datetime


"""CLASS FOR GENERATING RELEASE NOTES INFORMATION"""


class GeneratorJiraReleaseNotes:
    def __init__(self, user, release_name, release, firstname, lastname, email_account, data_basic, path):
        self.user = user
        self.release_name = release_name
        self.release = release
        self.firstname = firstname
        self.lastname = lastname
        self.email_account = email_account
        self.data_basic = data_basic
        self.path = path

    def generating_doc_jira(self):
        now = datetime.now()
        now_str = now.strftime("%Y-%m-%d_%H-%M-%S")
        if self.user is None:
            self.user = 'unknown_username'
        if self.email_account is '':
            self.email_account = 'Email is not defined at the configuration file'
        if self.firstname is '':
            self.firstname = 'Unknown Firstname - '
        if self.lastname is '':
            self.lastname = ' - Unknown Lastname'
        if self.path is None:
            f = open('release-notes-docs/jira_bug_info_{}_{}_{}.adoc'.format(self.release_name, self.user, now_str),
                     'w+')
            f_txt = open('release-notes-docs/jira_bug_info_{}_{}_{}.txt'.format(self.release_name, self.user, now_str),
                         'w+')
        else:
            f = open('{}/jira_bug_info_{}_{}_{}.adoc'.format(self.path, self.release_name, self.user, now_str), 'w+')
            f_txt = open('{}/jira_bug_info_{}_{}_{}.txt'.format(self.path, self.release_name, self.user, now_str), 'w+')
        print('Writing file..')
        f.write('= Release Notes Generation Tool (RLGEN)')
        f_txt.write('= Release Notes Generation Tool (RLGEN)')
        f.write('\n')
        f_txt.write('\n')
        f.write(':author: {} {}'.format(self.firstname, self.lastname))
        f_txt.write(':author: {} {}'.format(self.firstname, self.lastname))
        f.write('\n')
        f_txt.write('\n')
        f.write(':email: {}'.format(self.email_account))
        f_txt.write(':email: {}'.format(self.email_account))
        f.write('\n')
        f_txt.write('\n')
        f.write('\n')
        f_txt.write('\n')
        if self.data_basic:
            for item in self.data_basic:
                f.write(item)
                f_txt.write(item)
                f.write('\n')
                f_txt.write('\n')
                f.write('\n')
                f_txt.write('\n')
        f.write('\n')
        f_txt.write('\n')
        f.write('\n')
        f_txt.write('\n')
        f.write('----------\n')
        f_txt.write('----------\n')
        f.write('Report time: ' + str(datetime.now()))
        f_txt.write('Report time: ' + str(datetime.now()))
        f.write('\n')
        f_txt.write('\n')
        f.write('\n')
        f_txt.write('\n')
        f.write('\n')
        f_txt.write('\n')
        f.close()
        f_txt.close()
        print('File AsciiDoc is written successfully!')


class GeneratorJira:
    def __init__(self, user, bug, firstname, lastname, email_account, data_basic, data_custom, path):
        self.user = user
        self.bug = bug
        self.firstname = firstname
        self.lastname = lastname
        self.email_account = email_account
        self.data_basic = data_basic
        self.data_custom = data_custom
        self.path = path

    def generating_doc_jira(self):
        now = datetime.now()
        now_str = now.strftime("%Y-%m-%d_%H-%M-%S")
        if self.user is None:
            self.user = 'unknown_username'
        if self.email_account is '':
            self.email_account = 'Email is not defined at the configuration file'
        if self.firstname is '':
            self.firstname = 'Unknown Firstname - '
        if self.lastname is '':
            self.lastname = ' - Unknown Lastname'
        if self.path is None:
            f = open('release-notes-docs/jira_bug_info_{}_{}_{}.adoc'.format(self.bug, self.user, now_str), 'w+')
        else:
            f = open('{}/jira_bug_info_{}_{}_{}.adoc'.format(self.path, self.bug, self.user, now_str), 'w+')
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


""" BUGZILLA REPORT GENERATION CLASS """


class GeneratorBugzillaReport:
    def __init__(self, kind_of_report, releases, bug, user, username, firstname, lastname, email_account, data_basic, path):
        self.kind_of_report = kind_of_report
        self.releases = releases
        self.bug = bug
        self.user = user
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        self.email_account = email_account
        self.data_basic = data_basic
        self.path = path

    def generating_doc_bugzilla(self):
        now = datetime.now()
        now_str = now.strftime("%Y-%m-%d_%H-%M-%S")
        report_fields = []
        if self.username is '':
            self.username = 'unknown_username'
        if self.email_account is '':
            self.email_account = 'Email is not defined at the configuration file'
        if self.firstname is '':
            self.firstname = 'Unknown Firstname - '
        if self.lastname is '':
            self.lastname = ' - Unknown Lastname'
        # kind of report
        report_fields.append(self.kind_of_report)
        print(report_fields)
        # releases input
        if self.releases is not None:
            for release in self.releases:
                report_fields.append(release)
        # bug/issue input
        if self.bug is not None:
            report_fields.append(self.bug)
        # user input
        if self.user is not None:
            report_fields.append(self.user)
        report_fields_string = '_'.join(report_fields)
        if self.path is None:
            f = open('release-notes-docs/Bugzilla/bugzilla_{}_{}.adoc'
                     .format(report_fields_string, now_str), 'w+')
        else:
            f = open('{}/bugzilla_{}_{}.adoc'
                     .format(self.path, report_fields_string, now_str), 'w+')
        print('Writing file..')
        f.write('= Release Notes Generation Tool (RLGEN)')
        f.write('\n')
        f.write(':author: {} {}'.format(self.firstname, self.lastname))
        f.write('\n')
        f.write(':email: {}'.format(self.email_account))
        f.write('\n')
        f.write(':username: {}'.format(self.username))
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
