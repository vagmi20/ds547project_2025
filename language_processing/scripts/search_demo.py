#!/usr/bin/env python3

import argparse
import sys
import unicodedata

import joblib
import numpy as np
from sklearn.metrics.pairwise import linear_kernel

def strip_accents(text: str) -> str:
    text = unicodedata.normalize('NFD', text)
    return ''.join(ch for ch in text if unicodedata.category(ch) != 'Mn')
def normalize_query(q: str) -> str:
    q = unicodedata.normalize('NFKC', q).lower().strip()
    q = strip_accents(q)
    return q

def main():
    parser = argparse.ArgumentParser(description='Search demo over TF-IDF index')
    parser.add_argument('--index', default='../../../data/genius/tfidf_index.joblib', help='Path to joblib index')
    parser.add_argument('--query', required=True, help='Search query string')
    parser.add_argument('--topk', type=int, default=5, help='Number of results to show')
    args = parser.parse_args()

    try:
        idx = joblib.load(args.index)
    except Exception as e:
        print(f"Failed to load index: {e}", file=sys.stderr)
        sys.exit(1)

    vec = idx['vectorizer']
    X = idx['X']
    titles = idx['titles']
    artists = idx['artists']

    
    q = normalize_query(args.query)
    q_vec = vec.transform([q])
    sims = linear_kernel(q_vec, X).ravel()
    top = np.argsort(sims)[::-1][:args.topk]

    print(f"Query: {args.query}\n")
    for rank, i in enumerate(top, start=1):
        print(f"{rank}. {artists[i]} - {titles[i]} (score={sims[i]:.4f})")


if __name__ == '__main__':
    main()
