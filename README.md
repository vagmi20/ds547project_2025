## CS547 Group Project - Musical Search Engine Recommender Using TF_IDF and Sentiment Analysis
Welcome to the Search Engine! Given a set of filters and search options, our project intends to display songs that best match the search result. This will help new music listeners to choose songs that best match a specific emotion or term they associate with

[Link to github repository](https://github.com/vagmi20/ds547project_2025)

[Link to project dataset](https://www.kaggle.com/datasets/carlosgdcj/genius-song-lyrics-with-language-information/data)

## Dependencies and Startup

Create and activate environment with python version
```
python3 -m venv my-env
source my-env/bin/activate
```

Install dependencies

```
pip install -r requirements.txt
```

Run the application
```
streamlit run main.py
```
Username is admin, password is admin123

## NLP Processing (Spanish Lyrics)
- Input CSV expected at `data/spanish_lyrics.csv` (with a `lyrics` column).
- Process and normalize Spanish lyrics, then build a simple TF‑IDF index and try a quick search.

Commands:

```
# Install any new dependencies
pip install -r requirements.txt

Our project contains scripts that convert a subset into an SQL DB, which would later be used for querying. 

## NLP Processing (Spanish Lyrics)
- Input CSV expected at `data/spanish_lyrics.csv` (with a `lyrics` column).
- Process and normalize Spanish lyrics, then build a simple TF‑IDF index and try a quick search.

Commands:

```
# Install any new dependencies
pip install -r requirements.txt

# Process Spanish lyrics (creates data/spanish_lyrics_processed.csv)
"""
Process Spanish lyrics CSV for IR:
- Reads input CSV (default: data/spanish_lyrics.csv)
- Cleans/normalizes text
- Tokenizes, removes Spanish stopwords, applies Spanish stemming
- Saves processed CSV with columns: clean_text, token_count

Usage:
    python scripts/process_spanish_lyrics.py \
        --input data/spanish_lyrics.csv \
        --output data/spanish_lyrics_processed.csv
"""
python scripts/process_spanish_lyrics.py \
	--input data/spanish_lyrics.csv \
	--output data/spanish_lyrics_processed.csv \
	--lyrics-col lyrics

# Build TF-IDF index
"""
Build a simple TF-IDF index over processed Spanish lyrics for IR.
Requires input CSV with a 'clean_text' column (from process_spanish_lyrics.py).

Usage:
    python scripts/build_tfidf_index.py \
        --input data/spanish_lyrics_processed.csv \
        --output data/tfidf_index.joblib
"""
python scripts/build_tfidf_index.py \
	--input data/spanish_lyrics_processed.csv \
	--output data/tfidf_index.joblib

# Quick search demo
"""
Tiny search demo over the TF-IDF index.

Usage:
    python scripts/search_demo.py \
        --index data/tfidf_index.joblib \
        --query "amor perdido"
"""
python scripts/search_demo.py \
	--index data/tfidf_index.joblib \
	--query "amor perdido"
```

Notes:
- The processor uses NLTK (Spanish stopwords + Snowball stemmer) and removes accents by default for IR.
- If your CSV uses a different lyrics column name, pass it with `--lyrics-col`.

## Sentiment Analysis


## Demo
In order to access the music engine, please make sure to follow the steps above in terms of Dependencies and Data. 


## Conclusions and Future Work


Notes:
- The processor uses NLTK (Spanish stopwords + Snowball stemmer) and removes accents by default for IR.
- If your CSV uses a different lyrics column name, pass it with `--lyrics-col`.
