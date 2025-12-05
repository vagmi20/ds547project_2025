import nltk
from nltk.sentiment import SentimentIntensityAnalyzer


nltk.download('vader_lexicon')

_analyzer = SentimentIntensityAnalyzer()


def analysis(text):
    return _analyzer.polarity_scores(text)

    

# sentiment analysis for all songs in db
def add_sentiment_to_db(db):
    db['sentiment'] = db['lyrics'].apply(lambda text: _analyzer.polarity_scores(str(text))['compound'])
    return db

# change songs to be a pd type, the pd has name artist and sentiment columns
def rank_songs(songs, num):
    sorted_songs = sorted(songs, key=lambda x: x['sentiment'], reverse=True)
    return sorted_songs[:num]