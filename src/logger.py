import os
from datetime import datetime
import pytz

def get_current_time():
    # Set Taiwan timezone
    tw_timezone = pytz.timezone('Asia/Taipei')
    return datetime.now(tw_timezone)

def get_log_filename():
    # Get current date in Taiwan timezone for filename
    current_time = get_current_time()
    return f"logs/clipboard_{current_time.strftime('%Y%m%d')}.txt"

def ensure_log_directory():
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')

def write_to_log(original_text, converted_text):
    current_time = get_current_time()
    ensure_log_directory()
    
    filename = get_log_filename()
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(f"Time: {current_time.strftime('%Y-%m-%d %H:%M:%S (UTC+8)')}\n")
        f.write(f"Original: {original_text}\n")
        f.write("-" * 30 + "\n")
        f.write(f"Converted: {converted_text}\n")
        f.write("=" * 20 + " Finish Conversion " + "=" * 20 + "\n") 
