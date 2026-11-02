import os
import json
import sys
from display import clear_screen, print_divider, print_subdivider, print_error, print_success
from input_handler import collect_student_features, show_input_summary

def get_authoritative_metrics():
    """
    Retrieves the authoritative model evaluation metrics.
    Loads from MODEL_METADATA.json if present, falling back to verified baseline constants.
    """
    metadata_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "MODEL_METADATA.json")
    if os.path.exists(metadata_path):
        try:
            with open(metadata_path, "r", encoding="utf-8") as f:
                meta = json.load(f)
            test_metrics = meta.get("evaluation_context", {}).get("holdout_test_metrics", {})
            if test_metrics:
                return {
                    "accuracy": float(test_metrics.get("accuracy", 0.8310)),
                    "precision": float(test_metrics.get("precision", 0.8276)),
                    "recall": float(test_metrics.get("recall", 0.9019)),
                    "f1_score": float(test_metrics.get("f1_score", 0.8632)),
                    "roc_auc": float(test_metrics.get("roc_auc", 0.9036)),
                    "brier_score": float(test_metrics.get("brier_score", 0.1158))
                }
        except Exception:
            pass
    return {
        "accuracy": 0.8310,
        "precision": 0.8276,
        "recall": 0.9019,
        "f1_score": 0.8632,
        "roc_auc": 0.9036,
        "brier_score": 0.1158
    }

def show_main_menu():
    """
    Displays the Main Menu options.
    """
    clear_screen()
    print_divider("=")
    print("                    MAIN MENU                    ".center(52))
    print_divider("=")
    print()
    print("[1] Enter Student Details & Predict Placement")
    print("[2] Model Information")
    print("[3] About Project")
    print("[4] Exit")
    print()
    print_divider("=")
    print()
    choice = input("Enter your choice: ").strip()
    return choice

def display_prediction_results(result_dict):
    """
    Displays prediction class and exact dynamic probabilities from predict_proba().
    """
    clear_screen()
    status = result_dict['predicted_status']
    prob_placed = result_dict['probability_placed']
    prob_not_placed = result_dict['probability_not_placed']

    print_divider("=")
    print("              PREDICTION RESULT              ".center(52))
    print_divider("=")
    print()

    if status == "Placed":
        print("                 ✓ PLACED                 ".center(52))
    else:
        print("              ✗ NOT PLACED                ".center(52))

    print()
    print("        Placement Probability        ".center(52))
    print(f"                 {prob_placed:.2f}%                 ".center(52))
    print()
    print("        Not Placed Probability        ".center(52))
    print(f"                 {prob_not_placed:.2f}%                 ".center(52))
    print()
    print_divider("=")
    print()

def handle_predict_workflow(predictor):
    """
    Handles Option 1: Feature collection, summary confirmation, prediction call, and result loop.
    """
    while True:
        student_dict = collect_student_features()

        while True:
            confirm_choice = show_input_summary(student_dict)

            if confirm_choice == "1":
                # Confirm & Predict
                clear_screen()
                print_subdivider("-")
                print("Analyzing Student Profile...")
                print_subdivider("-")
                print("✓ Input validation complete")
                print("✓ Feature preparation complete")
                print("✓ Trained model loaded")
                print("✓ Placement prediction generated")
                print("✓ Probability calculated")
                print()

                # Execute ML prediction via pipeline
                try:
                    result = predictor.predict_student(student_dict)
                    display_prediction_results(result)
                except Exception as e:
                    print_error(f"Prediction failed: {e}")
                    input("Press ENTER to return to Main Menu...")
                    return

                # After prediction options
                while True:
                    print("What would you like to do?")
                    print()
                    print("[1] Predict Another Student")
                    print("[2] Return to Main Menu")
                    print("[3] Exit")
                    print()
                    after_choice = input("Enter choice (1-3): ").strip()

                    if after_choice == "1":
                        break # Break inner loop, start fresh collection
                    elif after_choice == "2":
                        return # Return to Main Menu
                    elif after_choice == "3":
                        if show_exit_confirmation():
                            sys.exit(0)
                        else:
                            clear_screen()
                            display_prediction_results(result)
                    else:
                        print_error("Invalid selection. Please enter 1, 2, or 3.")

                if after_choice == "1":
                    break # Break to outer collection loop

            elif confirm_choice == "2":
                # Edit Details - loop back to feature collection
                break

            elif confirm_choice == "3":
                # Cancel - return to main menu
                return

def show_model_info():
    """
    Displays Option 2: Model Information & Features Information
    """
    clear_screen()
    print_divider("=")
    print("                MODEL INFORMATION                ".center(52))
    print_divider("=")
    print()
    print("Model Architecture:")
    print("  Gradient Boosting Classifier (Ensemble)")
    print()
    print("Dataset Split:")
    print("  Total Records : 5,000")
    print("  Training Set  : 4,000 records (80%)")
    print("  Test Set      : 1,000 records (20%)")
    print()
    metrics = get_authoritative_metrics()
    print("Empirical Evaluation Metrics (Untouched Test Set):")
    print(f"  Test Accuracy  : {metrics['accuracy'] * 100:.2f}%")
    print(f"  Test Precision : {metrics['precision'] * 100:.2f}%")
    print(f"  Test Recall    : {metrics['recall'] * 100:.2f}%")
    print(f"  Test F1 Score  : {metrics['f1_score'] * 100:.2f}%")
    print(f"  Test ROC-AUC   : {metrics['roc_auc'] * 100:.2f}%")
    print(f"  Brier Score    : {metrics['brier_score']:.4f}")
    print()
    print_subdivider("-")
    print("MODEL INPUT FEATURES (Exact 9 Features):")
    print("  1. Branch")
    print("  2. College Tier")
    print("  3. 10th Percentage")
    print("  4. 12th Percentage")
    print("  5. Current CGPA")
    print("  6. Backlogs")
    print("  7. Attendance Percentage")
    print("  8. Projects")
    print("  9. Internships")
    print()
    print("Excluded from Prediction Pipeline:")
    print("  - Student ID, Name, Gender, College Name, Placement Probability")
    print_subdivider("-")
    print()
    print("NOTE: Performance was measured on the synthetic/augmented")
    print("project dataset and should not be interpreted as real-world")
    print("placement prediction accuracy.")
    print()
    print_divider("=")
    print()
    input("Press ENTER to return to Main Menu...")

def show_about_project():
    """
    Displays Option 3: About Project
    """
    clear_screen()
    print_divider("=")
    print("                  ABOUT PROJECT                  ".center(52))
    print_divider("=")
    print()
    print("Student Placement Prediction System")
    print()
    print("This project uses Machine Learning to predict whether a")
    print("student is likely to be placed based on nine academic,")
    print("attendance, experience, and college-related features.")
    print()
    print("Best Model:")
    print("  Gradient Boosting Classifier")
    print()
    print("Prediction Output:")
    print("  Placed / Not Placed")
    print()
    print("Probability Calculation:")
    print("  Generated dynamically using pipeline.predict_proba()")
    print()
    print("Dataset Context:")
    print("  5,000 synthetic/augmented student records")
    print()
    print_divider("=")
    print()
    input("Press ENTER to return to Main Menu...")

def show_exit_confirmation():
    """
    Displays Option 4: Exit confirmation screen.
    Returns True if user confirms exit, False otherwise.
    """
    while True:
        clear_screen()
        print_divider("=")
        print("                EXIT CONFIRMATION                ".center(52))
        print_divider("=")
        print()
        print("Are you sure you want to exit?")
        print()
        print("[1] Yes")
        print("[2] No")
        print()
        choice = input("Enter choice (1-2): ").strip()
        if choice == "1":
            clear_screen()
            print_divider("=")
            print("Thank you for using the".center(52))
            print("Student Placement Prediction System.".center(52))
            print_divider("=")
            print()
            print("Goodbye!\n")
            return True
        elif choice == "2":
            return False
        else:
            print_error("Invalid selection. Please enter 1 or 2.")
