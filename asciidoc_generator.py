from datetime import datetime


class Generator:
    def __init__(self, user, bug, firstname, lastname, email_account, data_basic, data_custom):
        self.user = user
        self.bug = bug
        self.firstname = firstname
        self.lastname = lastname
        self.email_account = email_account
        self.data_basic = data_basic
        self.data_custom = data_custom

    def generating_doc_jira(self):
        f = open('{}_{}.adoc'.format(self.bug, self.user), 'w+')
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
