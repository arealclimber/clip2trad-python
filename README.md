# Clipboard Chinese Converter

A Python tool that automatically converts Simplified Chinese text to Traditional Chinese when copying text to the clipboard. It also supports converting tables to Markdown format.

## Features

- Real-time clipboard monitoring
- Automatic conversion from Simplified to Traditional Chinese
- Preserves code snippets without conversion
- Converts tables to Markdown format
- Logging of all conversions with timestamps
- Custom character preservation and mapping

## Installation and Usage

### Method 1: Direct Python Execution

1. Ensure you have Python 3.6 or above installed
2. Clone this repository:
   ```bash
   git clone https://github.com/your-username/clipboard-converter.git
   cd clipboard-converter
   ```
3. Install required packages:
   ```bash
   pip install pyperclip opencc-python-reimplemented pytz
   ```
4. Run the script directly:
   ```bash
   python src/clipboard_converter.py
   ```

### Method 2: Package Installation

1. Clone and enter the repository as shown above
2. Install the package:
   ```bash
   pip install -e .
   ```
3. Run using the command:
   ```bash
   clipboard-converter
   ```

## How It Works

The program will:

1. Monitor your clipboard for changes
2. Automatically convert any Simplified Chinese text to Traditional Chinese
3. Preserve any code snippets or special characters
4. Convert tables to Markdown format
5. Log all conversions in the `logs` directory

To stop the program, press `Ctrl+C`.

## Development Guide

### Project Structure

```
clipboard-converter/
├── src/
│   ├── text_converter.py    # Text conversion functions
│   ├── table_converter.py   # Table conversion functions
│   └── logger.py           # Logging functions
├── clipboard_converter.py   # Main program
├── setup.py                # Installation configuration
└── README.md              # Documentation
```

### Modules

#### text_converter.py

- `is_code_content(text)`: Detects if text contains code
- `convert_chinese_only(text, cc)`: Converts only Chinese characters
- `is_markdown_link(text)`: Checks if text is a Markdown link

#### table_converter.py

- `is_table_content(text)`: Detects if text is a table
- `convert_to_markdown_table(text, cc)`: Converts table to Markdown format

#### logger.py

- `get_current_time()`: Gets current time in Taiwan timezone
- `write_to_log(original, converted)`: Logs conversion details

### Adding New Features

To add new features:

1. Create appropriate module in `src/` directory
2. Import and use the module in `clipboard_converter.py`
3. Update `setup.py` if new dependencies are required

### Configuration

The converter includes several configurable features:

- Preserved characters: Characters that should not be converted
- Custom mappings: Special character conversion rules
- Code detection: Patterns for identifying code snippets

These can be modified in `text_converter.py`.

## Logging

Conversion logs are stored in the `logs` directory with filename format:

```
logs/clipboard_YYYYMMDD.txt
```

Each log entry includes:

- Timestamp (UTC+8)
- Original text
- Converted text
- Conversion completion marker

## Dependencies

- pyperclip: Clipboard operations
- opencc-python-reimplemented: Chinese character conversion
- pytz: Timezone handling

## License

MIT License
