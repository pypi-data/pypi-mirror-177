from platformdirs import *
from os.path import join

app_folder = user_data_dir('aqua-cli')
db_file = join(app_folder, 'database.db')