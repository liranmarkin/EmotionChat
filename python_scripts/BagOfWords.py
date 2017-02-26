import re
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords

def sentence_to_wordlist(sentence, remove_stopwords=False):
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



def clean_sentences(sentences):
    # Initialize an empty list to hold the clean_sentences
    clean = []

    for i in xrange(0, len(sentences)):
        clean.append(" ".join(sentence_to_wordlist(sentences[i], True)))

    return clean

def get_features(sentences):

    sentences = clean_sentences(sentences)
    # Initialize the "CountVectorizer" object, which is scikit-learn's
    # bag of words toolsentiment.
    vectorizer = CountVectorizer(analyzer="word", \
                                 tokenizer=None, \
                                 preprocessor=None, \
                                 stop_words=None, \
                                 max_features=5000)

    # fit_transform() does two functions: First, it fits the model
    # and learns the vocabulary; second, it transforms our training data
    # into feature vectors. The input to fit_transform should be a list of
    # strings.
    train_data_features = vectorizer.fit_transform(sentences)

    # Numpy arrays are easy to work with, so convert the result to an
    # array
    train_data_features = train_data_features.toarray()

    return train_data_features
