import os
from dotenv import load_dotenv
import tweepy
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
load_dotenv()

bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
client = tweepy.Client(bearer_token=bearer_token)
query = 'nasa -is:retweet -is:reply'
tweets = client.search_recent_tweets(
    query=query, tweet_fields=['context_annotations', 'created_at'], max_results=10
)
attributes = [[tweet.text, tweet.created_at, tweet.id] for tweet in tweets.data]

for attribute in attributes:
    print(attribute)

# query = '"#FinanceNews OR #StockMarket OR #EarningsReport -filter:retweets AND -filter:replies AND -filter:links"'
# num_tweets = 10

# try:
#     tweets = client.search_recent_tweets(query=query, tweet_fields=['context_annotations', 'created_at'], max_results=100)
#     attributes = [[tweet.user.name, tweet.created_at, tweet.favorite_count, tweet.source, tweet.full_text] for tweet in tweets]
#     columns = ['user', 'date', 'num_likes', 'source', 'tweet']
#     tweets_df = pd.DataFrame(attributes, columns=columns)
#     print(tweets_df)
# except BaseException as ex:
#     logger.error("Error on data: %s" % str(ex))
