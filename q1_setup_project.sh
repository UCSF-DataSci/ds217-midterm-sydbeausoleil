#!/bin/bash

# TODO: Add shebang line: #!/bin/bash
# Assignment 5, Question 1: Project Setup Script
# This script creates the directory structure for the clinical trial analysis project
# TODO: Make this script executable (if not already)
# chmod +x q1_setup_project.sh

# TODO: Create the following directories:
#   - data/
#   - output/
#   - reports/

# TODO: Generate the dataset
#       Run: python3 generate_data.py
#       This creates data/clinical_trial_raw.csv with 10,000 patients

# TODO: Save the directory structure to reports/directory_structure.txt
#       Hint: Use 'ls -la' or 'tree' command

set -e

mkdir -p data
mkdir -p output
mkdir -p reports

echo "Generating clinical trial dataset..."
python3 generate_data.py

if [ -f "data/clinical_trial_raw.csv" ]; then
    echo "Dataset generated successfully: data/clinical_trial_raw.csv"
else
    echo "Dataset generation failed."
    exit 1
fi

echo "Saving directory structure to reports/directory_structure.txt..."
if command -v tree &> /dev/null
then
    tree > reports/directory_structure.txt
else
    ls -R > reports/directory_structure.txt
fi

echo  "Project setup complete. Directory structure saved in reports/directory_structure.txt."