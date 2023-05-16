import streamlit as st
import pandas as pd
from time import sleep

from Database.MySQLConnection import my_sql_connection
import Database.config as config

from Interactions.EditInteraction import choose_interaction_selectbox

# Define a function to edit a contact
def edit_reminder(**reminder_data):
    with my_sql_connection() as c:
        set_clause = ", ".join([f"{key}=%s" for key in reminder_data])
        query = f"UPDATE {config.db_name}.reminders SET {set_clause} WHERE id=%s"
        values = tuple(reminder_data.values()) + (reminder_data['id'],)
        c.execute(query, values)
        
def delete_reminder(reminder_id):
    with my_sql_connection() as c:
        c.execute(f"DELETE FROM {config.db_name}.reminders WHERE id = {reminder_id}")
        
def delete_reminder_button(reminder_id, key):
    # Creates a 'Delete' button for deleting an reminders.
    if st.button("Delete", key=key, use_container_width=True):
        delete_reminder(reminder_id)
        st.success("Reminder deleted!")
        sleep(1)
        st.experimental_rerun()
        
def choose_reminder_selectbox(contact_id, key):
    with my_sql_connection() as c:
        # Get the reminders for the selected contact
        c.execute(f"SELECT r.id, CONCAT(r.reminder_title, ' - ', r.reminder_actual_date) FROM {config.db_name}.reminders r "
                  f"JOIN {config.db_name}.contacts c ON r.contact_id = c.id WHERE c.id = {contact_id}")
        reminders = c.fetchall()
        if not reminders:
            return 0
        reminder_dict = {reminder[1]: reminder[0] for reminder in reminders}

        # Select the reminder to edit
        selected_reminder_str = st.selectbox("Select a reminder", list(reminder_dict.keys()), key=key)
        reminder_id = reminder_dict[selected_reminder_str]
        
    return reminder_id

def edit_reminder_form(contact_id, reminder_id):
    """
    Displays a form to edit a reminder and updates the reminder in the database.

    Args:
        contact_id (int): The ID of the contact whose reminder is being edited.
        reminder_id (int): The ID of the reminder which is being edited.

    Returns:
        None.
    """
    with my_sql_connection() as c:

        # Get the reminder data from the database
        c.execute(f"SELECT * FROM {config.db_name}.reminders WHERE id={reminder_id}")
        reminder_data = c.fetchone()
        
         # Connect to existing interaction
        if st.checkbox("Connect to interaction", key='connect-an-interaction-checkbox-edit-reminder-form'):
            interaction_id = choose_interaction_selectbox(contact_id, key='choose-interaction-selectbox-edit-reminder-form')
            if interaction_id == 0:
                st.write('No interactions found.')
        else:
            interaction_id = 0

        with st.form(key='edit-reminder-form',clear_on_submit=False):

            col1, col2 = st.columns(2)

            with col1:
                title = st.text_input("Title*",value=reminder_data[3])
            with col2:
                date = st.date_input("Date*",value=pd.to_datetime(reminder_data[4])) #min_value=pd.datetime.now().date())

            message = st.text_input("Notes*", value=reminder_data[5])

            # Submit button
            submit = st.form_submit_button("Edit Reminder")
            if submit:
                if any(var == '' for var in [title, message]):
                        st.error("Please fill all mandatory fields (*)")
                else:
                    reminder_data = {
                        'id' : reminder_id,
                        'contact_id' : contact_id,
                        'interaction_id' : interaction_id,
                        'reminder_title' : title,
                        'reminder_actual_date' : date,
                        'reminder_message' : message
                    }
                    edit_reminder(**reminder_data)
                    st.success("Reminder updated!")
                    sleep(1)
                    st.experimental_rerun()