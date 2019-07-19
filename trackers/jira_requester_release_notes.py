import requests
import configparser
import os
from requests_oauthlib import OAuth1

from conf.confparse import JiraReadConfigurationBasicAuth
from conf.confparse import JiraReadConfigurationOAuth


current_d = os.getcwd()
# print(current_d)
directories_list = current_d.split('/')
# print(directories_list)
# print(directories_list[1:4])
basic_desktop_path = directories_list[1:4]
new_path = 'conf/'
basic_desktop_path.append(new_path)
conf_path = '/' + '/'.join(basic_desktop_path)


class TargetRelease:
    def __init__(self, release_name, release, order):
        self.release_name = release_name
        self.release = release
        self.order = order

    def get_release_notes(self):
        # AsciiDoc data collection list
        ascii_data_list = []

        # AUTHENTICATION
        options = {}
        # Authentication objects
        jira_basic_auth = JiraReadConfigurationBasicAuth()
        jira_oauth = JiraReadConfigurationOAuth()
        # code for key cert here
        key_cert_data = None
        # with open(key_cert, 'r') as key_cert_file:
        #     key_cert_data = key_cert_file.read()
        key_cert_data = 'To be added'

        basic_auth = jira_basic_auth.read_user_basic_auth()['basic_auth']
        oauth = jira_oauth.read_oauth()['oauth']

        if basic_auth is True or oauth is True:
            if basic_auth is True:
                basic_auth_reason_value = jira_basic_auth.read_user_basic_auth()['basic_auth_reason']
                username_value = jira_basic_auth.read_user_basic_auth()['username']
                username_reason_value = jira_basic_auth.read_user_basic_auth()['username_reason']
                password_value = jira_basic_auth.read_user_basic_auth()['password']
                password_reason_value = jira_basic_auth.read_user_basic_auth()['password_reason']
                options['authentication'] = (username_value, password_value)
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
                    # OAuth1('YOUR_APP_KEY', 'YOUR_APP_SECRET', 'USER_OAUTH_TOKEN', 'USER_OAUTH_TOKEN_SECRET')
                    options['authentication'] = OAuth1(access_token_value,
                                                       access_token_secret_value,
                                                       consumer_key_value,
                                                       key_cert_data)
                else:
                    raise Exception('Please add the key certification data.')
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

        # Start making the AsciiDoc from the release notes
        ascii_data_list.append('== Issues')
        ascii_data_list.append('\n')
        for release_item in self.release:
            print('Release Note:', release_item)
            ascii_data_list.append('== Release Note: {}'.format(release_item))
            release_name_url = '{}'.format(self.release_name)
            release_url = '{}'.format(release_item)
            ascending_order = ' ORDER BY priority ASC'
            descending_order = ' ORDER BY priority DESC'
            order_definition = ''
            if self.order is 'a':
                order_definition = ascending_order
            elif self.order is 'd':
                order_definition = descending_order
            elif self.order is None:
                order_definition = ''
            url = 'https://issues.jboss.org/rest/api/latest/search?jql="{}"="{}"{}'.format(release_name_url,
                                                                                           release_url,
                                                                                           order_definition)
            # data retrieving from the REST API
            r = requests.get(url, auth=options['authentication'])
            data = r.json()

            keys_list = data.keys()
            # print(keys_list)
            for key in keys_list:
                if key == 'errorMessages':
                    print('This Field does not exist or you do not have permission to view it.')
                    print()
                    ascii_data_list.append('* This Field does not exist or you do not have permission to view it.')
                    # raise Exception('This Field does not exist or you do not have permission to view it.')
                elif key == 'issues':
                    print('Total Jiras found based on that release:', data.get('total'))
                    ascii_data_list.append('* Total Jiras: {}'.format(data.get('total')))
                    print()
                    jiras = data['issues']
                    for issue in jiras:
                        print('Collecting Key:', issue.get('key'))
                        # print('taking selected fields..')
                        ascii_data_list.append('==== {}'.format(issue.get('key')))
                        issue_fields = issue.get('fields')
                        ascii_data_list.append('* Summary: {}'.format(issue_fields.get('summary'),
                                                                      'No summary is provided here.'))
                        ascii_data_list.append('* Description:')
                        ascii_data_list.append('============================')
                        ascii_data_list.append('{}'.format(issue_fields.get('description',
                                                                            'No description is provided here.')))
                        ascii_data_list.append('============================')
                        # print()
            print()
            print('----------------------------')
            print()

        return ascii_data_list
