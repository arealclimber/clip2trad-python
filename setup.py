from setuptools import setup, find_packages

setup(
    name="clipboard-converter",
    version="1.0.0",
    packages=find_packages(include=['src', 'src.*']),
    install_requires=[
        "pyperclip",
        "opencc-python-reimplemented",
        "pytz",
    ],
    entry_points={
        'console_scripts': [
            'clipboard-converter=src.clipboard_converter:main',
        ],
    },
) 
