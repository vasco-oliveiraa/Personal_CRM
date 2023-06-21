import streamlit as st
from streamlit_option_menu import option_menu
import threading

from UserAccount.Authentication import authentication

from HomePage.Overview import overview
from HomePage.ContactPages import contact_pages
from HomePage.Account import account

from Reminders.Scheduler import schedule_reminders, schedule_birthday_reminders

def app():
    # Set the page configuration
    st.set_page_config(
    page_title="Sau",
    page_icon="✉️",
    #layout="wide",
    #initial_sidebar_state="expanded",
    menu_items={
    #     'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "mailto:vasco.oliveira260@gmail.com?subject=Personal CRM - Bug Report",
    #     'About': "# This is a header. This is an *extremely* cool app!"
    }
    )
    
    params = st.experimental_get_query_params()
    auth_param = params.get('auth', [''])[0]

    if auth_param == '':
        st.experimental_set_query_params(auth='False')
        authentication()
    elif auth_param == 'False':
        authentication()
    elif auth_param == 'True':

        selected = option_menu(
            menu_title = None,
            options = ['Overview', 'Contact Pages', 'Account'],
            icons = ['house', 'book', 'person'],
            menu_icon = 'cast',
            default_index = 0,
            orientation = 'horizontal'
        )

        if selected == 'Overview':
            overview(st.experimental_get_query_params()['user'][0])
        if selected == 'Contact Pages':
            contact_pages(st.experimental_get_query_params()['user'][0])
        if selected == 'Account':
            account(st.experimental_get_query_params()['user'][0])
            
    # Create a separate thread to run the reminders scheduler
#     reminder_scheduler_thread = threading.Thread(target=schedule_reminders)
#     reminder_scheduler_thread.start()
    
#     birthday_scheduler_thread = threading.Thread(target=schedule_birthday_reminders)
#     birthday_scheduler_thread.start()
        
if __name__ == "__main__":
    app()