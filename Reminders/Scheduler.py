from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, time, timedelta

scheduler = BackgroundScheduler()
scheduler.start()

def check_reminders():
    # Retrieve the list of reminders from your data structure or database
    reminders = get_reminders()

    current_time = datetime.now().time()

    # Iterate over each reminder
    for reminder in reminders:
        if (reminder.due_date.date() == datetime.now().date() and
                current_time >= reminder.due_time):
            # Calculate the time difference between the current time and the desired send time
            time_diff = datetime.combine(datetime.today(), reminder.due_time) - datetime.combine(datetime.today(), current_time)

            # Schedule the email to be sent at the desired send time
            scheduler.add_job(send_email, 'date', run_date=datetime.now() + timedelta(seconds=time_diff.seconds), args=[reminder])

# Schedule the check_reminders function to run every day at a specific time (e.g., 8:00 AM)
scheduler.add_job(check_reminders, 'cron', hour=8, minute=0)
