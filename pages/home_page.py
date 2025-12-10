import streamlit as st
from utils.text import tokenize, remove_stopwords, stemming
from utils.sentiment_analysis import analysis, rank_songs
# from data.kaggle_data import get_database
# from utils.db import get_connection

def home_page():

    # Create columns for main area and sidebar
    main_col, sidebar_col = st.columns([3, 1], gap="large")

    with sidebar_col:
        st.markdown("### Filters & Settings")
        slider_val = st.slider("Choose number of song results", 0, 50, 25, key='slider_val')
        language_option = st.selectbox("Choose a Language", ["All", "English", "Spanish", "Hindi"], key='language_option')

        # Initialize genre-related session state keys if missing
        genres = ['genre_rock', 'genre_pop', 'genre_hiphop', 'genre_jazz', 'genre_classical']
        for g in genres:
            st.session_state.setdefault(g, False)
        st.session_state.setdefault('all_genres', False)

        st.markdown("#### Genres")

        # Callback when select-all is toggled: only act when it becomes True (select everything)
        def _on_all_genres_change():
            if st.session_state.all_genres:
                # set all individual genre checkboxes to True
                for g in genres:
                    st.session_state[g] = True

        # Callback when any individual genre changes: keep all_genres synced (True only when all selected)
        def _on_individual_change():
            st.session_state['all_genres'] = all(st.session_state[g] for g in genres)

        st.checkbox("Choose all Genres", key="all_genres", on_change=_on_all_genres_change)
        # individual checkboxes are initialized from session_state and update the sync callback
        st.checkbox("Rock", key="genre_rock", on_change=_on_individual_change)
        st.checkbox("Pop", key="genre_pop", on_change=_on_individual_change)
        st.checkbox("Hip-Hop", key="genre_hiphop", on_change=_on_individual_change)
        st.checkbox("Jazz", key="genre_jazz", on_change=_on_individual_change)
        st.checkbox("Classical", key="genre_classical", on_change=_on_individual_change)

    with main_col:
        # let user select between two search forms
        st.markdown("# Music Search Engine")
        # include 2 search forms, one single raw search bar, one with 3 fields

        # Let user choose which search form to use
        form_choice = st.selectbox("Choose search form:", ["Raw Query", "Artist/Emotion/Year"], key='form_choice')

        # single raw search bar
        if form_choice == "Raw Query":
            with st.form(key="raw_search_form"):
                raw_query = st.text_input("Enter your search query:", "", key="raw_query_input")
                raw_submit = st.form_submit_button("Search")
        
            results = st.empty()
            if raw_submit and raw_query:
                results.write("Searching...")
                # results.progress(0)
        
                # Call existing search helper (fallback to query even if it's partial)
                configurations = collect_search_settings() # placeholder
                configurations['raw_query'] = raw_query
                cleaned_search = parse_raw_query(raw_query)
                perform_search(configurations)
                results.write(f"Showing results for query: {raw_query}")
                results.write(configurations)
            else:
                results.write("No results to display.")

    
        if form_choice == "Artist/Emotion/Year":
            with st.form(key="search_form"):
                artist = st.text_input("Artist name (optional):", "", key="artist_input")
                emotion = st.text_input("Emotion / Mood (optional):", "", key="emotion_input")
                year = st.text_input("Year (optional):", "", key="year_input")
                three_submit = st.form_submit_button("Search")

                # Only proceed when user submits at least one field
            results = st.empty()
            if three_submit and (artist or emotion or year):
                results.write("Searching...")
                # results.progress(0)
        

                # Call existing search helper (fallback to query even if it's partial)
                configurations = collect_search_settings() # placeholder
                perform_search(configurations)
                results.write(f"Showing results for query")
                results.write(configurations)
            else:
                results.write("No results to display.")

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

def perform_search(settings):
    # get songs from downloaded db
    data = get_database()
    # sort here based on filters and query
    
    # sentiment analysis ranked list
    sentiment_songs = rank_songs(settings)
