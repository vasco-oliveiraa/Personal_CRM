from Database.DatabaseCreation import database_creation
from Database.TableCreation import table_creation

def confirm_reset():
    response = input('Running this file will reset the database on which this application is based. All data will be lost. Are you sure you want to continue? (y/n): ')
    if response.lower() == 'y':
        return True
    elif response.lower() == 'n':
        return False
    else:
        print('Invalid input. Please enter y/n.')
        return confirm_reset()

if confirm_reset():
    database_creation()
    table_creation()
else:
    print('Reset canceled. No changes were made.')