import os
import configparser

current_d = os.getcwd()
# print(current_d)
directories_list = current_d.split('/')
# print(directories_list)
# print(directories_list[1:4])
basic_desktop_path = directories_list[1:4]
new_path = 'conf/'
basic_desktop_path.append(new_path)
conf_path = '/' + '/'.join(basic_desktop_path)

config = configparser.ConfigParser()
config.read('{}config.conf'.format(conf_path))

# read fields from configuration
search_list_conf_input = config['target_release']['search_list']
print(search_list_conf_input)
search_list_conf_input = search_list_conf_input.replace(', ', ',')
search_list_conf_input = search_list_conf_input.replace(' ,', ',')
search_list_conf_input = search_list_conf_input.replace(' , ', ',')
search_list_conf_input = search_list_conf_input.split(',')
print(search_list_conf_input)