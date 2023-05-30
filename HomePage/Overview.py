import streamlit as st
import datetime
import time

from Contacts.ViewContactList import view_contact_list
from Contacts.AddContact import add_contact_form
from Contacts.EditContact import edit_contact_form, choose_contact_selectbox, delete_contact_button

from Interactions.ViewInteractionList import view_interaction_list
from Interactions.AddInteraction import add_interaction_form
from Interactions.EditInteraction import edit_interaction_form, choose_interaction_selectbox, delete_interaction_button

from Reminders.ViewReminderList import view_reminder_list
from Reminders.AddReminder import add_reminder_form
from Reminders.EditReminder import edit_reminder_form, choose_reminder_selectbox, delete_reminder_button

from Reminders.Scheduler import check_reminders

from UserAccount.ReminderDeliveryTime import reminder_delivery_time

def overview(user_id):
    
    st.title("✉️ Sau")

    tab1, tab2, tab3 = st.tabs(["View Contacts","Add New Contact","Edit Contact"])

    with tab1:
        view_contact_list(user_id)

    with tab2:
        add_contact_form(user_id)

    with tab3:
        col1, col2 = st.columns([8,1])
        with col1:
            contact_id = choose_contact_selectbox(user_id, key='choose-contact-selectbox-edit-contact-form-overview')
        if contact_id == 0:
            st.write('No contacts found.')
        else:
            with col2:
                st.write(' ')
                st.write(' ')
                delete_contact_button(contact_id, key='delete-contact-edit-contact-form-overview')
            edit_contact_form(user_id, contact_id = contact_id)

    tab1, tab2, tab3 = st.tabs(["View Interactions", "Add New Interaction", "Edit Interaction"])

    with tab1:
        view_interaction_list(user_id)

    with tab2:
        contact_id = choose_contact_selectbox(user_id, key='choose-contact-selectbox-add-interaction-form-overview')
        if contact_id == 0:
            st.write('No contacts found.')
        else:
            add_interaction_form(user_id, contact_id = contact_id, key='add-interaction-form-overview')

    with tab3:
        contact_id = choose_contact_selectbox(user_id, key='choose-contact-selectbox-edit-interaction-form-overview')
        if contact_id == 0:
            st.write('No contacts found.')
        else:
            col1, col2 = st.columns([8,1])
            with col1:
                interaction_id = choose_interaction_selectbox(contact_id, key='choose-interaction-selectbox-edit-interaction-form-overview')
            if interaction_id == 0:
                st.write('No interactions found.')
            else:
                with col2:
                    st.write(' ')
                    st.write(' ')
                    delete_interaction_button(interaction_id, key='delete-interaction-edit-interaction-form-overview')
                edit_interaction_form(contact_id, interaction_id = interaction_id)
                
    # Check if reminder_delivery_time is set
    
    if reminder_delivery_time(user_id) is not None:
        
        tab1, tab2, tab3 = st.tabs(["View Reminders", "Add New Reminder", "Edit Reminder"])
        with tab1:
            view_reminder_list(user_id)

        with tab2:
            contact_id = choose_contact_selectbox(user_id, key='choose-contact-selectbox-add-reminder-form-overview')
            if contact_id == 0:
                st.write('No contacts found.')
            else:
                add_reminder_form(contact_id)

        with tab3:
            contact_id = choose_contact_selectbox(user_id, key='choose-contact-selectbox-edit-reminder-form-overview')
            if contact_id == 0:
                st.write('No contacts found.')
            else:
                col1, col2 = st.columns([8,1])
                with col1:
                    reminder_id = choose_reminder_selectbox(contact_id, key='choose-reminder-selectbox-edit-reminder-form-overview')
                if reminder_id == 0:
                    st.write('No reminders found.')
                else:
                    with col2:
                        st.write(' ')
                        st.write(' ')
                        delete_reminder_button(reminder_id, key='delete-reminder-edit-reminder-form-overview')
                    edit_reminder_form(contact_id, reminder_id = reminder_id)
    else:
        col1, col2 = st.columns([7,1])
        
        with col1:
            t = st.time_input('Reminders Notification Time', datetime.time(0,30), step=1800).strftime("%H:%M:%S")

        with col2:
            st.write(' ')
            st.write(' ')
            if st.button('Submit'):
                edit_reminder_delivery_time(user_id, time=t)
                st.success(f'Success!')
                time.sleep(1)
                st.experimental_rerun()
                
    