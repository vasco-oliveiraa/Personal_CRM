import streamlit as st
import pandas as pd
from time import sleep
from Database.MySQLConnection import my_sql_connection
import Database.config as config
from Contacts.EditContact import choose_contact_selectbox


def edit_interaction(**interaction_data):
    # Update interaction data in the MySQL database.
    with my_sql_connection() as c:
        set_clause = ", ".join([f"{key}=%s" for key in interaction_data])
        query = f"UPDATE {config.db_name}.interactions SET {set_clause} WHERE id=%s"
        values = tuple(interaction_data.values()) + (interaction_data['id'],)
        c.execute(query, values)

def delete_interaction(interaction_id):
    # Delete an interaction from the MySQL database.
    with my_sql_connection() as c:
        # Use parameterized queries to avoid SQL injection vulnerabilities.
        c.execute(f"DELETE FROM {config.db_name}.interactions WHERE id = %s", (interaction_id,))
    
def delete_interaction_button(interaction_id, key):
    # Creates a 'Delete' button for deleting an interaction.
    if st.button("Delete", key=key, use_container_width=True):
        delete_interaction(interaction_id)
        st.success("Interaction deleted!")
        sleep(1)
        st.experimental_rerun()
        
def choose_interaction_selectbox(contact_id, key):
    with my_sql_connection() as c:
        # Get the interactions for the selected contact
        c.execute(f"SELECT i.id, CONCAT(i.interaction_title, ' - ', i.interaction_date) FROM {config.db_name}.interactions i JOIN {config.db_name}.contacts c ON i.contact_id = c.id WHERE c.id = {contact_id}")
        interactions = c.fetchall()
        if not interactions:
            return 0
        interaction_dict = {interaction[1]: interaction[0] for interaction in interactions}

        # Select the interaction to edit
        selected_interaction_str = st.selectbox("Select an interaction", list(interaction_dict.keys()), key=key)
        interaction_id = interaction_dict[selected_interaction_str]
        
    return interaction_id
    

def edit_interaction_form(contact_id, interaction_id):
    """
    Displays a form to edit an interaction and updates the interaction in the database.

    Args:
        contact_id (int): The ID of the contact whose interaction is being edited.
        interaction_id (int): The ID of the interaction which is being edited.

    Returns:
        None.
    """
    with my_sql_connection() as c:

        # Get the interaction data from the database
        c.execute(f"SELECT * FROM {config.db_name}.interactions WHERE id={interaction_id}")
        interaction_data = c.fetchone()

        with st.form(key='edit-interaction-form',clear_on_submit=False):

            col1, col2 = st.columns(2)

            with col1:
                title = st.text_input("Title*",value=interaction_data[2])
            with col2:
                date = st.date_input("Date*",value=pd.to_datetime(interaction_data[3]), min_value=pd.to_datetime('2001-05-26'))

            notes = st.text_input("Notes*", value=interaction_data[4])

            # Submit button
            submit = st.form_submit_button("Edit Interaction")
            if submit:
                if any(var == '' for var in [title, notes]):
                        st.error("Please fill all mandatory fields (*)")
                else:
                    interaction_data = {
                        'id' : interaction_id,
                        'contact_id' : contact_id,
                        'interaction_title' : title,
                        'interaction_date' : date,
                        'notes' : notes
                    }
                    edit_interaction(**interaction_data)
                    st.success("Interaction updated!")
                    sleep(1)
                    st.experimental_rerun()