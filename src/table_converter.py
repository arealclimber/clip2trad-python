from .text_converter import convert_chinese_only, is_code_content

def is_table_content(text):
    # Check if content is a table (contains multiple tabs or comma-separated text)
    lines = text.split('\n')
    if len(lines) < 2:  # Need at least two lines (header and content)
        return False
    
    # Check if each line contains tab or at least one comma
    return all('\t' in line or ',' in line for line in lines)

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
