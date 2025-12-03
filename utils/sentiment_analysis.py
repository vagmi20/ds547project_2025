import nltk
from nltk.sentiment import SentimentIntensityAnalyzer


nltk.download('vader_lexicon')

# Create analyzer once at module level (CRITICAL OPTIMIZATION)
# This prevents reloading the VADER lexicon file for every row
_analyzer = SentimentIntensityAnalyzer()


def analysis(text):
    """Analyze sentiment of a single text using the shared analyzer instance."""
    return _analyzer.polarity_scores(text)

    

# sentiment analysis for all songs in db
def add_sentiment_to_db(db):
    """Add sentiment scores to DataFrame efficiently using vectorized operations."""
    # Use apply with the pre-initialized analyzer (much faster than iterrows)
    db['sentiment'] = db['lyrics'].apply(lambda text: _analyzer.polarity_scores(str(text))['compound'])
    return db

# change songs to be a pd type, the pd has name artist and sentiment columns
def rank_songs(songs, num):
    sorted_songs = sorted(songs, key=lambda x: x['sentiment'], reverse=True)
    return sorted_songs[:num]