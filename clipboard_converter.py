import pyperclip
import time
from opencc import OpenCC
from datetime import datetime
import pytz
import re

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

def is_code_content(text):
    # Check if content is code
    
    # 1. Check if it's a comment line or variable definition
    line = text.strip()
    if line.startswith('//'):
        # Check if it's a variable definition or configuration format
        if re.match(r'^//\s*[a-zA-Z_][a-zA-Z0-9_]*\s*[:=]', line):
            return True
        # Check if it contains common code value formats
        if re.search(r':\s*\d+,?$', line):  # e.g., // userId: 10000000,
            return True
    
    if line.startswith('/*'):
        return True
        
    # 2. Check common code characteristics
    code_indicators = [
        # Common programming language keywords
        'function ', 'def ', 'class ', 'import ', 'from ', 'var ', 'let ', 'const ',
        'return ', 'if ', 'else ', 'for ', 'while ', 'try ', 'catch ',
        # Common code symbol combinations
        '=>', '{', '}', ');', '};', '());',
        # Variable assignment patterns
        ': true,', ': false,', ': null,', ': undefined,',
        # HTML/XML tags
        '<div', '<span', '<p>', '</p>', '<a ', '</a>',
        # SQL keywords
        'SELECT ', 'FROM ', 'WHERE ', 'INSERT ', 'UPDATE ',
        # Code indentation patterns
        '    def ', '    if ', '    return',
    ]
    
    # Check each line
    lines = text.split('\n')
    for line in lines:
        line = line.strip()
        
        # Check if it's pure code line (no Chinese characters)
        has_chinese = bool(re.search(r'[\u4e00-\u9fff]', line))
        
        # Check if contains code indicators
        if any(indicator in line for indicator in code_indicators) and not has_chinese:
            return True
            
        # Check if it matches common code patterns
        if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*\s*\([^)]*\)\s*{?\s*$', line):  # Function definition
            return True
        if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*\s*=\s*function\s*\(', line):  # JavaScript function
            return True
        if re.match(r'^\s*[a-zA-Z_][a-zA-Z0-9_]*\s*:\s*function', line):  # Object method
            return True
        # Check variable definition format
        if re.match(r'^\s*[a-zA-Z_][a-zA-Z0-9_]*\s*:\s*\d+,?\s*$', line):  # Variable definition
            return True
            
    return False

def convert_chinese_only(text, cc):
    # If it's code, return original text
    if is_code_content(text):
        return text
        
    # Use regex to find all Chinese characters
    chinese_pattern = r'[\u4e00-\u9fff]+'
    
    # Define characters that should not be converted
    preserved_chars = ['吃', '才']
    
    # Define custom character mappings
    custom_mappings = {
        '里': '裡',
        '为': '為'
    }
    
    def replace_chinese(match):
        text = match.group(0)
        # First check for custom mappings
        for simplified, traditional in custom_mappings.items():
            text = text.replace(simplified, traditional)
            
        # Then handle preserved characters
        if any(char in text for char in preserved_chars):
            chars = list(text)
            for i, char in enumerate(chars):
                if char not in preserved_chars:
                    chars[i] = cc.convert(char)
            return ''.join(chars)
        
        # Convert remaining text
        return cc.convert(text)
    
    # Process text line by line
    lines = text.split('\n')
    converted_lines = []
    for line in lines:
        # If line is code comment, keep it as is
        if line.strip().startswith('//') or line.strip().startswith('/*'):
            converted_lines.append(line)
        else:
            # Only convert Chinese parts
            converted_lines.append(re.sub(chinese_pattern, replace_chinese, line))
    
    return '\n'.join(converted_lines)

def convert_to_markdown_table(text, cc):
    lines = text.split('\n')
    # Convert tab-separated content to list
    table_data = [line.split('\t') if '\t' in line else line.split(',') for line in lines]
    
    # Create Markdown table
    markdown_lines = []
    
    def convert_cell(cell):
        # Check if cell contains code
        if is_code_content(cell):
            return cell  # If it's code, keep it as is
        return convert_chinese_only(cell, cc)  # Otherwise convert Chinese
    
    # Add header row (check each cell for code)
    header = [convert_cell(cell) for cell in table_data[0]]
    markdown_lines.append('| ' + ' | '.join(header) + ' |')
    
    # Add separator line
    markdown_lines.append('| ' + ' | '.join(['---' for _ in table_data[0]]) + ' |')
    
    # Add data rows (check each cell for code)
    for row in table_data[1:]:
        converted_row = [convert_cell(cell) for cell in row]
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
    last_clipboard = pyperclip.paste() or ''  # Use empty string if None is returned
    
    print("Program started! When you copy new text, it will be automatically converted to Traditional Chinese.")
    print("Table conversion to Markdown format is supported.")
    print("Press Ctrl+C to stop the program")
    print("=" * 50)
    
    try:
        while True:
            try:
                current_clipboard = pyperclip.paste() or ''  # Use empty string if None is returned
                
                if (current_clipboard != last_clipboard and 
                    current_clipboard.strip() and 
                    not is_markdown_link(current_clipboard)):
                    
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
                
            except Exception as e:
                print(f"Error processing clipboard: {str(e)}")
                time.sleep(0.1)  # Pause briefly when error occurs
                continue
            
    except KeyboardInterrupt:
        print("\nProgram stopped")

if __name__ == "__main__":
    main() 
