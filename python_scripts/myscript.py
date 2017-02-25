import os, re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np
from nltk.corpus import stopwords
from SVM import SVM



def read_data():
    return pd.read_csv(os.path.join(os.path.dirname(__file__), 'data', 'real_data.csv'))

def get_sentences(data):
    return data['sentence'].values.tolist()

def get_emotions(data):
    return data['emotion'].values.tolist()




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
    # Initialize an empty list to hold the clean_train
    clean = []

    for i in xrange(0, len(train['content'])):
        clean.append(" ".join(sentence_to_wordlist(sentences[i], True)))

    return clean

def get_features(clean_sentences):

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
    train_data_features = vectorizer.fit_transform(clean_sentences)

    # Numpy arrays are easy to work with, so convert the result to an
    # array
    train_data_features = train_data_features.toarray()

if __name__ == '__main__':
    train = read_data()

    sentences = get_sentences(train)
    emotions = get_emotions(train)

    print sentences
    print emotions

    raw_input()

    # ******* Train a random forest using the bag of words
    #
    print "Training the random forest (this may take a while)..."

    # Initialize a Random Forest classifier with 100 trees
    forest = RandomForestClassifier(n_estimators=100)

    # Fit the forest to the training set, using the bag of words as
    # features and the sentiment labels as the response variable
    #
    # This may take a few minutes to run
    forest = forest.fit(train_data_features, train["sentiment"])

    # Create an empty list and append the clean reviews one by one
    clean_test_reviews = []

    print "Cleaning and parsing the test set movie reviews...\n"
    for i in xrange(0, len(test["review"])):
        clean_test_reviews.append(" ".join(KaggleWord2VecUtility.review_to_wordlist(test["review"][i], True)))

    # Get a bag of words for the test set, and convert to a numpy array
    test_data_features = vectorizer.transform(clean_test_reviews)
    test_data_features = test_data_features.toarray()

    # Use the random forest to make sentiment label predictions
    print "Predicting test labels...\n"
    result = forest.predict(test_data_features)

    # Copy the results to a pandas dataframe with an "id" column and# Initialize the "CountVectorizer" object, which is scikit-learn's
    # bag of words tool.
    vectorizer = CountVectorizer(analyzer = "word",   \
                             tokenizer = None,    \
                             preprocessor = None, \
                             stop_words = None,   \
                             max_features = 5000)

    # fit_transform() does two functions: First, it fits the model
    # and learns the vocabulary; second, it transforms our training data
    # into feature vectors. The input to fit_transform should be a list of
    # strings.
    train_data_features = vectorizer.fit_transform(clean_train_reviews)

    # Numpy arrays are easy to work with, so convert the result to an
    # array
    train_data_features = train_data_features.toarray()

    # ******* Train a random forest using the bag of words
    #
    print "Training the random forest (this may take a while)..."


    # Initialize a Random Forest classifier with 100 trees
    forest = RandomForestClassifier(n_estimators = 100)

    # Fit the forest to the training set, using the bag of words as
    # features and the sentiment labels as the response variable
    #
    # This may take a few minutes to run
    forest = forest.fit( train_data_features, train["sentiment"] )



    # Create an empty list and append the clean reviews one by one
    clean_test_reviews = []

    print "Cleaning and parsing the test set movie reviews...\n"
    for i in xrange(0,len(test["review"])):
        clean_test_reviews.append(" ".join(KaggleWord2VecUtility.review_to_wordlist(test["review"][i], True)))

    # Get a bag of words for the test set, and convert to a numpy array
    test_data_features = vectorizer.transform(clean_test_reviews)
    test_data_features = test_data_features.toarray()

    # Use the random forest to make sentiment label predictions
    print "Predicting test labels...\n"
    result = forest.predict(test_data_features)

    # Copy the results to a pandas dataframe with an "id" column and
    # a "sentiment" column
    output = pd.DataFrame( data={"id":test["id"], "sentiment":result} )

    # Use pandas to write the comma-separated output file
    output.to_csv(os.path.join(os.path.dirname(__file__), 'data', 'Bag_of_Words_model.csv'), index=False, quoting=3)
    print "Wrote results to Bag_of_Words_model.csv"
    # a "sentiment" column
    output = pd.DataFrame(data={"id": test["id"], "sentiment": result})

    # Use pandas to write the comma-separated output file
    output.to_csv(os.path.join(os.path.dirname(__file__), 'data', 'Bag_of_Words_model.csv'), index=False, quoting=3)
    print "Wrote results to Bag_of_Words_model.csv"

