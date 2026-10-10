import re
import string

import nltk

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


try:

    stopwords.words("english")

except:

    nltk.download("stopwords")
    nltk.download("wordnet")
    nltk.download("omw-1.4")


lemmatizer = WordNetLemmatizer()

stop_words = set(stopwords.words("english"))


def clean_text(text):

    text = text.lower()

    text = re.sub(r"http\S+", "", text)

    text = re.sub(r"\d+", "", text)

    text = text.translate(
        str.maketrans(
            "",
            "",
            string.punctuation
        )
    )

    words = text.split()

    words = [

        lemmatizer.lemmatize(word)

        for word in words

        if word not in stop_words

    ]

    return " ".join(words)