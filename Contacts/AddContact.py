import streamlit as st
import datetime
import pandas as pd
from time import sleep

from Database.MySQLConnection import my_sql_connection
import Database.config as config

# Define a function to add a new contact
def add_contact(contact_info):
    with my_sql_connection() as c:
        c.execute(f"INSERT INTO {config.db_name}.contacts (user_id, first_name, last_name, birthday, nationality, current_occupation, partner_name, circumstance_met, year_met, city_met, country_met, interests, talking_points) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", contact_info)

# Page where contact information is added
def add_contact_form(user_id):
    with st.form(key='add-contact-form',clear_on_submit=False):
    
        col1, col2, col3 = st.columns(3)

        with col1:
            first_name = st.text_input("First Name*") 
        with col2:
            last_name = st.text_input("Last Name*")
        with col3:
            birthday = st.date_input("Birthday",min_value=pd.to_datetime('1950-01-01'))
            
        col1, col2, col3 = st.columns(3)
        
        with col1:
            nationality = st.text_input("Nationality")
        with col2:
            current_occupation = st.text_input("Current Occupation")
        with col3:
            partner_name = st.text_input("Partner Name")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Define a list of all years since my birth until now
            years = range(2001, datetime.datetime.now().year + 1)
            year_met = st.selectbox("Year Met*", options=years)
            
        with col2:
            circumstance_met = st.text_input("Circumstance Met*")
            
        col1, col2 = st.columns(2)
        
        with col1:
            city_met = st.text_input("City Met*")
        with col2:
            country_met = st.text_input("Country Met*")

        interests = st.text_input("Interests")
        talking_points = st.text_input("Talking Points")

        # Submit button
        submit = st.form_submit_button("Add Contact")
        if submit:
            if any(var == '' for var in [first_name, last_name, year_met, circumstance_met, city_met, country_met]):
                    st.error("Please fill all mandatory fields (*)")
            else:
                contact_info = (user_id, first_name, last_name, birthday, nationality, current_occupation, partner_name, circumstance_met, year_met, city_met, country_met, interests, talking_points)
                add_contact(contact_info)
                st.success("Contact added!")
                sleep(1)
                st.experimental_rerun()
                # Next step is to figure out how to reset the form without having to reload the page.
                # Using the default clear_on_submit from the form doesn't work, because it clears everytime you try, and sometimes users will try without filling all the necessary fields.