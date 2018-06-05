import pickle

import keras
import numpy as np
import xmlrpc.client

from sentiment_baseline import process


def load_tweets(dataset='data/dataset/full_tweets_semeval'):
    tweets_file = pickle.load(open(dataset, 'rb'))
    tweets = [(t['object'].text, t['annotation']['label']) for t in tweets_file 
            if t['annotation']['label'] == 'positive' or 
            t['annotation']['label'] == 'negative' or 
            t['annotation']['label'] == 'neutral']
    split_tweets = []
    for tweet, label in tweets:
        split_tweets.append((tweet, label))
    return split_tweets


def get_tweets_vector(tweets):
    with xmlrpc.client.ServerProxy("http://localhost:8000") as proxy:
        return proxy.tweets_to_vec([process(tweet) for tweet in tweets])


if __name__ == "__main__":
    tweets = load_tweets()
    dataset = get_tweets_vector([t for t, l in tweets])
    labels = [l for t, l in tweets]

    counter = 0
    nones = 0
    for datum in dataset:
        for entry in datum:
            counter += 1
            if entry is None:
                nones += 1

    print(counter)
    print(nones)

