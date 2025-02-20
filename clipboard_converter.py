import pyperclip
import time
from opencc import OpenCC
from datetime import datetime
import pytz

def get_current_time():
    # 設定台灣時區
    tw_timezone = pytz.timezone('Asia/Taipei')
    return datetime.now(tw_timezone).strftime('%Y-%m-%d %H:%M:%S (UTC+8)')

def write_to_log(original_text, converted_text):
    with open('conversion_log.txt', 'a', encoding='utf-8') as f:
        f.write(f"時間：{get_current_time()}\n")
        f.write(f"原文：{original_text}\n")
        f.write("-" * 30 + "\n")  # 原文之後的短分隔線
        f.write(f"轉換：{converted_text}\n")
        f.write("=" * 20 + " Finish Conversion " + "=" * 20 + "\n")  # 加入文字的長分隔線

def main():
    # 初始化簡體到繁體轉換器
    cc = OpenCC('s2t')  # s2t 表示從簡體轉換到繁體
    
    # 記錄上一次的剪貼簿內容
    last_clipboard = pyperclip.paste()
    
    print("程序已啟動！當您複製新的文字時，將自動轉換為繁體中文。")
    print("按 Ctrl+C 可停止程序")
    print("=" * 50)
    
    try:
        while True:
            # 獲取當前剪貼簿內容
            current_clipboard = pyperclip.paste()
            
            # 如果剪貼簿內容有變化
            if current_clipboard != last_clipboard:
                # 轉換為繁體中文
                converted_text = cc.convert(current_clipboard)
                
                # 將轉換後的文字放回剪貼簿
                pyperclip.copy(converted_text)
                
                # 寫入日誌
                write_to_log(current_clipboard, converted_text)
                
                # 在終端機顯示轉換結果
                print(f"時間：{get_current_time()}")
                print(f"原文：{current_clipboard}")
                print("-" * 30)  # 原文之後的短分隔線
                print(f"轉換：{converted_text}")
                print("=" * 20 + " Finish Conversion " + "=" * 20)  # 加入文字的長分隔線
                
                # 更新上一次的剪貼簿內容
                last_clipboard = converted_text
            
            # 短暫休息，避免佔用過多 CPU
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\n程序已停止")

if __name__ == "__main__":
    main() 
