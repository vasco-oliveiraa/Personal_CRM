import streamlit as st
import pandas as pd
from time import sleep, strftime

from Database.MySQLConnection import my_sql_connection
import Database.config as config

# from Interactions.AudioRecorder import record_audio

from Contacts.EditContact import choose_contact_selectbox

# Define a function to add a new contact
def add_interaction(interaction_info):
    with my_sql_connection() as c:
        c.execute(f"INSERT INTO {config.db_name}.interactions (contact_id, interaction_title, interaction_date, notes) VALUES (%s, %s, %s, %s)", interaction_info)

# Page where interaction information is added
def add_interaction_form(user_id: int, contact_id: int, key:str) -> None:
    
    tab1, tab2 = st.tabs(['Written', 'Recorded'])
    
    with tab1:
        
        with st.form(key='add-interaction-form-written',clear_on_submit=True):

            col1, col2 = st.columns(2)

            with col1:
                title = st.text_input("Title*")

            with col2:
                date = st.date_input("Date*", min_value=pd.to_datetime('2001-05-26'))

            written_notes = st.text_input("Notes*")

            if st.form_submit_button("Add Interaction"):
                interaction_info = (contact_id, title, date, written_notes)
                add_interaction(interaction_info)
                st.success("Interaction added!")
                sleep(1)
                st.experimental_rerun()
        
#     with tab2:
        
#         with st.form(key='add-interaction-form-recorded',clear_on_submit=True):
            
#             col1, col2 = st.columns(2)

#             with col1:
#                 title = st.text_input("Title*")

#             with col2:
#                 date = st.date_input("Date*", min_value=pd.to_datetime('2001-05-26'))

#             duration = st.slider("Select recording duration", 0, 60, 30, 5)

#             if st.form_submit_button("Start Recording"):
#                 timestr = strftime("%Y-%m-%d - %H-%M-%S")
#                 filename = f"{contact_id} - {timestr}"
#                 recorded_notes = record_audio(duration, filename)

#                 interaction_info = (contact_id, title, date, recorded_notes)
#                 add_interaction(interaction_info)
#                 st.success("Interaction added!")
#                 sleep(1)
#                 st.experimental_rerun()