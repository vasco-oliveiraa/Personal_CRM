from Database.MySQLConnection import my_sql_connection
import Database.config as config

from Reminders.AddReminder import add_reminder

from datetime import datetime

def add_birthday_reminder(contact_id):
    # Checking if there are any birthday reminders
    birthday_reminder_constant = 'birthday! You should reach out with a message or a quick call.'
    current_date = datetime.now().date()

    with my_sql_connection() as c:
        c.execute(f'''
            SELECT
                 c.first_name, c.last_name, c.birthday, r.reminder_message, r.reminder_actual_date
            FROM
                {config.db_name}.contacts c
            JOIN
                {config.db_name}.reminders r ON r.contact_id = c.id
            WHERE
                c.id = %s AND r.reminder_message LIKE %s
            ORDER BY
                YEAR(r.reminder_actual_date) DESC
            LIMIT 1
        ''', (contact_id,f'%{birthday_reminder_constant}%'))
        results = c.fetchone()

        # If there are no birthday reminders for the current year, gather contact information
        if results is None:
            with my_sql_connection() as c:
                c.execute(f'''
                    SELECT
                        first_name, last_name, birthday
                    FROM
                        {config.db_name}.contacts c
                    WHERE id = %s
                ''', (contact_id,))
                results = c.fetchone()
            first_name = results[0]
            last_name = results[1]
            birthday = results[2]
            if birthday > current_date:
                date = birthday.replace(year=current_date.year)
            else:
                date = birthday.replace(year=current_date.year+1)
            
            print('No Birthday Reminders For Current Year')

        # If there are birthday reminders for this year, gather contact information and reminder information to assess if other birthday reminders should be set or not
        else:
            reminder_date = results[4]
            # If there is a reminder this year, but it has passed already
            if (reminder_date < current_date) and (reminder_date.year == current_date.year):
                date = reminder_date.replace(year=current_date.year+1)
            # If there is a reminder for a previous year
            elif (reminder_date.year < current_date.year):
                # Add a reminder for this year
                date = reminder_date.replace(year=current_date.year)
            else:
                date = None
                
            #check if the reminder date is in the past or in the future and if in the past, add the next reminder already
            first_name = results[0]
            last_name = results[1]
            print('Birthday Reminders For Current Year')
    if date is not None:
        title = f'Wish {first_name} {last_name} a happy birthday!'
        message = f"Today is {first_name}'s birthday! You should reach out with a message or a quick call."

        reminder_info = (contact_id, 0, title, date, message)
        add_reminder(reminder_info)
        print(f'Reminder Added: {title}')
    else:
        pass