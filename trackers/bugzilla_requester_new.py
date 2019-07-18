import requests
from pprint import pprint


def data_retriever(url):
    r = requests.get(url)
    data = r.json()
    # pprint(data)
    # print()
    # print(data.keys())

    for bug in data['bugs']:
        bug_keys_list = bug.keys()
        print(bug_keys_list)
        for key in bug_keys_list:
            if key.startswith('cc'):
                print('Header 1:', key)
                # print(key)
                # print(bug.get(key))
                nested = bug.get(key)
                if type(nested) is list:
                    for item in nested:
                        if type(item) is dict:
                            item_keys_list = item.keys()
                            for item_key in item_keys_list:
                                print('\t', item_key + ':', item.get(item_key))
                            print()
                        else:
                            print('\t', item)
                    print()
                    print()



if __name__ == '__main__':
    link = 'https://bugzilla.redhat.com/rest/bug/1376835'
    data_retriever(link)