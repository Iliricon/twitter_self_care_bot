import pprint
import csv
import tweepy
import pickle
from tweepy import OAuthHandler
from tweepy import TweepError

# registers a PrettyPrinter for debugging purposes
pp = pprint.PrettyPrinter(indent=4)

def get_api_token():
    '''
    Reads the secrets file for api tokens
    '''
    with open('secrets.txt', 'r') as f:
        # [:-1] strips newline from end
        consumer_key = f.readline()[:-1]
        consumer_secret = f.readline()[:-1]
        access_token = f.readline()[:-1]
        access_secret = f.readline()[:-1]
    return consumer_key, consumer_secret, access_token, access_secret


def authenticate():
    '''
    Loads auth tokens and performs the api authorization for twitter
    '''
    key, secret, access_token, access_secret = get_api_token()
    auth = OAuthHandler(key, secret)
    auth.set_access_token(access_token, access_secret)

    api = tweepy.API(auth)
    return api


def load_data():
    '''
    The function loads the original research data and crawls twitter for the associated
    tweetts and users. The enhanced dataset is stored as "tweet_level_data.json" in the
    datasets folder and available for preprocessing and modelling. The tweet data is
    joined with the annotation label, 0 denoting no anotator found signs of depression,
    1 denoting 1 annotator who found signs of depression and 2 denoting a clearly
    depressive tweet.

    The data is saved in "dataset/full_tweets.pickle"
    '''
    # gather tweet id's from dataset
    with open('dataset/60Users_annotations.csv', 'r') as csvfile:
        tweet_reader = csv.DictReader(csvfile, delimiter=',')
        tweet_list = [tweet for tweet in tweet_reader]
    api = authenticate()
    
    removed_tweets = 0
    depressed_tweets = 0
    removed_depressed_tweets = 0
    full_tweets = []

    # try to download the actual tweets from twitter
    for tweet in tweet_list:
        try:
            level = 0
            if tweet['annotator1'] == '1':
                level += 1
            if tweet['annotator2'] == '1':
                level += 1
            full_tweets.append({'object': api.get_status(id=tweet['id']), 'annotation': level})
            if level > 0:
                depressed_tweets += 1
        except TweepError as e:
            removed_tweets += 1
            if tweet['annotator1'] == '1' or tweet['annotator2'] == 1:
                removed_depressed_tweets += 1
    # gives an indication how many tweets were removed since the dataset was created
    print('Removed: {}'.format(removed_tweets))
    print('Depressed (kept): {}'.format(depressed_tweets))
    print('Depressed (removed): {}'.format(removed_depressed_tweets))
    
    # saves the data to the pickled file
    pickle.dump(full_tweets, open('dataset/full_tweets.pickle', 'wb'))


def preprocessing():
    pass


if __name__ == '__main__':
    load_data()
