import streamlit as st
from utils.db import query_db, setup_database
from utils.playlist_search import find_playlist
import pandas as pd
from utils.tfidf_search import perform_tfidf

def home_page():
    setup_database('data/song_lyrics_subset.csv')
    # Create columns for main area and sidebar
    main_col, sidebar_col = st.columns([3, 1], gap="large")

    with sidebar_col:
        st.markdown("### Filters & Settings")
        slider_val = st.slider("Choose number of song results", 0, 50, 25, key='slider_val')
        language_option = st.selectbox("Choose a Language", ["All", "English", "Spanish", "Hindi"], key='language_option')

        # Initialize genre-related session state keys if missing
        genres = ['genre_rock', 'genre_pop', 'genre_hiphop', 'genre_jazz', 'genre_classical', 'genre_rap']
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
        st.checkbox("Rap", key="genre_rap", on_change=_on_individual_change)

    with main_col:
        # let user select between two search forms (emotion vs TF_IDF)
        st.markdown("# Music Search Engine")

        # Let user choose which search form to use
        form_choice = st.selectbox("Choose search form:", ["Search by Emotion", "Search Generic Playlist", "Search by Term Importance"], key='form_choice')

        if form_choice == "Search by Term Importance":
            with st.form(key="search_form"):
                artist = st.text_input("Artist name (optional):", "", key="artist_input")
                term = st.text_input("Term (required):", "", key="term_input")
                year = st.text_input("Year Range (optional) Use 's' for eras or '-' to specify a range:", "", key="year_input")
                term_submit = st.form_submit_button("Search")
        
                results = st.empty()
                if term_submit and term:
                    results.write("Searching...")
                    configurations = collect_search_settings()
                    
                    # Prepare TF-IDF search config
                    tfidf_config = {
                        'query': term,
                        'csv_path': './data/tfidf_all.csv',
                        'index_path': './data/tfidf_index.joblib',
                        'top_k': configurations.get('num_songs', 25),
                        'filters': {}
                    }
    
                    if artist:
                        tfidf_config['filters']['artist'] = artist
                    if configurations.get('year_start') and configurations.get('year_end'):
                        # You may need to adjust this based on your CSV column name for year
                        tfidf_config['filters']['year'] = list(range(
                            int(configurations['year_start']), 
                            int(configurations['year_end']) + 1
                        ))
                
                    search_results = perform_tfidf(tfidf_config)
                    
                    if search_results:
                        results.write(f"Found {len(search_results)} results for '{term}':")
                        df_results = pd.DataFrame([{
                            'Title': r.get('title', 'N/A'),
                            'Artist': r.get('artist', 'N/A'),
                            'Score': f"{r['score']:.3f}"
                        } for r in search_results])
                        st.dataframe(df_results, hide_index=True)
                    else:
                        results.write(f"No results found for '{term}'.")
                else:
                    results.write("Please enter a term to search.")
        elif form_choice == "Search Generic Playlist":
            # raw single search bar with year
            # disable the language field since it's language agnostic
            with st.form(key="search_form"):
                st.markdown("All Filters are disbaled and therefore won't work in this form mode.")
                raw_search_bar = st.text_input("Generic Terms (Required):", "", key="generic_input")
                year = st.text_input("Year Range (optional) Use 's' for eras or '-' to specify a range:", "", key="year_input", disabled=True, placeholder="Disabled in this mode")
                generic_submit = st.form_submit_button("Search")
            
                results = st.empty()
                if generic_submit and raw_search_bar:
                    results.write("Searching...")
                    configurations = collect_search_settings() # placeholder
                    config = {
                        'csv_path': 'data/song_lyrics_subset.csv',
                        'playlist_metadata_path': 'data/playlist_metadata.csv',
                        'top_k': configurations['num_songs'],
                        'min_playlist_count': 1
                    }
                    
                    # Call playlist finder
                    playlist_results = find_playlist(raw_search_bar, config)
                
                    if playlist_results:
                        results.write(f"Found {len(playlist_results)} songs matching '{raw_search_bar}':")
                        # Format results as a dataframe for display
                        df_results = pd.DataFrame([{
                            'Title': r['title'],
                            'Artist': r['artist'],
                            'Score': f"{r['score']:.3f}",
                            'Playlists': r['playlist_count']
                        } for r in playlist_results])
                        st.dataframe(df_results, hide_index=True)
                else:
                    results.write(f"No results found for '{raw_search_bar}'.")
                
                # Only proceed when user submits at least one field

    
        else:
            with st.form(key="search_form"):
                artist = st.text_input("Artist name (optional):", "", key="artist_input")
                emotion = st.text_input("Emotion / Mood (optional):", "", key="emotion_input")
                year = st.text_input("Year Range (optional) Use 's' for eras or '-' to specify a range:", "", key="year_input")
                three_submit = st.form_submit_button("Search")

                # Only proceed when user submits at least one field
                results = st.empty()
                if three_submit and (artist or emotion or year):
                    results.write("Searching...")
                    # results.progress(0)
                    # Call existing search helper (fallback to query even if it's partial)
                    configurations = collect_search_settings() # placeholder
                    songs = query_db(configurations)
                    results.write(f"Showing results for query")
                    st.dataframe(songs, hide_index=True)
                    print(songs)
                    # results.write(songs)
                else:
                    results.write("No results to display.")

def collect_search_settings(): 
    # when user submits search, collect all settings from sidebar and query fields and return as dict
    settings = {}
    settings['num_songs'] = st.session_state.get('slider_val', 25)
    settings['language'] = st.session_state.get('language_option', 'All')
    if 's' in st.session_state.get('year_input', None): # decades like '1990s'
        # add year_start and year_end keys
        settings['year_start'] = int(st.session_state.get('year_input', None)[:4])
        settings['year_end'] = settings['year_start'] + 9
    elif '-' in st.session_state.get('year_input', None): # range like '1990-2000'
        parts = st.session_state.get('year_input', None).split("-")
        settings['year_start'] = int(parts[0])
        settings['year_end'] = int(parts[1])
    else:
        settings['year_start'] = st.session_state.get('year_input', None)
        settings['year_end'] = st.session_state.get('year_input', None)
    settings['term'] = st.session_state.get('term_input', None)
    settings['emotion'] = st.session_state.get('emotion_input', None)
    settings['generic'] = st.session_state.get('generic_input', None) 
    settings['artist'] = st.session_state.get('artist_input', None)    
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
            'rap': st.session_state.get('genre_rap', False)
        }
    return settings
