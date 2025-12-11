#!/usr/bin/env python3
import os
import sys
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

class TfidfBuilder:
    def __init__(self, ngram_range=(1,2), min_df=2):
        self.vectorizer = TfidfVectorizer(ngram_range=ngram_range, min_df=min_df)
        self.X = None

    def fit(self, texts: pd.Series):
        texts = texts.fillna('')
        self.X = self.vectorizer.fit_transform(texts)
        return self

    def build_index(self, df: pd.DataFrame, text_col: str='clean_text'):
        if text_col not in df.columns:
            raise KeyError(f"Input DataFrame must contain '{text_col}' column")
        self.fit(df[text_col])
        titles = df['title'] if 'title' in df.columns else df.get('song_title', pd.Series(['']*len(df)))
        artists = df['artist'] if 'artist' in df.columns else df.get('artist_name', pd.Series(['']*len(df)))
        return {
            'vectorizer': self.vectorizer,
            'X': self.X,
            'titles': titles.tolist(),
            'artists': artists.tolist(),
        }

    def save(self, index: dict, output_path: str):
        os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
        joblib.dump(index, output_path)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True, help='CSV path containing cleaned text')
    parser.add_argument('--output', required=True, help='output joblib path')
    parser.add_argument('--column', default='clean_text', help='text column')
    args = parser.parse_args()
    df = pd.read_csv(args.input)
    builder = TfidfBuilder()
    index = builder.build_index(df, text_col=args.column)
    builder.save(index, args.output)
    print(f"Saved TFIDF index at {args.output}")
