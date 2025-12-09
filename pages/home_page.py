import streamlit as st
from utils.scrape import get_top_songs_from_genius
from utils.text import tokenize, remove_stopwords, stemming
from utils.sentiment_analysis import analysis, rank_songs
# from data.kaggle_data import get_database
# from utils.db import get_connection
import pandas as pd

def home_page():

    # Create columns for main area and sidebar
    main_col, sidebar_col = st.columns([3, 1], gap="large")

    with sidebar_col:
        st.markdown("### Filters & Settings")
        # Example sliders/filters/settings
        slider_val = st.slider("Choose number of song results", 0, 50, 25)
        language_option = st.selectbox("Choose a Language", ["All", "English", "Spanish", "Hindi"])
        # have checkboxes for specific genres
        
        st.markdown("#### Genres")
        all_genres_checkbox = st.checkbox("Choose all Genres", key="all_genres")
        genre_rock = st.checkbox("Rock")
        genre_pop = st.checkbox("Pop")
        genre_hiphop = st.checkbox("Hip-Hop")
        genre_jazz = st.checkbox("Jazz")
        genre_classical = st.checkbox("Classical")

        if all_genres_checkbox:
            genre_rock = True
            genre_pop = True
            genre_hiphop = True
            genre_jazz = True
            genre_classical = True

        st.markdown("---")
        st.write(f"Slider value: {slider_val}")
        st.write(f"Filter: {language_option}")

    with main_col:
        # Replace single search bar with three fields: artist, emotion, year
        st.markdown("## Search by Artist / Emotion / Year")
        with st.form(key="search_form"):
            artist = st.text_input("Artist name (optional):", "", key="artist_input")
            emotion = st.text_input("Emotion / Mood (optional):", "", key="emotion_input")
            year = st.text_input("Year (optional):", "", key="year_input")
            submit = st.form_submit_button("Search")

        # Results window/container
        st.markdown("---")
        st.markdown("### Results")
        results_placeholder = st.empty()

        # Only proceed when user submits at least one field
        if submit and (artist or emotion or year):
            results_placeholder.write("Searching...")
            # Prefer artist when provided, otherwise build a simple query from emotion/year
            if artist:
                query = artist
            else:
                query = " ".join([t for t in [emotion.strip(), year.strip()] if t])

            # Call existing search helper (fallback to query even if it's partial)
            songs = get_top_songs_from_genius(query, max_songs=slider_val)
            results_placeholder.write(f"Showing results for: **{query}**")
            results_placeholder.write(songs)
        else:
            results_placeholder.write("No results to display.")


def perform_search(query, num):
    # get songs from downloaded db
    data = get_database()
    # sort here based on filters and query
    
    # sentiment analysis ranked list
    sentiment_songs = rank_songs(query, num)
