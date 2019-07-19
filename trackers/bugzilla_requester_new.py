import requests
from pprint import pprint

class BugFields:
    def __init__(self, url):
        self.url = url

    def get_bug_fields(self):
        r = requests.get(self.url)
        data = r.json()
        # pprint(data)
        if 'bugs' in data.keys():
            print('Bug Fields:')
            keys = data.get('bugs')[0].keys()
            for key in keys:
                print(key)


def data_retriever(url):
    r = requests.get(url)
    data = r.json()
    # pprint(data)
    # print()
    # print(data.keys())

    search_list = ['summary', 'platform', 'component']

    for bug in data['bugs']:
        bug_keys_list = bug.keys()
        print(bug_keys_list)
        print(len(bug_keys_list))
        # print(bug.get('cf_release_notes', 'Nothing found'))
        # print(bug.get('summary', 'Nothing found'))
        print()
        print('Printing Keys:')
        print()
        counter_bug_keys = 0
        for key in search_list:
            if key in bug_keys_list:
            # for key in bug_keys_list:
                if type(bug.get(key)) is str or type(bug.get(key)) is bool or type(bug.get(key)) is int or type(bug.get(key)) is None:
                    if bug.get(key) is '':
                        print(key + ': ' + 'Nothing related to {} is now available.'.format(key))
                    else:
                        print(key + ': ' + str(bug.get(key, 'Nothing related to {} is now available.'.format(key))))
                    print(type(bug.get(key)))
                    print()
                if type(bug.get(key)) is list:
                    print(key + ':')
                    counter__dictionary_items = 1
                    for list_item in bug.get(key):
                        if type(list_item) is dict:
                            print('\tItem: {}'.format(counter__dictionary_items))
                            dictionary_keys = list_item.keys()
                            for dictionary_key in dictionary_keys:
                                # print(dictionary_keys)
                                print('\t\t' + dictionary_key + ':' + str(list_item.get(dictionary_key)))
                            print()
                            counter__dictionary_items += 1
                        else:
                            print('\t', list_item)
                            print()
                    print()
                # counter_bug_keys += 1
        print()
        print('Countered keys:', counter_bug_keys)


if __name__ == '__main__':
    link = 'https://bugzilla.redhat.com/rest/bug/1376835'
    # data_retriever(link)

    bug_fields = BugFields(link)
    bug_fields.get_bug_fields()