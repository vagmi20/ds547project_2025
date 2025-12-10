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
                    id, title, artist, lyrics  tokenize = 'porter'
                );
        """)

        print("building index")
        conn.execute("INSERT INTO lyrics_fts (id, title, artist, lyrics) SELECT id, title, artist, lyrics from mytable;")
        print("finished building index")


def bm25(query):
    conn = get_connection()
    ranked = pd.read_sql_query("SELECT title, artist FROM lyrics_fts WHERE lyrics_fts MATCH :query ORDER BY rank ASC LIMIT 10;", conn, params={"query": query})
    return ranked


def query(query_str, artist=None, language=None, limit=1000):
    artist_cond = "WHERE artist=?"
    langauge_cond = "language=?"
    limit_stmt = "LIMIT ?"

    conn = get_connection()
    params = []
    query_strings = ["SELECT artist, title, sentiment FROM mytable"]
    if artist:
        params.append(artist)
        query_strings.append(artist_cond)
    if language:
        if artist:
            query_strings.append("AND")
        else:
            query_strings.append("WHERE")
        params.append(language)
        query_strings.append(langauge_cond)
    params.append(limit)
    query_strings.append(limit_stmt)

    query = " ".join(query_strings)
    

    songs = pd.read_sql_query(query, conn, params=params)

    return filter_songs_by_sentiment(query_str, songs)



    


   












