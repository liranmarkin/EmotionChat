import os

import pandas as pd
import numpy as np
from BagOfWords import BagOfWords
from sklearn.svm import LinearSVC, SVC


def read_data(path):
    return pd.read_csv(os.path.join(os.path.dirname(__file__), path))

def get_sentences(data):
    return data['sentence'].values

def get_emotions(data):
    return data['emotion'].values

def initialize_model():
    # Initialize a SVM classifier
    model = SVC(max_iter=1000, tol=0.0001, C=1.0, class_weight=None, verbose=0, random_state=None)
    return model

def fit_model(model, X, y):
    # Fit the model using the bag of words
    print "Fitting the model (this may take a while)..."

    # Fit the SVM to the training set, using the bag of words as
    # features and the sentiment labels as the response variable
    #
    # This may take a few minutes to run
    model = model.fit(X,y)
    return model

if __name__ == '__main__':

    print "Reading data from file"

    train = read_data('./data/real_data.csv')

    test = train[30000:40000]
    train = train[:30000]

    sentences = get_sentences(train)
    emotions = get_emotions(train)

    print "Press Enter to Continue..."
    raw_input()

    bag = BagOfWords()

    X = bag.fit_transform(sentences)
    #y = np.vectorize(emotion_numbers.get)(emotions)
    y = emotions

    model = initialize_model()
    model = fit_model(model, X, y)

    print "Press Enter to Continue..."
    raw_input()

    sentences = get_sentences(test)
    emotions = get_emotions(test)

    X = bag.transform(sentences)
    y = emotions

    print model.score(X, y)








