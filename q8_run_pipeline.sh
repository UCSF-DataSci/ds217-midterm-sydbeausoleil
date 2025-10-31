#!/bin/bash

# Assignment 5, Question 8: Pipeline Automation Script
# Run the clinical trial data analysis pipeline

# NOTE: This script assumes Q1 has already been run to create directories and generate the dataset
# NOTE: Q2 (q2_process_metadata.py) is a standalone Python fundamentals exercise, not part of the main pipeline
# NOTE: Q3 (q3_data_utils.py) is a library imported by the notebooks, not run directly
# NOTE: The main pipeline runs Q4-Q7 notebooks in order

LOG_FILE="reports/pipeline_log.txt"
NOTEBOOKS=("q4_exploration.ipynb" "q5_missing_data.ipynb" "q6_transformation.ipynb" "q7_aggregation.ipynb")

echo "Starting clinical trial pipeline at $(date)" > $LOG_FILE

for nb in "${NOTEBOOKS[@]}"; do
    echo "Running $nb ..." >> $LOG_FILE

    # Run notebook and stop on error using || 
    jupyter nbconvert --execute --to notebook "$nb" --output "output/${nb}" --ExecutePreprocessor.timeout=600 || {
        echo "ERROR: $nb failed." >> $LOG_FILE
        echo "Pipeline stopped due to failure in $nb."
        exit 1
    }

    echo "$nb completed successfully." >> $LOG_FILE
done

echo "Pipeline completed successfully at $(date)!" >> $LOG_FILE

# TODO: Run analysis notebooks in order (q4-q7) using nbconvert with error handling
# Use either `$?` or `||` operator to check exit codes and stop on failure
# Add a log entry for each notebook execution or failure
# jupyter nbconvert --execute --to notebook q4_exploration.ipynb

