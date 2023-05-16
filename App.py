import streamlit as st
from streamlit_option_menu import option_menu

from UserAccount.Authentication import authentication

from HomePage.Overview import overview
from HomePage.ContactPages import contact_pages

def app():
    # Set the page configuration
    st.set_page_config(
    page_title="Personal CRM",
    page_icon="📖",
    #layout="wide",
    #initial_sidebar_state="expanded",
    menu_items={
    #     'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "mailto:vasco.oliveira260@gmail.com?subject=Personal CRM - Bug Report",
    #     'About': "# This is a header. This is an *extremely* cool app!"
    }
    )
    
    # Set the initial session state variable to False
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = True # Change to False to activate login functionality

    # If the user is not logged in, show the login page
    if not st.session_state.authenticated:
        authentication()
        
    # If the user is logged in, show the main page
    if st.session_state.authenticated:
        st.session_state.user_id = 1 # Delete to activate login functionality

        selected = option_menu(
            menu_title = None,
            options = ['Overview', 'Contact Pages'],
            icons = ['house', 'book'],
            menu_icon = 'cast',
            default_index = 0,
            orientation = 'horizontal'
        )

        if selected == 'Overview':
            overview(st.session_state.user_id)
            # overview(1)
        if selected == 'Contact Pages':
            contact_pages(st.session_state.user_id)
            # contact_pages(1)
        
if __name__ == "__main__":
    app()