import pyperclip
import time
from opencc import OpenCC
from src.text_converter import convert_chinese_only, is_markdown_link
from src.table_converter import is_table_content, convert_to_markdown_table
from src.logger import write_to_log, get_current_time

def main():
    cc = OpenCC('s2t')
    last_clipboard = pyperclip.paste() or ''
    
    print("Program started! When you copy new text, it will be automatically converted to Traditional Chinese.")
    print("Table conversion to Markdown format is supported.")
    print(f"Log files will be saved in the logs directory with format: clipboard_YYYYMMDD.txt")
    print("Press Ctrl+C to stop the program")
    print("=" * 50)
    
    try:
        while True:
            try:
                current_clipboard = pyperclip.paste() or ''  # Use empty string if None is returned
                
                if (current_clipboard != last_clipboard and 
                    current_clipboard.strip() and 
                    not is_markdown_link(current_clipboard)):
                    
                    # Determine if content is table and convert accordingly
                    if is_table_content(current_clipboard):
                        converted_text = convert_to_markdown_table(current_clipboard, cc)
                    else:
                        converted_text = convert_chinese_only(current_clipboard, cc)

                    pyperclip.copy(converted_text)
                    write_to_log(current_clipboard, converted_text)
                    
                    print(f"Time: {get_current_time().strftime('%Y-%m-%d %H:%M:%S (UTC+8)')}")
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
