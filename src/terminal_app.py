import os
import sys

# Ensure src directory is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from display import print_start_banner, print_error
from predict import StudentPlacementPredictor
from menu import show_main_menu, handle_predict_workflow, show_model_info, show_about_project, show_exit_confirmation

def main():
    # Initialize ML Prediction Engine
    try:
        predictor = StudentPlacementPredictor()
    except Exception as e:
        print_error(f"Failed to load trained model pipeline: {e}")
        print("Please verify that models/best_model.pkl exists.")
        sys.exit(1)

    # Show Start Screen Banner
    print_start_banner()

    # Main Application Loop
    while True:
        choice = show_main_menu()

        if choice == "1":
            handle_predict_workflow(predictor)
        elif choice == "2":
            show_model_info()
        elif choice == "3":
            show_about_project()
        elif choice == "4":
            if show_exit_confirmation():
                sys.exit(0)
        else:
            print_error("Invalid selection. Please enter a choice between 1 and 4.")
            input("Press ENTER to try again...")

if __name__ == "__main__":
    main()
