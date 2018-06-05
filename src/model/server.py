from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

from word2vecReader import load_model

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

# Create server
with SimpleXMLRPCServer(("localhost", 8000),
                        requestHandler=RequestHandler, allow_none=True) as server:
    server.register_introspection_functions()

    model = load_model()

    # transform one word into a vector
    def word_to_vec(string):
        try:
            return model[string].tolist()
        except KeyError as e:
            return None
    server.register_function(word_to_vec)

    # transform a list of strings into a vector
    def tweet_to_vec(tweet):
        return [word_to_vec(s) for s in tweet]
    server.register_function(tweet_to_vec)

    # return the dictionary words as list
    def get_model_entries():
        return model.keys()
    server.register_function(get_model_entries)

    # process whole lists of tweets
    def tweets_to_vec(tweets):
        return [tweet_to_vec(t) for t in tweets]
    server.register_function(tweets_to_vec)

    # Run the server's main loop
    print('Ready!')
    server.serve_forever()
