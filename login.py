import streamlit as st

def login_page():
    """
    Render the log in page
    """
    st.markdown("<h1>Welcome to the Music Engine</h1>", unsafe_allow_html=True)
    st.markdown("### Please log in to continue")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    VALID_CREDENTIALS = {"admin": "admin123", "user": "user123"}
    if st.button("Login"):
        if username in VALID_CREDENTIALS and password == VALID_CREDENTIALS[username]:
            st.session_state["logged_in"] = True
            st.success("Login successful!")
            st.rerun()  # Refresh the app
        else:
            st.error("Incorrect username or password")