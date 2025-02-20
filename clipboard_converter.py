import pyperclip
import time
from opencc import OpenCC

def main():
    # 初始化簡體到繁體轉換器
    cc = OpenCC('s2t')  # s2t 表示從簡體轉換到繁體
    
    # 記錄上一次的剪貼簿內容
    last_clipboard = pyperclip.paste()
    
    print("程序已啟動！當您複製新的文字時，將自動轉換為繁體中文。")
    print("按 Ctrl+C 可停止程序")
    
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
                
                # 更新上一次的剪貼簿內容
                last_clipboard = converted_text
                
                print("已轉換：", converted_text)
            
            # 短暫休息，避免佔用過多 CPU
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\n程序已停止")

if __name__ == "__main__":
    main() 
