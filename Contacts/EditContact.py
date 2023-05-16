import datetime
from typing import Dict, Any
from time import sleep

import pandas as pd
import streamlit as st

import Database.config as config
from Database.MySQLConnection import my_sql_connection


# Define a function to edit a contact
def edit_contact(**contact_data: Dict[str, Any]) -> None:
    # Open a connection to the MySQL database
    with my_sql_connection() as c:
        # Generate the SET clause of the SQL query to update the contact
        set_clause = ", ".join([f"{key}=%s" for key in contact_data])
        # Generate the complete SQL query to update the contact
        query = f"UPDATE {config.db_name}.contacts SET {set_clause} WHERE id=%s"
        # Generate the tuple of values to be passed to the SQL query
        values = tuple(contact_data.values()) + (contact_data['id'],)
        # Execute the SQL query to update the contact
        c.execute(query, values)


def choose_contact_selectbox(user_id: int, key: str) -> int:
    # Open a connection to the MySQL database
    with my_sql_connection() as c:
        # Generate the SQL query to fetch the contacts for the specified user
        c.execute(
            f"SELECT c.id, CONCAT(c.first_name, ' ', c.last_name, ' - ', c.circumstance_met) "
            f"FROM {config.db_name}.contacts c "
            f"JOIN {config.db_name}.users u ON u.id = c.user_id "
            "WHERE u.id = %s", [user_id]
        )
        # Fetch all contacts for the specified user
        contacts = c.fetchall()
        # If no contacts are found, display a message and return 0
        if not contacts:
            return 0
        # Create a dictionary that maps contact names to contact IDs
        contact_dict = {contact[1]: contact[0] for contact in contacts}
        # Display a selectbox for the user to choose a contact from the list
        selected_contact = st.selectbox("Select a contact", list(contact_dict.keys()), key=key)
        # Return the ID of the selected contact
        return contact_dict[selected_contact]


def delete_contact(contact_id: int) -> None:
    # Open a connection to the MySQL database
    with my_sql_connection() as c:
        # Generate the SQL query to delete the specified contact
        c.execute(f"DELETE FROM {config.db_name}.contacts WHERE id = %s", [contact_id])


def delete_contact_button(contact_id: int, key: str) -> None:
    # Display a button to delete the specified contact
    if st.button("Delete", key=key, use_container_width=True):
        # Call the delete_contact function to delete the specified contact
        delete_contact(contact_id)
        # Display a success message
        st.success("Contact deleted!")
        sleep(1)
        # Rerun the app to update the list of contacts
        st.experimental_rerun()


def edit_contact_form(user_id: int, contact_id: int) -> None:
    # Open a connection to the MySQL database and fetch the data for the specified contact
    with my_sql_connection() as c:
        c.execute(f"SELECT * FROM {config.db_name}.contacts WHERE id=%s", [contact_id])
        contact_data = c.fetchone()
        
    if contact_data is not None:

        # Create a form to edit the contact's information
        with st.form(key='edit-contact-form'):
            # Create three columns for the first name, last name, and birthday fields
            col1, col2, col3 = st.columns(3)
            with col1:
                first_name = st.text_input("First Name*", value=contact_data[2])
            with col2:
                last_name = st.text_input("Last Name*", value=contact_data[3])
            with col3:
                # Create a date input field for the birthday
                birthday = st.date_input("Birthday", value=pd.to_datetime(contact_data[4]), min_value=pd.to_datetime('1950-01-01'))

            # Create three columns for the nationality, current occupation, and partner name fields
            col1, col2, col3 = st.columns(3)
            with col1:
                nationality = st.text_input("Nationality", value=contact_data[5])
            with col2:
                current_occupation = st.text_input("Current Occupation", value=contact_data[6])
            with col3:
                partner_name = st.text_input("Partner Name", value=contact_data[7])

            # Create two columns for the year met and circumstance met fields
            col1, col2 = st.columns(2)
            years = range(2001, datetime.datetime.now().year + 1)
            with col1:
                # Create a selectbox for the year met field
                year_met = st.selectbox("Year Met*", options=years, index=years.index(contact_data[8]))
            with col2:
                # Create a text input field for the circumstance met field
                circumstance_met = st.text_input("Circumstance Met*", value=contact_data[9])

            # Create two columns for the city met and country met fields
            col1, col2 = st.columns(2)
            with col1:
                city_met = st.text_input("City Met*", value=contact_data[10])
            with col2:
                country_met = st.text_input("Country Met*", value=contact_data[11])

            # Create text input fields for the interests and talking points fields
            interests = st.text_input("Interests", value=contact_data[12])
            talking_points = st.text_input("Talking Points", value=contact_data[13])

            # If the "Update Contact" button is pressed, update the contact's information in the database and display a success message
            if st.form_submit_button("Update Contact"):
                contact_data = {
                    'id': contact_id,
                    'first_name': first_name,
                    'last_name': last_name,
                    'birthday': birthday,
                    'nationality': nationality,
                    'current_occupation': current_occupation,
                    'partner_name': partner_name,
                    'circumstance_met': circumstance_met,
                    'year_met': year_met,
                    'city_met': city_met,
                    'country_met': country_met,
                    'interests': interests,
                    'talking_points': talking_points
                }
                edit_contact(**contact_data)
                st.success("Contact updated!")
                sleep(1)
                st.experimental_rerun()