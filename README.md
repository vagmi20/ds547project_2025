## CS547 Group Project - Musical Search Engine Recommender Using TF_IDF and Sentiment Analysis
Welcome to the Search Engine! Given a set of filters and search options, our project intends to display songs that best match the search result. This will help new music listeners to choose songs that best match a specific emotion or term they associate with

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

## Data
Given the high computational overhead and limited resources, we aimed to deploy a subset of songs (up to 300,000) and rather develop a proof-of-concept using Information Retrieval tools. We utilized the following link:

```
https://www.kaggle.com/datasets/carlosgdcj/genius-song-lyrics-with-language-information/data 
```

After downloading and unzipping the CSV, the recommended step is to take a subset and move into the data/ folder of the repo. The easiest way is to take the first 2,000,000 lines. 
```
head {number} data/song_lyrics.csv > data/song_lyrics_subset.csv
```

Our project contains scripts that convert a subset into an SQL DB, which would later be used for querying. 

## NLP Processing (Spanish Lyrics)
- Input CSV expected at `data/genius/spanish_lyrics.csv` (with a `lyrics` column).
- Process and normalize Spanish lyrics, then build a simple TF‑IDF index and try a quick search.

Commands:

```
# Install any new dependencies
pip install -r requirements.txt

# Process Spanish lyrics (creates data/genius/spanish_lyrics_processed.csv)
"""
Process Spanish lyrics CSV for IR:
- Reads input CSV (default: data/genius/spanish_lyrics.csv)
- Cleans/normalizes text
- Tokenizes, removes Spanish stopwords, applies Spanish stemming
- Saves processed CSV with columns: clean_text, token_count

Usage:
    python scripts/process_spanish_lyrics.py \
        --input data/genius/spanish_lyrics.csv \
        --output data/genius/spanish_lyrics_processed.csv
"""
python scripts/process_spanish_lyrics.py \
	--input data/genius/spanish_lyrics.csv \
	--output data/genius/spanish_lyrics_processed.csv \
	--lyrics-col lyrics

# Build TF-IDF index
"""
Build a simple TF-IDF index over processed Spanish lyrics for IR.
Requires input CSV with a 'clean_text' column (from process_spanish_lyrics.py).

Usage:
    python scripts/build_tfidf_index.py \
        --input data/genius/spanish_lyrics_processed.csv \
        --output data/genius/tfidf_index.joblib
"""
python scripts/build_tfidf_index.py \
	--input data/genius/spanish_lyrics_processed.csv \
	--output data/genius/tfidf_index.joblib

# Quick search demo
"""
Tiny search demo over the TF-IDF index.

Usage:
    python scripts/search_demo.py \
        --index data/genius/tfidf_index.joblib \
        --query "amor perdido"
"""
python scripts/search_demo.py \
	--index data/genius/tfidf_index.joblib \
	--query "amor perdido"
```

Notes:
- The processor uses NLTK (Spanish stopwords + Snowball stemmer) and removes accents by default for IR.
- If your CSV uses a different lyrics column name, pass it with `--lyrics-col`.

## Sentiment Analysis


## Demo
In order to access the music engine, please make sure to follow the steps above in terms of Dependencies and Data. 


## Conclusions and Future Work


## Acknowledgements
We would like to thank Professor and the TA for their guidance during the semester.
