#!/usr/bin/env python3

import argparse
import os
import sys

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer


def build_index(df: pd.DataFrame):
    texts = df['clean_text'].fillna('')
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=2)
    X = vectorizer.fit_transform(texts)

    #Basic metadata to present search results
    titles = df['title'] if 'title' in df.columns else df.get('song_title', pd.Series(['']*len(df)))
    artists = df['artist'] if 'artist' in df.columns else df.get('artist_name', pd.Series(['']*len(df)))

    index = {
        'vectorizer': vectorizer,
        'X': X,
        'titles': titles.tolist(),
        'artists': artists.tolist(),
    }
    return index


def main():
    parser = argparse.ArgumentParser(description='Build TF-IDF index for Spanish lyrics')
    parser.add_argument('--input', default='data/genius/spanish_lyrics_processed.csv', help='Processed CSV path')
    parser.add_argument('--output', default='data/genius/tfidf_index.joblib', help='Output index file')
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"file not found: {args.input}", file=sys.stderr)
        sys.exit(1)
    df = pd.read_csv(args.input)
    if 'clean_text' not in df.columns:
        print("Input CSV must contain 'clean_text'. Run process_spanish_lyrics.py first.", file=sys.stderr)
        sys.exit(1)

    index = build_index(df)
    os.makedirs(os.path.dirname(args.output) or '.', exist_ok=True)
    joblib.dump(index, args.output)
    print(f"Saved TF-IDF index -> {args.output}")
if __name__ == '__main__':
    main()
