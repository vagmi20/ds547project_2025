import joblib
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from utils.tfidf_search import perform_tfidf

def find_playlist(query, config):
    csv_path = config.get('csv_path')
    playlist_metadata_path = config.get('playlist_metadata_path')
    top_k = config.get('top_k', 20)
    filters = config.get('filters', {})
    min_playlist_count = config.get('min_playlist_count', 1)
    if not csv_path or not playlist_metadata_path:
        raise ValueError("csv_path and playlist_metadata_path required")
    df = pd.read_csv(csv_path, engine='python', on_bad_lines='skip', usecols=['title', 'artist'])
    playlist_meta = pd.read_csv(playlist_metadata_path, usecols=['title', 'artist', 'playlists', 'playlist_count', 'tags'])

    # Build hash lookup
    meta_lookup = {}
    for _, row in playlist_meta.iterrows():
        key = (str(row['title']).lower().strip(), str(row['artist']).lower().strip())
        meta_lookup[key] = row

    #filter songs by playlist count and additional filters
    results = []
    for _, song in df.iterrows():
        key = (str(song['title']).lower().strip(), str(song['artist']).lower().strip())
        meta = meta_lookup.get(key)
        if meta is None or meta['playlist_count'] < min_playlist_count:
            continue
        passed = True
        for col, value in filters.items():
            if col in meta and meta[col] != value:
                passed = False
                break
        if not passed:
            continue
        search_text = str(meta['playlists']) + ' ' + str(meta['tags'])
        results.append({
            'title': song['title'],
            'artist': song['artist'],
            'playlists': meta['playlists'],
            'playlist_count': meta['playlist_count'],
            'tags': meta['tags'],
            'search_text': search_text
        })

    if not results:
        return []

    search_texts = [r['search_text'] for r in results]
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1)
    playlist_vectors = vectorizer.fit_transform(search_texts)
    query_vec = vectorizer.transform([query])

    similarities = cosine_similarity(query_vec, playlist_vectors).flatten()
    playlist_boost = np.log1p([r['playlist_count'] for r in results])
    combined_scores = similarities * 0.7 + (playlist_boost / np.max(playlist_boost)) * 0.3
    top_indices = np.argsort(combined_scores)[::-1][:top_k]
    final_results = []
    for idx in top_indices:
        result = results[idx].copy()
        result['score'] = float(combined_scores[idx])
        result['similarity'] = float(similarities[idx])
        final_results.append(result)
    return final_results


def search_by_lyrics_and_playlist(query, config):
    """
    Hybrid search combining lyrics TF-IDF and playlist matching
    
    Args:
        query (str): Search query
        config (dict): Configuration with:
            - csv_path, index_path, playlist_metadata_path
            - lyrics_weight (float): Weight for lyrics match (0-1, default 0.5)
            - playlist_weight (float): Weight for playlist match (0-1, default 0.5)
            - top_k (int): Number of results
    
    Returns:
        list: Ranked results
    """
    lyrics_weight = config.get('lyrics_weight', 0.5)
    playlist_weight = config.get('playlist_weight', 0.5)
    top_k = config.get('top_k', 20)
    
    lyrics_config = config.copy()
    lyrics_config['top_k'] = top_k * 2  
    lyrics_results = perform_tfidf(lyrics_config)
    
    playlist_results = find_playlist(query, config)
    
    combined = {}
    for result in lyrics_results:
        key = (result['title'], result['artist'])
        combined[key] = {
            'data': result,
            'lyrics_score': result['score'],
            'playlist_score': 0
        }
    
    for result in playlist_results:
        key = (result['title'], result['artist'])
        if key in combined:
            combined[key]['playlist_score'] = result['score']
        else:
            combined[key] = {
                'data': result,
                'lyrics_score': 0,
                'playlist_score': result['score']
            }
    
    #calculate final scores
    final_results = []
    for key, item in combined.items():
        final_score = (
            lyrics_weight * item['lyrics_score'] + 
            playlist_weight * item['playlist_score']
        )
        result = item['data'].copy()
        result['final_score'] = final_score
        result['lyrics_score'] = item['lyrics_score']
        result['playlist_score'] = item['playlist_score']
        final_results.append(result)
    
    #sort by final score
    final_results.sort(key=lambda x: x['final_score'], reverse=True)
    
    return final_results[:top_k]

if __name__ == "__main__":
    config = {
        'csv_path' : '/home/ostikar/MyProjects/CS547/project/data/tfidf_all.csv',
        'playlist_metadata_path' : '/home/ostikar/MyProjects/CS547/project/data/playlist_metadata.csv',
        'top_k' : 20
    }
    playlist = find_playlist('house party', config)
    for item in playlist:
        print(f"{item['title']} by {item['artist']}")

