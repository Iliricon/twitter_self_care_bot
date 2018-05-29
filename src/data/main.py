import pprint
import sys
import time
import csv
import tweepy
import pickle
from tweepy import OAuthHandler
from tweepy import TweepError
from tweepy import RateLimitError

# registers a PrettyPrinter for debugging purposes
pp = pprint.PrettyPrinter(indent=4)

def get_api_token():
    '''
    Reads the secrets file for api tokens
    '''
    with open('data/secrets.txt', 'r') as f:
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
    rate_limit_wait = False
    api = tweepy.API(auth, wait_on_rate_limit=rate_limit_wait, wait_on_rate_limit_notify=rate_limit_wait)
    return api


def load_data(dataset='dataset/depression_tagged/60Users_annotations.csv', output_location='dataset/full_depression.pickle', delimiter=','):
    with open(dataset, 'r') as csvfile:
        tweet_reader = csv.DictReader(csvfile, delimiter=delimiter)
        tweet_list = [tweet for tweet in tweet_reader]

    download_data(tweet_list, output_location)



def download_data(tweet_list, output_location):
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
    api = authenticate()
    
    full_tweets = []
    len_list = len(tweet_list)
    start_time = time.time()
    # try to download the actual tweets from twitter
    i = 0
    while i < len_list:
        tweet = tweet_list[i]
        if i > 0 and i%50 ==0:
            print('\rDownloading {} %, Time passed: {} s, Tweets loaded: {}'     .format(
                round(i*100/len_list, 3), 
                round(time.time() - start_time), 
                i), end="", flush=True)
        try:
            # append tweet to list of all tweets
            full_tweets.append({'object': api.get_status(id=tweet['id']), 'annotation': tweet})
            i += 1
        except RateLimitError as e:
            reset = int(e.response.headers['x-rate-limit-reset'])
            wait = int(reset-time.time())
            print('\rDownload at {}% | Rate limit hit, waiting {} s            '.format(round(i*100/len_list,3), wait), end="", flush=True)
            pickle.dump(full_tweets, open(output_location + '_{}.pickle'.format(i), 'wb'))
            time.sleep(1)
            continue
        except TweepError as e:
            i += 1
    
    # gives an indication how many tweets were removed since the dataset was created
    print('Finished')
    
    # saves the data to the pickled file
    pickle.dump(full_tweets, open(output_location, 'wb'))


def preprocessing():
    pass


if __name__ == '__main__':
    load_data()
