import pyperclip
import time
from opencc import OpenCC
from datetime import datetime
import pytz
import re

def get_current_time():
    # 設定台灣時區
    tw_timezone = pytz.timezone('Asia/Taipei')
    return datetime.now(tw_timezone).strftime('%Y-%m-%d %H:%M:%S (UTC+8)')

def is_table_content(text):
    # 檢查是否為表格內容（包含多個 tab 或逗號分隔的文本）
    lines = text.split('\n')
    if len(lines) < 2:  # 至少需要兩行（標題行和內容行）
        return False
    
    # 檢查是否每行都包含 tab 或至少一個逗號
    return all('\t' in line or ',' in line for line in lines)

def convert_to_markdown_table(text):
    lines = text.split('\n')
    # 將 tab 分隔的內容轉換為列表
    table_data = [line.split('\t') if '\t' in line else line.split(',') for line in lines]
    
    # 創建 Markdown 表格
    markdown_lines = []
    # 添加標題行
    markdown_lines.append('| ' + ' | '.join(table_data[0]) + ' |')
    # 添加分隔行
    markdown_lines.append('| ' + ' | '.join(['---' for _ in table_data[0]]) + ' |')
    # 添加數據行
    for row in table_data[1:]:
        markdown_lines.append('| ' + ' | '.join(row) + ' |')
    
    return '\n'.join(markdown_lines)

def write_to_log(original_text, converted_text):
    with open('conversion_log.txt', 'a', encoding='utf-8') as f:
        f.write(f"時間：{get_current_time()}\n")
        f.write(f"原文：{original_text}\n")
        f.write("-" * 30 + "\n")
        f.write(f"轉換：{converted_text}\n")
        f.write("=" * 20 + " Finish Conversion " + "=" * 20 + "\n")

def main():
    cc = OpenCC('s2t')
    last_clipboard = pyperclip.paste()
    
    print("程序已啟動！當您複製新的文字時，將自動轉換為繁體中文。")
    print("支援表格轉換為 Markdown 格式。")
    print("按 Ctrl+C 可停止程序")
    print("=" * 50)
    
    try:
        while True:
            current_clipboard = pyperclip.paste()
            
            if current_clipboard != last_clipboard:
                # 檢查是否為表格內容
                if is_table_content(current_clipboard):
                    # 先轉換文字為繁體
                    converted_text = cc.convert(current_clipboard)
                    # 再轉換為 Markdown 表格格式
                    converted_text = convert_to_markdown_table(converted_text)
                else:
                    # 一般文本只進行繁體轉換
                    converted_text = cc.convert(current_clipboard)
                
                pyperclip.copy(converted_text)
                write_to_log(current_clipboard, converted_text)
                
                print(f"時間：{get_current_time()}")
                print(f"原文：{current_clipboard}")
                print("-" * 30)
                print(f"轉換：{converted_text}")
                print("=" * 20 + " Finish Conversion " + "=" * 20)
                
                last_clipboard = converted_text
            
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\n程序已停止")

if __name__ == "__main__":
    main() 
