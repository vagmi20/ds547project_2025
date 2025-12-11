import joblib
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def perform_tfidf(config: dict):
    """
    Perform TF-IDF search with optional filtering.
    
    Args:
        config (dict): Configuration dictionary with the following keys:
            - query (str): Search query term
            - csv_path (str): Path to the processed CSV file
            - index_path (str): Path to the TF-IDF index joblib file
            - top_k (int, optional): Number of results to return (default: 10)
            - filters (dict, optional): Dictionary of column filters, e.g.:
                {'year': 2020, 'artist': 'Taylor Swift', 'language_cld3': 'en'}
    
    Returns:
        list: List of dictionaries containing search results with columns from CSV
    """
    query = config.get('query', '')
    csv_path = config.get('csv_path')
    index_path = config.get('index_path')
    top_k = config.get('top_k', 10)
    filters = config.get('filters', {})
    
    if not csv_path or not index_path:
        raise ValueError("csv_path and index_path are required in config")
    
    #load tfidf index
    index = joblib.load(index_path)
    vectorizer = index['vectorizer']
    X = index['X']
    
    df = pd.read_csv(csv_path)
    
    filtered_indices = np.arange(len(df))
    if filters:
        mask = pd.Series([True] * len(df))
        for col, value in filters.items():
            if col in df.columns:
                if isinstance(value, list):
                    mask &= df[col].isin(value)
                else:
                    mask &= (df[col] == value)
        filtered_indices = np.where(mask)[0]
    if len(filtered_indices) == 0:
        return []
    
    # Vectorize
    query_vec = vectorizer.transform([query])
    
    X_filtered = X[filtered_indices]
    similarities = cosine_similarity(query_vec, X_filtered).flatten()
    
    # Get top k results
    top_indices = similarities.argsort()[::-1][:top_k]
    original_indices = filtered_indices[top_indices]
    
    results = []
    for i, orig_idx in enumerate(original_indices):
        result = df.iloc[orig_idx].to_dict()
        result['score'] = float(similarities[top_indices[i]])
        results.append(result)
    
    return results
