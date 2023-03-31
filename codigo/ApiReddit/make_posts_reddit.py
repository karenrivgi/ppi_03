import praw
import os
import pickle
from create_access import create_access

dir_path_api = os.path.dirname(os.path.realpath(__file__))
token_file = os.path.join(dir_path_api, "token.pickle")

if os.path.exists(token_file):
    with open(token_file, 'rb') as token:
        creds = pickle.load(token)
else:
    creds = create_access()
    pickle_out = open(token_file,"wb")
    pickle.dump(creds, pickle_out)

reddit = praw.Reddit(client_id=creds['client_id'],
                    client_secret=creds['client_secret'],
                    user_agent=creds['user_agent'],
                    username=creds['username'],
                    password=creds['password'])

dir_path = os.getcwd()
map_path = os.path.join(dir_path, "map.png")

sub = reddit.subreddit("PyMansSky")
sub.submit_image(title="Prueba #3, StarMap", image_path=map_path)