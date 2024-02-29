import tweepy
import pandas as pd
import json
from datetime import datetime
import s3fs


acces_key = "Gf108Do8c6iYc4Y34u8k9IOss"
access_secret = "kdYdW8CmrY4yo0NtMSFvo3eh1XGAnr6J0dA3Upu94r4EQ8wmW3"
consumer_key = "1578081627888132099-8rZhGdzG2ezz9sONIJ55pYgHzb1XmK"
consumer_secret = "PIQB3F1Tv0skmKFoIDqszrVvZz9quWZgUUyxYEKElqXef"

auth = tweepy.OAuthHandler(acces_key,access_secret)
auth.set_access_token(consumer_key,consumer_secret)

api = tweepy.API(auth)

tweets = api.user_timeline()


