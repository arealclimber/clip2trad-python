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

def is_code_content(text):
    # 檢查是否為程式碼
    
    # 1. 檢查是否為註釋行或變數定義
    line = text.strip()
    if line.startswith('//'):
        # 檢查是否為變數定義或配置格式
        if re.match(r'^//\s*[a-zA-Z_][a-zA-Z0-9_]*\s*[:=]', line):
            return True
        # 檢查是否包含常見的程式碼值格式
        if re.search(r':\s*\d+,?$', line):  # 例如 // userId: 10000000,
            return True
    
    if line.startswith('/*'):
        return True
        
    # 2. 檢查常見的程式碼特徵
    code_indicators = [
        # 常見程式語言的關鍵字
        'function ', 'def ', 'class ', 'import ', 'from ', 'var ', 'let ', 'const ',
        'return ', 'if ', 'else ', 'for ', 'while ', 'try ', 'catch ',
        # 常見程式碼符號組合
        '=>', '{', '}', ');', '};', '());',
        # 變數賦值模式
        ': true,', ': false,', ': null,', ': undefined,',
        # HTML/XML 標籤
        '<div', '<span', '<p>', '</p>', '<a ', '</a>',
        # SQL 關鍵字
        'SELECT ', 'FROM ', 'WHERE ', 'INSERT ', 'UPDATE ',
        # 程式碼縮排特徵
        '    def ', '    if ', '    return',
    ]
    
    # 檢查每一行
    lines = text.split('\n')
    for line in lines:
        line = line.strip()
        
        # 檢查是否為純程式碼行（不包含中文字符）
        has_chinese = bool(re.search(r'[\u4e00-\u9fff]', line))
        
        # 檢查是否包含程式碼指標
        if any(indicator in line for indicator in code_indicators) and not has_chinese:
            return True
            
        # 檢查是否為常見的程式碼模式
        if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*\s*\([^)]*\)\s*{?\s*$', line):  # 函數定義
            return True
        if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*\s*=\s*function\s*\(', line):  # JavaScript 函數
            return True
        if re.match(r'^\s*[a-zA-Z_][a-zA-Z0-9_]*\s*:\s*function', line):  # 物件方法
            return True
        # 檢查變數定義格式
        if re.match(r'^\s*[a-zA-Z_][a-zA-Z0-9_]*\s*:\s*\d+,?\s*$', line):  # 變數定義
            return True
            
    return False

def convert_chinese_only(text, cc):
    # 如果是程式碼，直接返回原文
    if is_code_content(text):
        return text
        
    # 使用正則表達式找出所有中文字符
    chinese_pattern = r'[\u4e00-\u9fff]+'
    
    # 定義不需要轉換的字符列表
    preserved_chars = ['吃', '才']
    
    def replace_chinese(match):
        text = match.group(0)
        # 如果匹配到的文字包含任何需要保留的字符
        if any(char in text for char in preserved_chars):
            chars = list(text)
            for i, char in enumerate(chars):
                if char not in preserved_chars:
                    chars[i] = cc.convert(char)
            return ''.join(chars)
        return cc.convert(text)
    
    # 逐行處理文本
    lines = text.split('\n')
    converted_lines = []
    for line in lines:
        # 如果這行是程式碼註釋，保持原樣
        if line.strip().startswith('//') or line.strip().startswith('/*'):
            converted_lines.append(line)
        else:
            # 只轉換中文部分
            converted_lines.append(re.sub(chinese_pattern, replace_chinese, line))
    
    return '\n'.join(converted_lines)

def convert_to_markdown_table(text, cc):
    lines = text.split('\n')
    # 將 tab 分隔的內容轉換為列表
    table_data = [line.split('\t') if '\t' in line else line.split(',') for line in lines]
    
    # 創建 Markdown 表格
    markdown_lines = []
    
    def convert_cell(cell):
        # 檢查單元格是否包含程式碼
        if is_code_content(cell):
            return cell  # 如果是程式碼，保持原樣
        return convert_chinese_only(cell, cc)  # 否則轉換中文
    
    # 添加標題行（檢查每個單元格是否為程式碼）
    header = [convert_cell(cell) for cell in table_data[0]]
    markdown_lines.append('| ' + ' | '.join(header) + ' |')
    
    # 添加分隔行
    markdown_lines.append('| ' + ' | '.join(['---' for _ in table_data[0]]) + ' |')
    
    # 添加數據行（檢查每個單元格是否為程式碼）
    for row in table_data[1:]:
        converted_row = [convert_cell(cell) for cell in row]
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
                
                # # 檢查是否為表格內容
                # if is_table_content(current_clipboard):
                #     # 轉換表格（只轉換中文部分）
                #     converted_text = convert_to_markdown_table(current_clipboard, cc)
                # else:
                #     # 一般文本只轉換中文部分
                #     converted_text = convert_chinese_only(current_clipboard, cc)
                
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
