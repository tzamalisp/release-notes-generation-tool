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


"""GENERATING BUGZILLA BUG INFORMATION DOC"""


class GeneratorBugzillaReleaseNotes:
    def __init__(self, user, release, firstname, lastname, email_account, data_basic, path):
        self.user = user
        self.release = release
        self.firstname = firstname
        self.lastname = lastname
        self.email_account = email_account
        self.data_basic = data_basic
        self.path = path

    def generating_doc_bugzilla(self):
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
            f = open('release-notes-docs/bugzilla_Target_Release_{}_{}_{}.adoc'
                     .format(self.release, self.user, now_str), 'w+')
        else:
            f = open('{}/bugzilla_Target_Release_{}_{}_{}.adoc'
                     .format(self.path, self.release, self.user, now_str), 'w+')
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

class GeneratorBugzillaBug:
    def __init__(self, user, bug, firstname, lastname, email_account, data_basic, path):
        self.user = user
        self.bug = bug
        self.firstname = firstname
        self.lastname = lastname
        self.email_account = email_account
        self.data_basic = data_basic
        self.path = path

    def generating_doc_bugzilla(self):
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
            f = open('release-notes-docs/bugzilla_bug_info_{}_{}_{}.adoc'.format(self.bug, self.user, now_str), 'w+')
        else:
            f = open('{}/bugzilla_bug_info_{}_{}_{}.adoc'.format(self.path, self.bug, self.user, now_str), 'w+')
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


"""GENERATING BUGZILLA BUG COMMENTS DOC"""


class GeneratorBugzillaBugComments:
    def __init__(self, user, bug, firstname, lastname, email_account, data_comments, path):
        self.user = user
        self.bug = bug
        self.firstname = firstname
        self.lastname = lastname
        self.email_account = email_account
        self.data_comments = data_comments
        self.path = path

    def generating_doc_bug_comments(self):
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
            f = open('release-notes-docs/bugzilla_bug_comments__{}_{}_{}.adoc'
                     .format(self.bug, self.user, now_str), 'w+')
        else:
            f = open('{}/bugzilla_bug_comments__{}_{}_{}.adoc'
                     .format(self.path, self.bug, self.user, now_str), 'w+')
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


"""GENERATING BUGZILLA BUG HISTORY DOC"""


class GeneratorBugzillaBugHistory:
    def __init__(self, user, bug, firstname, lastname, email_account, data_bug_history, path):
        self.user = user
        self.bug = bug
        self.firstname = firstname
        self.lastname = lastname
        self.email_account = email_account
        self.data_bug_history = data_bug_history
        self.path = path

    def generating_doc_bug_history(self):
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
            f = open('release-notes-docs/bugzilla_bug_history_{}_{}_{}.adoc'.format(self.bug, self.user,now_str), 'w+')
        else:
            f = open('{}/bugzilla_bug_history_{}_{}_{}.adoc'.format(self.path, self.bug, self.user, now_str), 'w+')
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


"""GENERATING BUGZILLA USER BUGS DOC"""


class GeneratorBugzillaUserBugs:
    def __init__(self, user, firstname, lastname, email_account, data_bugs_user, path):
        self.user = user
        self.firstname = firstname
        self.lastname = lastname
        self.email_account = email_account
        self.data_bugs_user = data_bugs_user
        self.path = path

    def generating_doc_user_bugs(self):
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
            f = open('release-notes-docs/bugzilla_user_bugs_{}_{}.adoc'.format(self.user, now_str), 'w+')
        else:
            f = open('{}/bugzilla_user_bugs_{}_{}.adoc'.format(self.path, self.user, now_str), 'w+')
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


"""GENERATING BUGZILLA USER INFO DOC"""


class GeneratorBugzillaUserInfo:
    def __init__(self, user, firstname, lastname, email_account, data_user, path):
        self.user = user
        self.firstname = firstname
        self.lastname = lastname
        self.email_account = email_account
        self.data_user = data_user
        self.path = path

    def generating_doc_user_info(self):
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
            f = open('release-notes-docs/bugzilla_user_info_{}_{}.adoc'.format(self.user, now_str), 'w+')
        else:
            f = open('{}/bugzilla_user_info_{}_{}.adoc'.format(self.path, self.user, now_str), 'w+')
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
