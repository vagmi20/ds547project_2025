#!/usr/bin/env python3
import argparse
import csv
import os
import re
import sys
import unicodedata

import pandas as pd

# NLTK 
try:
    import nltk
    from nltk.corpus import stopwords
    from nltk.stem.snowball import SnowballStemmer
    from nltk.tokenize import TweetTokenizer
except Exception as e:
    print("NLTK not available.", file=sys.stderr)
    raise

try:
    import emoji
except Exception:
    emoji = None


def ensure_nltk_resources():
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords', quiet=True)


def strip_accents(text: str) -> str:
    text = unicodedata.normalize('NFD', text)
    return ''.join(ch for ch in text if unicodedata.category(ch) != 'Mn')


def remove_emoji(text: str) -> str:
    if emoji is None:
        return text
    return emoji.replace_emoji(text, replace=' ')


def clean_text(text: str, *, keep_accents: bool = False) -> str:
    if not isinstance(text, str):
        return ''
    # Normalize spaces/unicode
    text = unicodedata.normalize('NFKC', text)
    text = text.lower()
    # Remove emoji
    text = remove_emoji(text)
    # Remove URLs and handles
    text = re.sub(r'https?://\S+|www\.\S+', ' ', text)
    text = re.sub(r'@[A-Za-z0-9_]+', ' ', text)
    # Strip accents unless requested
    if not keep_accents:
        text = strip_accents(text)
    # Replace non-word except spaces (keep letters/numbers)
    text = re.sub(r"[^\w\s]", " ", text, flags=re.UNICODE)
    # Collapse whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text


def tokenize_spanish(text: str, stopword_set: set, stemmer: SnowballStemmer) -> list:
    print("starting tokenizer")
    tokenizer = TweetTokenizer(preserve_case=False, strip_handles=True, reduce_len=True)
    tokens = tokenizer.tokenize(text)
    tokens = [t for t in tokens if re.match(r'^[\w]+$', t, flags=re.UNICODE)]
    tokens = [t for t in tokens if t not in stopword_set]
    tokens = [stemmer.stem(t) for t in tokens]
    tokens = [t for t in tokens if t not in stopword_set]
    return tokens


def process_dataframe(df: pd.DataFrame, lyrics_col: str, keep_accents: bool = False) -> pd.DataFrame:
    ensure_nltk_resources()
    stopword_set = set(stopwords.words('spanish'))
    stemmer = SnowballStemmer('spanish')

    if lyrics_col not in df.columns:
        raise KeyError(f"lyrics column not found. Found: {list(df.columns)}")
    cleaned = []
    token_counts = []
    for txt in df[lyrics_col].astype(str):
        c = clean_text(txt, keep_accents=keep_accents)
        toks = tokenize_spanish(c, stopword_set, stemmer)
        cleaned.append(' '.join(toks))
        token_counts.append(len(toks))

    df_out = df.copy()
    df_out['clean_text'] = cleaned
    df_out['token_count'] = token_counts
    return df_out


def main():
    parser = argparse.ArgumentParser(description="Process Spanish lyrics CSV for IR")
    parser.add_argument('--input', default='data/genius/spanish_lyrics.csv', help='Input CSV path')
    parser.add_argument('--output', default='data/genius/spanish_lyrics_processed.csv', help='Output CSV path')
    parser.add_argument('--lyrics-col', default='lyrics', help='Column name containing lyrics text')
    parser.add_argument('--keep-accents', action='store_true', help='Keep accents/diacritics (default strips)')
    parser.add_argument('--sample', type=int, default=3, help='Print N sample processed rows')
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)
    print(f"reading file: {args.input}")
    try:
        df = pd.read_csv(args.input)
    except UnicodeDecodeError:
        df = pd.read_csv(args.input, encoding='latin-1')
    print(f"starting processing")
    df_out = process_dataframe(df, lyrics_col=args.lyrics_col, keep_accents=args.keep_accents)

    os.makedirs(os.path.dirname(args.output) or '.', exist_ok=True)
    df_out.to_csv(args.output, index=False)
    print(f"Saved processed CSV -> {args.output}")
if __name__ == '__main__':
    main()
