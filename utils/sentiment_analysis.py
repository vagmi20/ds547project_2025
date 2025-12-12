import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import pandas as pd

nltk.download('vader_lexicon')

_analyzer = SentimentIntensityAnalyzer()


def analysis(text):
    return _analyzer.polarity_scores(text)
    

# sentiment analysis for all songs in db
def add_sentiment_to_db(db):
    db['sentiment'] = db['lyrics'].apply(lambda text: _analyzer.polarity_scores(str(text))['compound'])
    return db


def rank_songs(songs, num):
    sorted_songs = sorted(songs, key=lambda x: x['sentiment'], reverse=True)
    return sorted_songs[:num]


def filter_songs_by_sentiment(query, songs, limit):
    query_analysis = analysis(query)["compound"]
    songs["diff"] = abs(songs["sentiment"] - query_analysis)
    return songs.sort_values(by="diff").iloc[:limit, :]
    