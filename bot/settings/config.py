import os

import dotenv

dotenv.load_dotenv()

MOTIVATION_BUTTON = 'Give motivation'
UNFOLLOWERS_BUTTON = 'Who didn\'t follow back'
CONVERT_CURRENCIES_BUTTON = 'Convert money'
LIST_OF_USER_BUTTONS = [MOTIVATION_BUTTON, CONVERT_CURRENCIES_BUTTON, UNFOLLOWERS_BUTTON]


ADMIN_IDS = [int(admin_id.strip()) for admin_id in os.getenv("ADMIN_IDS").split(',')]
ADMIN_FIRST_STEP = 'admin'
ADMIN_ADD_MOTIVATION_BUTTON = 'Add motivation'
LIST_OF_ADMIN_BUTTONS = [ADMIN_FIRST_STEP, ADMIN_ADD_MOTIVATION_BUTTON]

START_COMMAND = '/start'
HELP_COMMAND = '/help'
BUTTONS_COMMAND = '/buttons'


BACK_POINT = 'Back'
ADMIN_POINT = 'Admin buttons'
USER_POINT = 'User buttons'
LIST_OF_POINTS = [BACK_POINT, ADMIN_POINT, USER_POINT]

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.8 (KHTML, like Gecko)'
