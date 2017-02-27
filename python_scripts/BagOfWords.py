import re
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords


class BagOfWords():
    def __init__(self):
        # Initialize the "CountVectorizer" object, which is scikit-learn's
        # bag of words toolsentiment.
        self.vectorizer = CountVectorizer(analyzer="word", \
                                     tokenizer=None, \
                                     preprocessor=None, \
                                     stop_words=None, \
                                     max_features=5000)

    def sentence_to_wordlist(self, sentence, remove_stopwords=False):
        # Function to convert a document to a sequence of words,
        # optionally removing stop words.  Returns a list of words.
        #
        # 1. Remove non-letters
        sentence = re.sub("[^a-zA-Z]", " ", sentence)
        #
        # 2. Convert words to lower case and split them
        words = sentence.lower().split()
        #
        # 3. Optionally remove stop words (false by default)
        if remove_stopwords:
            stops = set(stopwords.words("english"))
            words = [w for w in words if not w in stops]
        #
        # 4. Return a list of words
        return words



    def clean_sentences(self, sentences):
        # Initialize an empty list to hold the clean_sentences
        clean = []

        for i in xrange(0, len(sentences)):
            clean.append(" ".join(self.sentence_to_wordlist(sentences[i], True)))

        return clean

    def fit_transform(self, sentences):

        sentences = self.clean_sentences(sentences)
        return self.vectorizer.fit_transform(sentences).toarray()

    def transform(self, sentences):

        sentences = self.clean_sentences(sentences)
        return self.vectorizer.transform(sentences).toarray()