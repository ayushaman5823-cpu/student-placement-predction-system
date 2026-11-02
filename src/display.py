import os
import sys

# Ensure UTF-8 output encoding on Windows terminals if supported
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

LINE_WIDTH = 52

def clear_screen():
    """
    Clears the terminal screen smoothly across Windows and Unix platforms.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def print_divider(char="=", width=LINE_WIDTH):
    print(char * width)

def print_subdivider(char="-", width=LINE_WIDTH):
    print(char * width)

def print_header(title, width=LINE_WIDTH):
    print_divider("=")
    print(f"{title.center(width)}")
    print_divider("=")
    print()

def print_subsections(title, width=LINE_WIDTH):
    print_subdivider("-")
    print(f"{title}")
    print_subdivider("-")

def print_error(message):
    try:
        print(f"\n[X] {message}\n")
    except UnicodeEncodeError:
        print(f"\n[ERROR] {message}\n")

def print_success(message):
    try:
        print(f"[OK] {message}")
    except UnicodeEncodeError:
        print(f"[OK] {message}")

def print_start_banner():
    clear_screen()
    print_divider("=")
    print("       STUDENT PLACEMENT PREDICTION SYSTEM       ".center(LINE_WIDTH))
    print_divider("=")
    print()
    print("        Machine Learning Based System".center(LINE_WIDTH))
    print()
    print("        Model: Gradient Boosting".center(LINE_WIDTH))
    print("        Dataset: 5,000 Student Records".center(LINE_WIDTH))
    print()
    print_divider("=")
    print()
    input("Press ENTER to continue... ")
