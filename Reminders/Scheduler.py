from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_ADDED, EVENT_JOB_REMOVED, EVENT_JOB_EXECUTED

from Database.MySQLConnection import my_sql_connection
import Database.config as config

from Reminders.SendEmail import send_email
from Reminders.AddBirthdayReminder import add_birthday_reminder

def job_event_listener(event):
    if event.code == EVENT_JOB_ADDED:
        print(f"New job added: {event.job_id}")
    elif event.code == EVENT_JOB_REMOVED:
        print(f"Job removed: {event.job_id}")
    elif event.code == EVENT_JOB_EXECUTED:
        print(f"Job executed: {event.job_id}")

def check_reminders(user_id):
    scheduler = BackgroundScheduler()
    scheduler.add_listener(job_event_listener, EVENT_JOB_ADDED | EVENT_JOB_REMOVED | EVENT_JOB_EXECUTED)
    scheduler.start()

    with my_sql_connection() as c:
        c.execute(f'''
            SELECT
                r.reminder_title AS Title,
                r.reminder_actual_date AS Date,
                r.reminder_message AS Message,
                CONCAT(c.first_name, ' ', c.last_name) AS Contact,
                u.first_name AS User_First_Name,
                u.email AS User_Email,
                u.reminder_delivery_time AS User_Reminder_Delivery_Time
            FROM
                {config.db_name}.reminders r
            JOIN
                {config.db_name}.contacts c ON c.id = r.contact_id
            JOIN
                {config.db_name}.users u ON u.id = c.user_id
            WHERE
                u.id = %s
        ''', (user_id,))

        reminders = c.fetchall()

    todays_reminders = []

    current_date = datetime.now().date()

    for reminder in reminders:
        reminder_date = reminder[1]
        if reminder_date == current_date:
            todays_reminders.append(reminder)

    if todays_reminders:
        user_first_name = todays_reminders[0][4]
        receiver_email = todays_reminders[0][5]
        reminder_delivery_time = todays_reminders[0][6]
        hour = int(reminder_delivery_time.total_seconds() // 3600)
        minute = int((reminder_delivery_time.total_seconds() % 3600) // 60)
        subject = '✉️ Sau Reminders for Today!'
        message = f"Hey {user_first_name},\n\nHere are your Sau reminders for today:\n\n"

        for reminder in todays_reminders:
            contact = reminder[3]
            reminder_message = reminder[2]
            reminder_title = reminder[0]

            message += f"- {contact} - {reminder_title}:\n"
            message += f"  {reminder_message}\n\n"
            
    # Schedule the email to be sent at the desired send time
    scheduler.add_job(send_email, trigger='cron', hour=hour, minute=minute, args=[receiver_email, subject, message])
        
def schedule_reminders():
    scheduler = BackgroundScheduler()
    scheduler.add_listener(job_event_listener, EVENT_JOB_ADDED | EVENT_JOB_REMOVED | EVENT_JOB_EXECUTED)

    # Retrieve all user_ids from the database
    with my_sql_connection() as c:
        c.execute(f'SELECT DISTINCT id FROM {config.db_name}.users;')
        rows = c.fetchall()

    user_ids = [row[0] for row in rows]

    # Calculate the start time for the next day at 00:00
    start_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)

    for user_id in user_ids:
        scheduler.add_job(
            check_reminders,
            trigger='interval',
            days=1,
            start_date=start_time,
            args=[user_id]
        )

    scheduler.start()
    
def schedule_birthday_reminders():
    scheduler = BackgroundScheduler()
    scheduler.add_listener(job_event_listener, EVENT_JOB_ADDED | EVENT_JOB_REMOVED | EVENT_JOB_EXECUTED)
    
    # Retrieve all user_ids from the database
    with my_sql_connection() as c:
        c.execute(f'SELECT DISTINCT id FROM {config.db_name}.contacts;')
        rows = c.fetchall()

    contact_ids = [row[0] for row in rows]
    
    for index, contact_id in enumerate(contact_ids):
        # Calculate the minute and second values
        minute = index // 60  # Integer division to get the minute value
        second = index % 60  # Modulo operator to get the second value

        # Schedule the function to run on the first day of every year at 00:00
        scheduler.add_job(
            add_birthday_reminder,
            trigger='cron',
            month=1,
            day=1,
            hour=0,
            minute=minute,
            second=second,
            args=[contact_id]
        )

    # Start the scheduler
    scheduler.start()