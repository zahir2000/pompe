"""
Main Preprocessing Script

This script coordinates the cleaning and preprocessing of multiple datasets
including demographic, diagnosis, drugs, labs, and clinical data. 

Each data type has its own preprocessing module, and this script invokes 
the cleaning function from each module sequentially.
"""

# Importing necessary preprocessing modules for each data type
from tqdm import tqdm
from preprocess import demographic, diagnosis, drugs, labs, clinical


def main():
    """
    Main function to run the data preprocessing.
    
    Invokes the cleaning functions from each preprocessing module in sequence.
    """
    
   # List of all the preprocessing functions you want to run
    tasks = [
        ("demographic", demographic.run_cleaning),
        ("diagnosis", diagnosis.run_cleaning),
        ("drugs", drugs.run_cleaning),
        ("labs", labs.run_cleaning),
        ("clinical", clinical.run_cleaning)
    ]
    
    # Use tqdm to iterate over tasks and show progress
    for _, task_func in tqdm(tasks, desc="Processing Datasets", unit="dataset"):
        task_func()

# Ensuring the main function is only run when this script is executed directly
if __name__ == "__main__":
    main()
