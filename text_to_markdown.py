import re

def convert_to_markdown(text):
    # 移除多餘的空白行
    text = text.strip()
    
    # 將文字按行分割
    lines = text.splitlines()
    
    converted_lines = []
    
    for line in lines:
        # 移除行首尾的空白
        line = line.strip()
        
        # 處理主要項目符號 "- "
        if line.startswith('- '):
            line = line.replace('- ', '# ', 1)
            
        # 處理次要項目符號 "• "，改為使用 "- "
        elif '•' in line:
            # 移除開頭的空白，並將項目符號替換成markdown格式
            line = re.sub(r'\s*•\s*', '- ', line)
            
        # 如果不是空行就加入結果
        if line:
            converted_lines.append(line)
    
    # 合併所有行並加上適當的換行
    return '\n'.join(converted_lines)

def process_file(input_text):
    """處理輸入文字並返回markdown格式"""
    return convert_to_markdown(input_text)

if __name__ == "__main__":
    # 測試用範例
    sample_text = """  
    
• 從「舊流程(登入後檢查 IP)」變為「新流程(強制 2FA)」的最大差異，在於「預先」阻擋可疑登入，而不再依靠「事後通知」與「使用者自行封鎖」。  
• 後端在新流程中最主要的挑戰是「2FA 驗證碼產生、寄送、比對」與「對接前端的驗證狀態管理」，並決定是否還要保留一部分舊流程的功能 (如封鎖 IP) 作為補強。  
• 前後端需討論的重點在於：如何在前端順暢地完成驗證碼輸入、顯示錯誤與倒數、是否保留舊的 IP 管理介面，以及在新舊流程切換時的 UI/UX 與使用者認知。  
    
    """
    
    result = process_file(sample_text)
    print("轉換結果：\n")
    print(result) 
