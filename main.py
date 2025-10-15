import streamlit as st
from pages.home_page import home_page
from streamlit_option_menu import option_menu
from login import login_page

st.cache_data.clear()
st.cache_resource.clear()

st.set_page_config(
    page_title= "Music Search Engine", 
    layout="wide",
)

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    login_page() 
    st.stop()

with st.sidebar:
    selected = option_menu(
        menu_title="Menu", 
        options=["Home Page"],
        menu_icon="cast", 
        default_index=0,
        styles={
            "container": {"padding": "5!important",},
            "icon": {"font-size": "18px"},
            "nav-link": {
                "font-size": "14px",
                "text-align": "left",
                "margin": "0px",
                "letter-spacing": "0px"
            },
        }
    )
    if st.button("Logout"):
        st.session_state["logged_in"] = False
        st.rerun()
if selected == "Home Page":
    home_page()