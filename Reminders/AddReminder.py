import streamlit as st
from datetime import datetime
from time import sleep

from Database.MySQLConnection import my_sql_connection
import Database.config as config

from Interactions.EditInteraction import choose_interaction_selectbox

# Define a function to add a new contact
def add_reminder(reminder_info):
    with my_sql_connection() as c:
        c.execute(f"INSERT INTO {config.db_name}.reminders (contact_id, interaction_id, reminder_title, reminder_actual_date, reminder_message) VALUES (%s, %s, %s, %s, %s)", reminder_info)

# Page where reminder information is added
def add_reminder_form(contact_id: int) -> None:
    
    # Connect to existing interaction
    if st.checkbox("Connect to interaction", key='connect-an-interaction-checkbox-add-reminder-form'):
        interaction_id = choose_interaction_selectbox(contact_id, key='choose-interaction-selectbox-add-reminder-form')
        if interaction_id == 0:
            st.write('No interactions found.')
    else:
        interaction_id = 0
        
    with st.form(key='add-reminder-form',clear_on_submit=True):

        col1, col2 = st.columns(2)

        with col1:
            title = st.text_input("Title*")

        with col2:
            date = st.date_input("Date*", min_value=datetime.now().date())

        message = st.text_input("Message*")
        
        if st.form_submit_button("Add Reminder"):
            reminder_info = (contact_id, interaction_id, title, date, message)
            add_reminder(reminder_info)
            st.success("Reminder added!")
            sleep(1)
            st.experimental_rerun()