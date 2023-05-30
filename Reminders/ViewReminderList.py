import pandas as pd
import streamlit as st

from Database.MySQLConnection import my_sql_connection
import Database.config as config

def view_reminder_list(user_id):
    with my_sql_connection() as c:
        c.execute(f'''
            SELECT
                r.reminder_title Title,
                r.reminder_actual_date Date,
                CONCAT(c.first_name, ' ', c.last_name) Contact
            FROM
                {config.db_name}.reminders r
            JOIN
                {config.db_name}.contacts c ON c.id = r.contact_id
            JOIN
                {config.db_name}.users u ON u.id = c.user_id
            WHERE
                u.id = %s
        ''', [user_id])
        
        rows = c.fetchall()
        # Get the column names from cursor.description
        columns = [desc[0] for desc in c.description]
        # Create a DataFrame from the rows
        df = pd.DataFrame(rows, columns=columns)
        # Set id as the index
        df.set_index(["Title","Date"], inplace=True)
        # Write the DataFrame to the streamlit app
        st.dataframe(df, use_container_width=True)