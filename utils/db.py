import sqlite3
import pandas as pd
import streamlit as st

@st.cache_resource
def get_connection():
    conn = sqlite3.connect("file:/data/data.db?mode=ro", uri=True, check_same_thread=False)
    return conn
