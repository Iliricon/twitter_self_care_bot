import pickle
import re, string
import nltk
from nltk.sentiment.util import demo_tweets
from nltk.tokenize import TweetTokenizer
from sklearn.model_selection import train_test_split
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


SEED = 1337
pattern = re.compile('[\W_]+')

def process(tweet):
    words = tweet.split()
    words = ['TWITTERHANDLE' if w[0] == '@' else w.lower() for w in words]
    words = [pattern.sub('', w) for w in words]
    return words


def load_tweets(dataset='data/dataset/full_tweets_semeval'):
    tweets_file = pickle.load(open(dataset, 'rb'))
    tweets = [(t['object'].text, t['annotation']['label']) for t in tweets_file 
            if t['annotation']['label'] == 'positive' or 
            t['annotation']['label'] == 'negative' or 
            t['annotation']['label'] == 'neutral']
    split_tweets = []
    for tweet, label in tweets:
        split_tweets.append((process(tweet), label))
    print(split_tweets[:10])
    return split_tweets


def create_features(tweet):
    tweet_rep = dict([(word, True) for word in tweet if word not in stopwords.words('english')])
    return tweet_rep



def learn_naive_bayes_classifier(tagged_data):
    tweets = [(create_features(d[0]), l) for d, l in tagged_data if l == 'positive' or l == 'negative']

    train = tweets[:4000]
    test = tweets[4000:]

    classifier = NaiveBayesClassifier.train(train)
    accuracy = nltk.classify.util.accuracy(classifier, test)
    print(accuracy * 100)
    print(len(test))


def test_classifier(tagges_data):
    pass


if __name__ == '__main__':
    tweets = load_tweets_prefab()
    learn_naive_bayes_classifier(tweets)
