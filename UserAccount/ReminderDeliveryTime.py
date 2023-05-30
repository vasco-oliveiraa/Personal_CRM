import streamlit as st
import datetime

from Database.MySQLConnection import my_sql_connection
import Database.config as config

def reminder_delivery_time(user_id):
    with my_sql_connection() as c:
        c.execute(f'SELECT reminder_delivery_time FROM {config.db_name}.users WHERE id=%s',(user_id,))
        return c.fetchone()[0]

def edit_reminder_delivery_time(user_id, time):
    with my_sql_connection() as c:
        c.execute(f'UPDATE {config.db_name}.users SET reminder_delivery_time = %s WHERE id=%s',(time, user_id,))