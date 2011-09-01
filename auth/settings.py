
import os

PROJECT_PATH = os.path.abspath(os.path.split(__file__)[0])

DATABASE_PATH = "/tmp/auth_test.db"

EMAIL_HOST = "localhost"
EMAIL_FROM = "noreply@localhost"

#number of days for the user to activate the account
DAYS_TO_ACTIVATE = 31

#Max tries with wrong password
MAX_PWD_TRIES = 3

