import os

import pandas as pd
import numpy as np
from BagOfWords import get_features
from SVM import SVM


def read_data(path):
    return pd.read_csv(os.path.join(os.path.dirname(__file__), path))

def get_sentences(data):
    return data['sentence'].values

def get_emotions(data):
    return data['emotion'].values

if __name__ == '__main__':

    print "Reading data from file"

    train = read_data('./data/real_data.csv')

    train = train[:100]

    sentences = get_sentences(train)
    emotions = get_emotions(train)

    #Transforming emotions to integer values
    emotion_list = list(set(emotions))
    emotion_numbers = {}
    for i in xrange(len(emotion_list)):
        emotion_numbers[emotion_list[i]] = i

    print "Press Enter to Continue..."
    raw_input()

    # Train a SVM using the bag of words
    print "Training the SVM (this may take a while)..."

    # Initialize a SVM classifier
    model = SVM(max_iter=10000, kernel_type='linear', C=1.0, epsilon=0.001)

    X = get_features(sentences)
    y = np.vectorize(emotion_numbers.get)(emotions)

    # Fit the SVM to the training set, using the bag of words as
    # features and the sentiment labels as the response variable
    #
    # This may take a few minutes to run
    model = model.fit(X, y)



