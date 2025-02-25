import pyperclip
import time
from opencc import OpenCC
from .text_converter import convert_chinese_only, is_markdown_link
from .table_converter import is_table_content, convert_to_markdown_table
from .logger import write_to_log, get_current_time

def main():
    # ... 原有的 main 函數內容 ... 
