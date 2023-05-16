import streamlit as st
import pandas as pd
import datetime

from Database.MySQLConnection import my_sql_connection
import Database.config as config

from Contacts.EditContact import edit_contact_form, choose_contact_selectbox, delete_contact_button

from Interactions.AddInteraction import add_interaction_form
from Interactions.EditInteraction import edit_interaction_form, choose_interaction_selectbox, delete_interaction_button

from Reminders.AddReminder import add_reminder_form
from Reminders.EditReminder import edit_reminder_form, choose_reminder_selectbox, delete_reminder_button

def contact_pages(user_id):
    
    col1, col2 = st.columns([8,1])
    
    with col1:

        contact_id = choose_contact_selectbox(user_id, key='choose-contact-contact-pages')
    if contact_id == 0:
        st.write('No contacts found.')
    else:
        with col2:
            st.write(' ')
            st.write(' ')
            delete_contact_button(contact_id, key='delete-contact-button-contact-pages')

        # Contact Information
    
        with st.expander('Contact Information'):

            edit_contact_form(user_id, contact_id = contact_id)
                
        # Interactions

        with st.expander('Interactions'):

            tab1, tab2 = st.tabs(['Add Interaction', 'Edit Interaction'])

            with tab1:
                add_interaction_form(user_id, contact_id = contact_id, key='add-interaction-form-contact-pages')

            with tab2:
                
                col1, col2 = st.columns([7,1])
    
                with col1:

                    interaction_id = choose_interaction_selectbox(contact_id, key='choose-interaction-selectbox-edit-interaction-form-contact-pages')
                if interaction_id == 0:
                    st.write('No interactions found.')
                else:
                    with col2:
                        st.write(' ')
                        st.write(' ')
                        delete_interaction_button(contact_id, key='delete-interaction-button-contact-pages')
                    edit_interaction_form(contact_id, interaction_id = interaction_id)
                    
        # Reminders
        with st.expander('Reminders'):
            tab1, tab2 = st.tabs(['Add Reminder', 'Edit Reminder'])
            with tab1:
                add_reminder_form(contact_id)

            with tab2:

                col1, col2 = st.columns([7,1])

                with col1:

                    reminder_id = choose_reminder_selectbox(contact_id, key='choose-reminder-selectbox-edit-reminder-form-contact-pages')
                if interaction_id == 0:
                    st.write('No reminders found.')
                else:
                    with col2:
                        st.write(' ')
                        st.write(' ')
                        delete_reminder_button(contact_id, key='delete-reminder-button-contact-pages')
                    edit_reminder_form(contact_id, reminder_id = reminder_id)