import sys
from display import print_subsections, print_error, print_success, print_divider, clear_screen

# Valid categories supported by the trained model
BRANCHES = [
    "AI/ML", "Biotechnology", "Chemical", "Civil", "CSE",
    "Data Science", "ECE", "EEE", "IT", "Mechanical"
]

COLLEGE_TIERS = ["Tier 1", "Tier 2", "Tier 3"]

def get_branch_input():
    """
    Step 1: Select Branch
    """
    while True:
        print_subsections("Select Branch")
        for idx, b_name in enumerate(BRANCHES, 1):
            print(f"[{idx:2d}] {b_name}")
        print()
        choice = input("Enter choice (1-10): ").strip()
        if choice.isdigit():
            val = int(choice)
            if 1 <= val <= len(BRANCHES):
                selected = BRANCHES[val - 1]
                print_success(f"Branch selected: {selected}\n")
                return selected
        print_error("Invalid selection. Please enter a number between 1 and 10.")

def get_tier_input():
    """
    Step 2: Select College Tier
    """
    while True:
        print_subsections("Select College Tier")
        for idx, t_name in enumerate(COLLEGE_TIERS, 1):
            print(f"[{idx}] {t_name}")
        print()
        choice = input("Enter choice (1-3): ").strip()
        if choice.isdigit():
            val = int(choice)
            if 1 <= val <= len(COLLEGE_TIERS):
                selected = COLLEGE_TIERS[val - 1]
                print_success(f"College Tier selected: {selected}\n")
                return selected
        print_error("Invalid selection. Please enter a number between 1 and 3.")

def get_percentage_input(prompt_label):
    """
    Steps 3, 4, 7: 10th %, 12th %, Attendance %
    """
    while True:
        raw_val = input(f"{prompt_label} (0–100): ").strip()
        try:
            val = float(raw_val)
            if 0.0 <= val <= 100.0:
                return round(val, 2)
            else:
                print_error("Invalid percentage. Enter a value between 0 and 100.")
        except ValueError:
            print_error("Invalid input. Please enter a valid numerical percentage.")

def get_cgpa_input():
    """
    Step 5: Current CGPA (0 to 10)
    """
    while True:
        raw_val = input("Enter Current CGPA (0–10): ").strip()
        try:
            val = float(raw_val)
            if 0.0 <= val <= 10.0:
                return round(val, 2)
            else:
                print_error("Invalid CGPA. Enter a value between 0 and 10.")
        except ValueError:
            print_error("Invalid input. Please enter a valid numerical CGPA.")

def get_count_input(section_title, min_val, max_val):
    """
    Steps 6, 8, 9: Backlogs (0-5), Projects (0-5), Internships (0-4)
    """
    while True:
        print_subsections(section_title)
        for i in range(min_val, max_val + 1):
            print(f"[{i}] {i}")
        print()
        choice = input(f"Enter choice ({min_val}–{max_val}): ").strip()
        if choice.isdigit():
            val = int(choice)
            if min_val <= val <= max_val:
                return val
        print_error(f"Invalid selection. Please enter an integer between {min_val} and {max_val}.")

def collect_student_features():
    """
    Collects EXACTLY the 9 model input features in logical order.
    Returns a dictionary with exact keys required by the prediction pipeline.
    """
    clear_screen()
    print_divider("=")
    print("      STUDENT FEATURE ENTRY FORM      ".center(52))
    print_divider("=")
    print()

    branch = get_branch_input()
    tier = get_tier_input()
    tenth_pct = get_percentage_input("Enter 10th Percentage")
    print()
    twelfth_pct = get_percentage_input("Enter 12th Percentage")
    print()
    cgpa = get_cgpa_input()
    print()
    backlogs = get_count_input("Select Number of Backlogs", 0, 5)
    print()
    attendance = get_percentage_input("Enter Attendance Percentage")
    print()
    projects = get_count_input("Select Number of Projects", 0, 5)
    print()
    internships = get_count_input("Select Number of Internships", 0, 4)
    print()

    student_dict = {
        "Branch": branch,
        "College_Tier": tier,
        "10th_Percentage": tenth_pct,
        "12th_Percentage": twelfth_pct,
        "Current_CGPA": cgpa,
        "Backlogs": backlogs,
        "Attendance_Percentage": attendance,
        "Projects": projects,
        "Internships": internships
    }

    return student_dict

def show_input_summary(student_dict):
    """
    Displays the confirmation screen for collected student features.
    Options: [1] Confirm & Predict, [2] Edit Details, [3] Cancel
    """
    while True:
        clear_screen()
        print_divider("=")
        print("                INPUT SUMMARY                ".center(52))
        print_divider("=")
        print(f"Branch                  : {student_dict['Branch']}")
        print(f"College Tier            : {student_dict['College_Tier']}")
        print(f"10th Percentage         : {student_dict['10th_Percentage']:.2f}%")
        print(f"12th Percentage         : {student_dict['12th_Percentage']:.2f}%")
        print(f"Current CGPA            : {student_dict['Current_CGPA']:.2f}")
        print(f"Backlogs                : {student_dict['Backlogs']}")
        print(f"Attendance Percentage   : {student_dict['Attendance_Percentage']:.2f}%")
        print(f"Projects                : {student_dict['Projects']}")
        print(f"Internships             : {student_dict['Internships']}")
        print_divider("=")
        print()
        print("[1] Confirm & Predict")
        print("[2] Edit Details")
        print("[3] Cancel")
        print()
        choice = input("Enter choice (1-3): ").strip()
        if choice in ["1", "2", "3"]:
            return choice
        print_error("Invalid selection. Please enter 1, 2, or 3.")
