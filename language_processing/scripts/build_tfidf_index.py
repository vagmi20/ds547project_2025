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
