import streamlit as st
import datetime
import time

from UserAccount.ReminderDeliveryTime import reminder_delivery_time, edit_reminder_delivery_time

def account(user_id):
    # Change Password
    
    # Change Reminder Delivery Time
    reminder_timedelta = reminder_delivery_time(user_id)
    reminder_datetime = reminder_timedelta + datetime.datetime.min
    reminder_time = reminder_datetime.time()
    col1, col2 = st.columns([7,1])

    with col1:
        if reminder_time is None:
            t = st.time_input('Reminders Notification Time', datetime.time(0,30), step=1800).strftime("%H:%M:%S")
        else:
            t = st.time_input('Reminders Notification Time', reminder_time, step=1800).strftime("%H:%M:%S") 

    with col2:
        st.write(' ')
        st.write(' ')
        if st.button('Submit'):
            edit_reminder_delivery_time(user_id, time=t)
            st.success(f'Success!')
            time.sleep(1)
            st.experimental_rerun()