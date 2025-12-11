#!/usr/bin/env python3

import argparse
import sys
import unicodedata
import os
import joblib
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import linear_kernel

def strip_accents(text: str) -> str:
    text = unicodedata.normalize('NFD', text)
    return ''.join(ch for ch in text if unicodedata.category(ch) != 'Mn')

def normalize_query(q: str) -> str:
    q = unicodedata.normalize('NFKC', q).lower().strip()
    q = strip_accents(q)
    return q

def main():
    tfidf_index_path = os.path.join('/home/ostikar/MyProjects/CS547/project/data/genius', 'tfidf_index.joblib')
    csv_default_path = os.path.join('/home/ostikar/MyProjects/CS547/project/data', 'song_lyrics.csv')
    parser = argparse.ArgumentParser(description='Search demo over TF-IDF index with optional CSV filters')
    parser.add_argument('--index', default=tfidf_index_path, help='Path to joblib index')
    parser.add_argument('--csv', default=csv_default_path, help='Path to CSV with song metadata')
    parser.add_argument('--query', required=True, help='Search query string')
    parser.add_argument('--topk', type=int, default=5, help='Number of results to show')
    # Optional filters
    parser.add_argument('--artist', type=str, help='Filter by exact artist name')
    parser.add_argument('--language', type=str, help='Filter by language code (e.g., en, es)')
    parser.add_argument('--year-min', type=int, help='Minimum year')
    parser.add_argument('--year-max', type=int, help='Maximum year')
    parser.add_argument('--contains', type=str, help='Substring filter on title or lyrics')
    args = parser.parse_args()

    # Load index
    try:
        idx = joblib.load(args.index)
    except Exception as e:
        print(f"Failed to load index: {e}", file=sys.stderr)
        sys.exit(1)

    vec = idx['vectorizer']
    X = idx['X']

    # Optional: titles/artists may be present in index; else load from CSV
    titles = idx.get('titles', None)
    artists = idx.get('artists', None)

    # Load CSV for filters and full metadata
    try:
        df = pd.read_csv(args.csv, engine='python', on_bad_lines='skip')
    except Exception as e:
        print(f"Failed to load CSV: {e}", file=sys.stderr)
        sys.exit(1)

    if len(df) != X.shape[0]:
        print(f"Warning: CSV rows ({len(df)}) != TF-IDF rows ({X.shape[0]}). Ensure index built from this CSV.", file=sys.stderr)

    # Build filter mask
    mask = pd.Series([True] * len(df))
    if args.artist:
        mask &= (df['artist'].astype(str) == args.artist)
    if args.language:
        col = 'language_cld3' if 'language_cld3' in df.columns else 'language'
        if col in df.columns:
            mask &= (df[col].astype(str) == args.language)
    if args.year_min is not None and 'year' in df.columns:
        mask &= (pd.to_numeric(df['year'], errors='coerce') >= args.year_min)
    if args.year_max is not None and 'year' in df.columns:
        mask &= (pd.to_numeric(df['year'], errors='coerce') <= args.year_max)
    if args.contains:
        substr = args.contains.lower()
        title_col = df['title'].astype(str).str.lower() if 'title' in df.columns else pd.Series([''] * len(df))
        lyrics_col = df['lyrics'].astype(str).str.lower() if 'lyrics' in df.columns else pd.Series([''] * len(df))
        mask &= (title_col.str.contains(substr, na=False) | lyrics_col.str.contains(substr, na=False))

    filtered_idx = np.where(mask.values)[0]
    if filtered_idx.size == 0:
        print("No rows match the given filters.", file=sys.stderr)
        sys.exit(0)

    # Compute similarities within filtered subset
    q = normalize_query(args.query)
    q_vec = vec.transform([q])
    sims = linear_kernel(q_vec, X[filtered_idx]).ravel()
    top_local = np.argsort(sims)[::-1][:args.topk]
    top_global = filtered_idx[top_local]

    print(f"Query: {args.query}\nFilters: artist={args.artist}, language={args.language}, year_min={args.year_min}, year_max={args.year_max}, contains={args.contains}\n")
    for rank, i in enumerate(top_global, start=1):
        art = artists[i] if artists is not None and i < len(artists) else (df.iloc[i]['artist'] if 'artist' in df.columns else 'Unknown')
        tit = titles[i] if titles is not None and i < len(titles) else (df.iloc[i]['title'] if 'title' in df.columns else f'Row {i}')
        print(f"{rank}. {art} - {tit} (score={sims[top_local[rank-1]]:.4f})")

if __name__ == '__main__':
    main()