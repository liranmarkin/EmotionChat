import os
import pandas as pd
import numpy as np

if __name__ == "__main__":
    text_emotion = pd.read_csv(os.path.join(os.path.dirname(__file__), 'text_emotion.csv'))

    emotions = text_emotion['sentiment']
    sentences = text_emotion['content']

    data = pd.DataFrame({
        "emotion" : emotions,
        "sentence" : sentences
    })

    data.to_csv('real_data.csv')
