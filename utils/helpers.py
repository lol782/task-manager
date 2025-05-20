# utils/helpers.py
import random
import time
import datetime

def generate_id():
    return random.randint(1000, 9999)

def format_time(seconds):
    return time.strftime('%H:%M:%S', time.gmtime(seconds))

def get_current_timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
