import streamlit as st
st.set_page_config(page_icon=":material/robot_2:",layout="wide",page_title="TechWillxGame",menu_items={"About":"https://github.com/aakash-test7/"},initial_sidebar_state="collapsed")
from streamlit_navigation_bar import st_navbar
import pages as pg
from pages.security_login import update_visitor_count
st.logo("logo.gif")
st.markdown("""
            <style>
            .stLogo {
                width: 48px;
                height: 48px;
            }
            </style>
            """, unsafe_allow_html=True)
pages = ["Home", "Recommend", "Tutorial", "About","Aakash"]
logo_path = ("logo.svg")
urls = {"Aakash": "https://linkedin.com/in/aakash-kharb/"}
options={"use_padding": False, "show_menu":False}

styles = {
    "nav": {
        "background-color": "rgba(75, 156, 211,0)",  # Background color of the navigation bar
        "height": "4rem",  # Set the total height of the navigation bar
        "display": "flex",  # Use flexbox for layout
        "align-items": "center",  # Vertically center the items
        "justify-content": "space-around",  # Spread out the headings evenly
        "padding": "0 1rem",  # Add padding to the left and right of the navigation bar
        "overflow-x": "auto",  # Enable horizontal scrolling if the content overflows
        "white-space": "nowrap",  # Prevent items from wrapping to a new line
    },
    "div": {
        "max-width": "72rem",  # Limit the maximum width of the navigation bar content
    },
    "span": {
        "border-radius": "0.5rem",  # Rounded corners for the headings
        "color": "rgb(49, 51, 63)",  # Text color of the headings
        "margin": "0 0.125rem",  # Margin around each heading
        "padding": "0.4375rem 0.625rem",  # Padding inside each heading
        "font-size": "1.1rem",  # Increase the font size of the headings
        "font-weight": "bold",  # Make the headings bold
        "text-transform": "uppercase",  # Convert heading text to uppercase
    },
    "active": {
        "background-color": "rgba(173, 216, 230, 0.5)",  # Light blue background for the active state
    },
    "hover": {
        "background-color": "rgba(173, 216, 230, 0.3)",
    },
    "img": {  # This targets the logo image specifically
            "width": "50px",  # You can increase or decrease this as needed
            "height": "50px"  # Adjust the height to match the width
        }
}

# Inject custom CSS for mobile responsiveness
st.markdown("""
    <style>
        /* Mobile responsiveness */
        @media (max-width: 900px) {
            .stNavBar-nav {
                overflow-x: scroll;  /* Enable scrolling on smaller screens */
                flex-wrap: nowrap;    /* Prevent wrapping of items */
                padding: 0.5rem;      /* Adjust padding for mobile */
            }
            .stNavBar-span {
                font-size: 0.9rem;      /* Slightly reduce font size for mobile */
            }
        }
    </style>
""", unsafe_allow_html=True)
st.markdown("""<style>.stApp {padding-top: 6rem !important;}</style>""", unsafe_allow_html=True)
if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"  # Default to Home page on first load
page = st_navbar(pages, logo_path=logo_path, urls=urls, styles=styles, options=options)
if page != st.session_state.current_page:
    st.session_state.current_page = page
#st.sidebar.markdown("---")  # Adds a separator
st.markdown("""
    <style>
        /* Change the background color of the sidebar */
        .stSidebar {
            background-color: #4b9cd3 !important;  /* Set the background to a light blue */
        }
    </style>
""", unsafe_allow_html=True)

#visitor
if 'first_access' not in st.session_state:
    st.session_state.first_access = True
if 'visitor_count' not in st.session_state:
    st.session_state.visitor_count = 0
if 'display_count' not in st.session_state:
    st.session_state.display_count = True

if st.session_state.first_access:
    st.session_state.visitor_count = update_visitor_count()

if st.session_state.display_count:
    st.toast(f"Visitor Count : {st.session_state.visitor_count}")
    st.session_state.display_count = False

if st.sidebar.button("Site Stats",use_container_width=True):
    visitor_count = update_visitor_count()
    st.sidebar.subheader(f"Total Visitors : {visitor_count}")
    st.toast(f"Total visitors: {visitor_count}")

def open_link(url):
    st.components.v1.html(f'<script>window.open("{url}", "_blank");</script>', height=0)

if st.sidebar.button("Github", key="1button1", use_container_width=True):
    open_link("https://github.com/aakash-test7/")

if st.sidebar.button("Youtube", key="1button2", use_container_width=True):
    open_link("https://youtube.com/@aakash5069")

if st.sidebar.button("Linkedin", key="1button3", use_container_width=True):
    open_link("https://linkedin.com/in/aakash-kharb")

if st.sidebar.button("X / Twitter", key="1button4", use_container_width=True):
    open_link("https://x.com/aakash_kharb")

functions = {
    "Home": pg.home_page,
    "Recommend": pg.recommend_page,
    "Tutorial": pg.tutorial_page,
    "About": pg.about_page,
}

go_to = functions.get(st.session_state.current_page)
if go_to:
    go_to()
