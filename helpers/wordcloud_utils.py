from os import path
from PIL import Image
import numpy as np

import re
from wordcloud import WordCloud
# for arabic, useless if you don't use a proper font that supports arabic (e.g. unifont)
from arabic_reshaper import reshape
from bidi.algorithm import get_display
####
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
# removing meaningless high-frequency words
STOPWORDS = set(stopwords.words('english'))


def clean_text(text):

    regex = r'(https?:\/\/.*[\r\n]*)'  # remove links
    regex += r'|(rt)'  # remove 'rt' from retweeted tweets
    cleaned_text = re.sub(regex, '', text.lower(), flags=re.MULTILINE)
    cleaned_text = get_display(reshape(cleaned_text))  # again, for arabic text
    cleaned_text = ' '.join(
        [word for word in cleaned_text.split() if word not in STOPWORDS])
    return cleaned_text.strip()


def count_occurences(text, counts):
    for word in text.split():  # populate dict with word counts

        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1


def generate_cloud(screen_name, counts):

    d = path.dirname(__file__)  # get current path
    # mask so word cloud takes shape of larry the twitter bird
    larry_mask = np.array(Image.open(
        path.join(d.replace('helpers', 'static'), "mask.png")))

    wc = WordCloud(background_color="white", max_words=2000, mask=larry_mask, width=1280, height=960,  # init
                   stopwords=STOPWORDS)

    wc.generate_from_frequencies(counts)  # finally, phew

    wc.to_file(path.join(path.join(d, path.pardir), "{}_wordcloud.png".format(
        screen_name)))  # and then there's this
