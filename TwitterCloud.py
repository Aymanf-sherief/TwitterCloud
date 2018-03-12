from helpers import Timeline
from helpers.wordcloud_utils import count_occurences, generate_cloud, clean_text
import os
import json  # for config


# change this if you want to change configuration file location
conf_path = './cloud_conf.json'

if os.path.exists(conf_path):  # check if there's a config file
    conf_file = open(conf_path, 'r')
    auth_data = json.load(conf_file)
    conf_file.close()
else:  # if not, write a dummy file and ask user to properly fill it
    consumer = {'key': 'xxxxxxxxxxxxxxxxxx',
                'secret': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxx'}
    access = {'key': 'xxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxxxxx',
              'secret': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'}
    print("No config file found, creating dummy config file")
    print("Please change keys in cloud_conf.json to your own keys")
    conf_file = open(conf_path, 'w')
    json.dump({'consumer': consumer, 'access': access}, conf_file, indent=4)
    conf_file.close()

    exit()


# normal flow
screen_name = input('Enter Screen name (handle without "@"): ')
# use Timeline class to initialize api connection
tl = Timeline.Timeline(auth_data)
print("collecting tweets...")
tweets = tl.load_tweets(screen_name)  # get tweets as pandas dataframe
counts = {}  # will hold word counts {word: #of occurence}
print("counting your words...")
tweets.text.apply(clean_text).apply(count_occurences, args=(
    counts, ))  # cleaning text then counting words
print('counted {} different words'.format(len(counts)))
print("drawing...")
generate_cloud(screen_name, counts)  # creating wordcloud
