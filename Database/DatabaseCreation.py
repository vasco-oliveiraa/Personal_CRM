from Database.MySQLConnection import my_sql_connection
import Database.config as config

def database_creation():
    with my_sql_connection() as c:
        c.execute("SHOW DATABASES")
        databases = c.fetchall()
        database_names = [d[0] for d in databases]

        if config.db_name in database_names:
            c.execute(
                f"DROP DATABASE {config.db_name}"
            )

        c.execute(
            f"CREATE DATABASE {config.db_name}"
        )