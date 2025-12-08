import streamlit as st
from utils.scrape import get_top_songs_from_genius
from utils.text import tokenize, remove_stopwords, stemming
from utils.db import get_connection
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
        # Search bar and button at the top
        st.markdown("## Text Search")
        search_query = st.text_input("Enter your search query:", "", key="search_bar")
        search_button = st.button("Enter", key="search_button")

        # Results window/container
        st.markdown("---")
        st.markdown("### Results")
        results_placeholder = st.empty()
        if search_button and search_query:
            ## searching message
            results_placeholder.write("Searching...")
            # Placeholder for search logic
            songs = get_top_songs_from_genius(search_query, max_songs=slider_val)
            results_placeholder.write(f"Showing results for: **{search_query}**")
            results_placeholder.write(songs)
        else:
            results_placeholder.write("No results to display.")
