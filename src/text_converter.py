import re
from opencc import OpenCC

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

def convert_chinese_only(text, cc=None):
    if cc is None:
        cc = OpenCC('s2t')
        
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

def is_markdown_link(text):
    # Check if text is in Markdown link format [text](url)
    markdown_link_pattern = r'^\[([^\]]+)\]\(([^)]+)\)$'
    return bool(re.match(markdown_link_pattern, text.strip())) 
