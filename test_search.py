from config import SONG_CSV_PATH, INDEX_PATH
from utils.tfidf_search import perform_tfidf

tfidf_config = {
    'query': 'nas',
    'csv_path': SONG_CSV_PATH,
    'index_path': INDEX_PATH,
    'top_k': 10,
    'filters': {}
}
tfidf_config['filters']['artist'] = 'Eminem'
tfidf_config['filters']['year'] = list(range(
    int('1999'), 
    int('2007') + 1
    ))
print(tfidf_config)
search_results = perform_tfidf(tfidf_config)

# Only print title, artist, and year for each result
for result in search_results:
    print({
        'title': result.get('title'),
        'artist': result.get('artist'),
        'year': result.get('year')
    })