import os

from appdirs import AppDirs


APP_DATA_PATH = AppDirs('spotifyblacklist', 'spotifyblacklist').user_data_dir

LIST_PATH = os.path.join(APP_DATA_PATH, 'blacklist.txt')
