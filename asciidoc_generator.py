from datetime import datetime
import logging

from logger_creation import LoggerSetup

logging__asciidoc = LoggerSetup(name='asciidoc_logger', log_file='log/asciidoc_generator.log', level=None)
logger_asciidoc = logging__asciidoc.setup_logger()

logger_asciidoc.debug('Entering AsciiDoc Generator Classes')


class GeneratorJira:
    def __init__(self, kind_of_report, releases, bug, user, firstname, lastname, email_account, data_basic, path):
        self.kind_of_report = kind_of_report
        self.releases = releases
        self.user = user
        self.bug = bug
        self.firstname = firstname
        self.lastname = lastname
        self.email_account = email_account
        self.data_basic = data_basic
        self.path = path

    def generating_doc_jira(self):
        now = datetime.now()
        now_str = now.strftime("%Y-%m-%d_%H-%M-%S")
        report_fields = []
        if self.user is None:
            self.user = 'unknown_username'
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
            f = open('release-notes-docs/JIRA/jira_{}_{}.adoc'
                     .format(report_fields_string, now_str), 'w+')
        else:
            f = open('{}/jira_{}_{}.adoc'
                     .format(self.path, report_fields_string, now_str), 'w+')
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
