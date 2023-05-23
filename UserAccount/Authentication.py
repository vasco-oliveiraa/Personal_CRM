from Database.MySQLConnection import my_sql_connection
import Database.config as config

import streamlit as st
import time
import bcrypt

def login(email, password, signup=False):
    with my_sql_connection() as c:
        c.execute(f'SELECT id, first_name, last_name, hashed_password FROM {config.db_name}.users WHERE email = %s', [email])
        result = c.fetchone()
        if result is not None:
            hashed_password = result[-1].encode()
            encoded_password = password.encode()
            if bcrypt.checkpw(encoded_password, hashed_password):
                
                st.experimental_set_query_params(
                    auth='True',
                    user=[result[0]],
                )
                if signup == True:
                    pass
                else:
                    st.success(f"Welcome back {result[1]+' '+result[2]}")
                    time.sleep(1)
                st.experimental_rerun()

            else:
                st.error("Incorrect password")
        else:
            st.error("Email not registered")
        
def signup(first_name, last_name, email, password, confirm_password):
    if password == confirm_password:
        with my_sql_connection() as c:
            c.execute(f"SELECT * FROM {config.db_name}.users WHERE email = %s", [email])
            user = c.fetchone()
            if user is not None:
                st.error("Email already registered")
            else:
                # Hash the password before storing it in the database
                encoded_password = password.encode()
                salt = bcrypt.gensalt()
                hashed_password = bcrypt.hashpw(encoded_password, salt)

                c.execute(f"INSERT INTO {config.db_name}.users (first_name, last_name, email, hashed_password) VALUES (%s, %s, %s, %s)", [first_name, last_name, email, hashed_password])
                st.success("Account created")
                time.sleep(2)
                
        if user is None:
            login(email, password, signup=True)
    else:
        st.error("Passwords do not match")

# Create a signup function
def authentication():
    # Add a title
    st.title("✉️ Sau")

    tab1, tab2 = st.tabs(["Log In","Sign Up"])

    with tab1:

        with st.form(key='log-in-form',clear_on_submit=False):

            email = st.text_input("Email")
            password = st.text_input("Password", type="password")

            # Check if the username and password are valid
            if st.form_submit_button("Log In"):
                login(email, password)

    with tab2:

        with st.form(key='sign-up-form',clear_on_submit=False):

            # Create input fields for the username and password
            col1, col2 = st.columns(2)

            with col1:
                first_name = st.text_input("First Name")

            with col2:
                last_name = st.text_input("Last Name")

            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")

            # Check if the new username is available and add the user to the database
            if st.form_submit_button("Sign Up"):
                signup(first_name, last_name, email, password, confirm_password)
                            