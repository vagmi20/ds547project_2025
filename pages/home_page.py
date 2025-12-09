import streamlit as st
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
        genre_rock = st.checkbox("Rock", value=all_genres_checkbox, key="genre_rock")
        genre_pop = st.checkbox("Pop", value=all_genres_checkbox, key="genre_pop")
        genre_hiphop = st.checkbox("Hip-Hop", value=all_genres_checkbox, key="genre_hiphop")
        genre_jazz = st.checkbox("Jazz", value=all_genres_checkbox, key="genre_jazz")
        genre_classical = st.checkbox("Classical", value=all_genres_checkbox, key="genre_classical")

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
                query = " ".join([t for t in [emotion.strip(), year.strip(), language_option.strip()] if t])

            # Call existing search helper (fallback to query even if it's partial)
            songs = collect_search_settings() # placeholder
            results_placeholder.write(f"Showing results for: **{query}**")
            results_placeholder.write(songs)
        else:
            results_placeholder.write("No results to display.")

def collect_search_settings(): 
    # when user submits search, collect all settings from sidebar and query fields and return as dict
    settings = {}
    settings['num_songs'] = st.session_state.get('slider_val', 25)
    settings['language'] = st.session_state.get('language_option', 'All')
    settings['year'] = st.session_state.get('year_input', '')
    settings['emotion'] = st.session_state.get('emotion_input', '') 
    settings['artist'] = st.session_state.get('artist_input', '')    
    if st.session_state.get('all_genres', False):
        settings['genres'] = {
            'rock': True,
            'pop': True,
            'hiphop': True,
            'jazz': True,
            'classical': True,
        }
    else:
        settings['genres'] = {
            'rock': st.session_state.get('genre_rock', False),
            'pop': st.session_state.get('genre_pop', False),
            'hiphop': st.session_state.get('genre_hiphop', False),
            'jazz': st.session_state.get('genre_jazz', False),
            'classical': st.session_state.get('genre_classical', False),
        }
    return settings

def perform_search(query, num):
    # get songs from downloaded db
    data = get_database()
    # sort here based on filters and query
    
    # sentiment analysis ranked list
    sentiment_songs = rank_songs(query, num)
