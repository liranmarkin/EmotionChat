import os

import pandas as pd
import numpy as np
from BagOfWords import BagOfWords
from sklearn.svm import LinearSVC, SVC
from sklearn.externals import joblib


def read_data(path):
    return pd.read_csv(os.path.join(os.path.dirname(__file__), path))

def get_sentences(data):
    return data['sentence'].values

def get_emotions(data):
    return data['emotion'].values

def initialize_model():
    # Initialize a SVM classifier
    model = LinearSVC(max_iter=1000, tol=0.0001, C=1.0, class_weight=None, verbose=True, random_state=None)
    return model

def fit_model(model, X, y):
    # Fit the model using the bag of words
    print "Fitting the model (this may take a while)..."

    # Fit the model to the training set, using the bag of words as
    # features and the sentiment labels as the response variable
    #
    # This may take a few minutes to run
    model = model.fit(X,y)
    return model

if __name__ == '__main__':

    print "Reading data from file"

    train = read_data('./data/real_data.csv')
    #train = train['emotion' in ['sadness', 'worry', 'surprise']]

    test = train[1000:2000]
    train = train[:40000]
    print train
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
    print "Press Enter to run test..."
    raw_input()

    sentences = get_sentences(test)
    emotions = get_emotions(test)

    X = bag.transform(sentences)
    y = emotions

    print 'model score: ', model.score(X, y)

    print "Press Enter to save the model..."
    raw_input()

    save_name_model = 'model_v1'
    save_name_bag = 'bag_v1'
    save_path_model = os.path.join('./model/', save_name_model)
    save_path_bag = os.path.join('./model/', save_name_bag)

    joblib.dump(model, save_path_model)
    joblib.dump(bag, save_path_bag)

    print "Model saved as ", save_name_model
    print "Bag saved as ", save_name_bag








