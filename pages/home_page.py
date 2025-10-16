import streamlit as st
from utils.scrape import get_top_songs_from_genius
from utils.text import tokenize, remove_stopwords, stemming

def home_page():

    # Create columns for main area and sidebar
    main_col, sidebar_col = st.columns([3, 1], gap="large")

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
            # Placeholder for search logic
            songs = get_top_songs_from_genius(search_query)
            results_placeholder.write(f"Showing results for: **{search_query}**")
            results_placeholder.write(songs)
        else:
            results_placeholder.write("No results to display.")

    with sidebar_col:
        st.markdown("### Filters & Settings")
        # Example sliders/filters/settings
        slider_val = st.slider("Select a value", 0, 100, 50)
        filter_option = st.selectbox("Choose a filter", ["All", "Option 1", "Option 2"])
        st.checkbox("Enable advanced settings")
        st.markdown("---")
        st.write(f"Slider value: {slider_val}")
        st.write(f"Filter: {filter_option}")
