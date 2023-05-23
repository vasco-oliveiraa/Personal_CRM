from Database.MySQLConnection import my_sql_connection
import Database.config as config

def table_creation():
    
    with my_sql_connection() as c:
        
        c.execute(f'''
            CREATE TABLE {config.db_name}.users(
                id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                first_name VARCHAR(255) NOT NULL,
                last_name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL UNIQUE,
                hashed_password VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                reminder_delivery_time TIME DEFAULT '08:00:00'
        );''')

        c.execute(f'''
            CREATE TABLE {config.db_name}.contacts(
                id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL REFERENCES {config.db_name}.users(id),
                first_name VARCHAR(255) NOT NULL,
                last_name VARCHAR(255) NOT NULL,
                birthday DATE,
                nationality VARCHAR(255),
                current_occupation VARCHAR(255),
                partner_name VARCHAR(255),
                year_met YEAR NOT NULL,
                circumstance_met VARCHAR(255) NOT NULL,
                city_met VARCHAR(255) NOT NULL,
                country_met VARCHAR(255) NOT NULL,
                interests TEXT,
                talking_points TEXT,
                maintenance CHAR(6)
        );''')

        c.execute(f'''
            CREATE TABLE {config.db_name}.interactions (
                id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                contact_id INT NOT NULL REFERENCES {config.db_name}.contacts(id),
                interaction_title VARCHAR(255),
                interaction_date DATE,
                notes TEXT
        );''')

        c.execute(f'''
            CREATE TABLE {config.db_name}.reminders (
                id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                contact_id INT NOT NULL REFERENCES {config.db_name}.contacts(id),
                interaction_id INT DEFAULT NULL REFERENCES {config.db_name}.interactions(id),
                reminder_title VARCHAR(255),
                reminder_actual_date DATE,
                reminder_message TEXT
        );''')



