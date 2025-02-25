import pyperclip
import time
from opencc import OpenCC
from datetime import datetime
import pytz
import re

# Define characters that should not be converted
preserved_chars = ['吃', '才', '裡']

def get_current_time():
    # Set Taiwan timezone
    tw_timezone = pytz.timezone('Asia/Taipei')
    return datetime.now(tw_timezone).strftime('%Y-%m-%d %H:%M:%S (UTC+8)')

def is_table_content(text):
    # Check if content is a table (contains multiple tabs or comma-separated text)
    lines = text.split('\n')
    if len(lines) < 2:  # Need at least two lines (header and content)
        return False
    
    # Check if each line contains tab or at least one comma
    return all('\t' in line or ',' in line for line in lines)

def convert_chinese_only(text, cc):
    # Use regex to find all Chinese characters
    chinese_pattern = r'[\u4e00-\u9fff]+'
    
    def replace_chinese(match):
        text = match.group(0)
        # If matched text contains any preserved characters
        if any(char in text for char in preserved_chars):
            # Split text into character list and process each
            chars = list(text)
            for i, char in enumerate(chars):
                # Convert character if it's not in preserved list
                if char not in preserved_chars:
                    chars[i] = cc.convert(char)
            return ''.join(chars)
        return cc.convert(text)
    
    # Only convert Chinese parts
    return re.sub(chinese_pattern, replace_chinese, text)

def convert_to_markdown_table(text, cc):
    lines = text.split('\n')
    # Convert tab-separated content to list
    table_data = [line.split('\t') if '\t' in line else line.split(',') for line in lines]
    
    # Create Markdown table
    markdown_lines = []
    # Add header row (convert only Chinese parts)
    header = [convert_chinese_only(cell, cc) for cell in table_data[0]]
    markdown_lines.append('| ' + ' | '.join(header) + ' |')
    # Add separator line
    markdown_lines.append('| ' + ' | '.join(['---' for _ in table_data[0]]) + ' |')
    # Add data rows (convert only Chinese parts)
    for row in table_data[1:]:
        converted_row = [convert_chinese_only(cell, cc) for cell in row]
        markdown_lines.append('| ' + ' | '.join(converted_row) + ' |')
    
    return '\n'.join(markdown_lines)

def write_to_log(original_text, converted_text):
    with open('conversion_log.txt', 'a', encoding='utf-8') as f:
        f.write(f"Time: {get_current_time()}\n")
        f.write(f"Original: {original_text}\n")
        f.write("-" * 30 + "\n")
        f.write(f"Converted: {converted_text}\n")
        f.write("=" * 20 + " Finish Conversion " + "=" * 20 + "\n")

def is_markdown_link(text):
    # Check if text is in Markdown link format [text](url)
    markdown_link_pattern = r'^\[([^\]]+)\]\(([^)]+)\)$'
    return bool(re.match(markdown_link_pattern, text.strip()))

def main():
    cc = OpenCC('s2t')
    last_clipboard = pyperclip.paste()
    
    print("Program started! When you copy new text, it will be automatically converted to Traditional Chinese.")
    print("Table conversion to Markdown format is supported.")
    print("Press Ctrl+C to stop the program")
    print("=" * 50)
    
    try:
        while True:
            current_clipboard = pyperclip.paste()
            
            if (current_clipboard != last_clipboard and 
                current_clipboard.strip() and 
                not is_markdown_link(current_clipboard)):
                
                # Check if content is a table
                if is_table_content(current_clipboard):
                    # Convert table (only Chinese parts)
                    converted_text = convert_to_markdown_table(current_clipboard, cc)
                else:
                    # For regular text, only convert Chinese parts
                    converted_text = convert_chinese_only(current_clipboard, cc)
                
                pyperclip.copy(converted_text)
                write_to_log(current_clipboard, converted_text)
                
                print(f"Time: {get_current_time()}")
                print(f"Original: {current_clipboard}")
                print("-" * 30)
                print(f"Converted: {converted_text}")
                print("=" * 20 + " Finish Conversion " + "=" * 20)
                
                last_clipboard = converted_text
            
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\nProgram stopped")

if __name__ == "__main__":
    main() 
