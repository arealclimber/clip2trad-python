import pyperclip
import time
from opencc import OpenCC
from datetime import datetime
import pytz
import re

# 定義不需要轉換的字符列表
preserved_chars = ['吃', '才', '裡']

def get_current_time():
    # 設定臺灣時區
    tw_timezone = pytz.timezone('Asia/Taipei')
    return datetime.now(tw_timezone).strftime('%Y-%m-%d %H:%M:%S (UTC+8)')

def is_table_content(text):
    # 檢查是否為表格內容（包含多個 tab 或逗號分隔的文本）
    lines = text.split('\n')
    if len(lines) < 2:  # 至少需要兩行（標題行和內容行）
        return False
    
    # 檢查是否每行都包含 tab 或至少一個逗號
    return all('\t' in line or ',' in line for line in lines)

def convert_chinese_only(text, cc):
    # 使用正則表達式找出所有中文字符
    chinese_pattern = r'[\u4e00-\u9fff]+'
    
    def replace_chinese(match):
        text = match.group(0)
        # 如果匹配到的文字包含任何需要保留的字符
        if any(char in text for char in preserved_chars):
            # 將文字分成字符列表，逐個處理
            chars = list(text)
            for i, char in enumerate(chars):
                # 如果字符不在保留列表中，則轉換
                if char not in preserved_chars:
                    chars[i] = cc.convert(char)
            return ''.join(chars)
        return cc.convert(text)
    
    # 只轉換中文部分
    return re.sub(chinese_pattern, replace_chinese, text)

def convert_to_markdown_table(text, cc):
    lines = text.split('\n')
    # 將 tab 分隔的內容轉換為列表
    table_data = [line.split('\t') if '\t' in line else line.split(',') for line in lines]
    
    # 創建 Markdown 表格
    markdown_lines = []
    # 添加標題行（只轉換中文部分）
    header = [convert_chinese_only(cell, cc) for cell in table_data[0]]
    markdown_lines.append('| ' + ' | '.join(header) + ' |')
    # 添加分隔行
    markdown_lines.append('| ' + ' | '.join(['---' for _ in table_data[0]]) + ' |')
    # 添加數據行（只轉換中文部分）
    for row in table_data[1:]:
        converted_row = [convert_chinese_only(cell, cc) for cell in row]
        markdown_lines.append('| ' + ' | '.join(converted_row) + ' |')
    
    return '\n'.join(markdown_lines)

def write_to_log(original_text, converted_text):
    with open('conversion_log.txt', 'a', encoding='utf-8') as f:
        f.write(f"時間：{get_current_time()}\n")
        f.write(f"原文：{original_text}\n")
        f.write("-" * 30 + "\n")
        f.write(f"轉換：{converted_text}\n")
        f.write("=" * 20 + " Finish Conversion " + "=" * 20 + "\n")

def is_markdown_link(text):
    # 檢查是否為 Markdown 連結格式 [text](url)
    markdown_link_pattern = r'^\[([^\]]+)\]\(([^)]+)\)$'
    return bool(re.match(markdown_link_pattern, text.strip()))

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
            
            if (current_clipboard != last_clipboard and 
                current_clipboard.strip() and 
                not is_markdown_link(current_clipboard)):
                
                # 檢查是否為表格內容
                if is_table_content(current_clipboard):
                    # 轉換表格（只轉換中文部分）
                    converted_text = convert_to_markdown_table(current_clipboard, cc)
                else:
                    # 一般文本只轉換中文部分
                    converted_text = convert_chinese_only(current_clipboard, cc)
                
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
