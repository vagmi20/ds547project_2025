import sqlite3
import pandas as pd
import streamlit as st
import os

from .sentiment_analysis import filter_songs_by_sentiment, add_sentiment_to_db

@st.cache_resource
def get_connection():
    conn = sqlite3.connect("file:data/data.db?mode=ro", uri=True, check_same_thread=False)
    return conn  

def setup_database(data_filepath, force_refresh=False):
    if os.path.exists('data/data.db') and not force_refresh:
        return

    with sqlite3.connect("file:data/data.db", uri=True, check_same_thread=False) as conn:
        df = pd.read_csv(data_filepath, nrows=10000)
        df = add_sentiment_to_db(df)
        print("inserting csv data into database")
        df.to_sql("mytable", conn, if_exists='replace', index=False)


        # Using FTS5 extension which provides automatic BM25 ranking
        print("creating virtual table")
        conn.executescript("""
            DROP TABLE IF EXISTS lyrics_fts;
            CREATE VIRTUAL TABLE lyrics_fts USING fts5(
                    id, title, artist, language, lyrics, tokenize = 'porter'
                );
        """)

        print("building index")
        conn.execute("INSERT INTO lyrics_fts (id, title, artist, language, lyrics) SELECT id, title, artist, language, lyrics from mytable;")
        print("finished building index")


def bm25(query):
    conn = get_connection()
    ranked = pd.read_sql_query("SELECT title, artist FROM lyrics_fts WHERE lyrics_fts MATCH :query ORDER BY rank ASC LIMIT 10;", conn, params={"query": query})
    return ranked


def query(query_str, artist=None, language=None, limit=25):

    conn = get_connection()
    conds = []
    base_query = "SELECT m.artist, m.title, sentiment FROM mytable m INNER JOIN lyrics_fts l on l.id = m.id WHERE lyrics_fts MATCH"
    if artist:
        conds.append(f"(artist: {artist})".replace("'", r"\'"))
    if language:
        conds.append(f"(language: {language})".replace("'", r"\'"))

    cond_str = " AND ".join(conds)
    query_string = f"{base_query} '{cond_str}'"
    print(query_string)
    

    songs = pd.read_sql_query(query_string, conn)

    return filter_songs_by_sentiment(query_str, songs, limit)



    


   












