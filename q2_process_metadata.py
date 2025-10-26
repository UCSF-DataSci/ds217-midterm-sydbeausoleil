#!/usr/bin/env python3
# Assignment 5, Question 2: Python Data Processing
# Process configuration files for data generation.

import random
import statistics
import os

def parse_config(filepath: str) -> dict:
    """
    Parse config file (key=value format) into dictionary.
    """
    config = {}
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if line and '=' in line:  # ignore empty lines or comments
                key, value = line.split('=', 1)
                config[key.strip()] = value.strip()
    return config


def validate_config(config: dict) -> dict:
    """
    Validate configuration values using if/elif/else logic.
    Rules:
      - sample_data_rows must be an int and > 0
      - sample_data_min must be an int and >= 1
      - sample_data_max must be an int and > sample_data_min
    """
    results = {}

    try:
        rows = int(config.get('sample_data_rows', 0))
        results['sample_data_rows'] = rows > 0
    except ValueError:
        results['sample_data_rows'] = False

    try:
        min_val = int(config.get('sample_data_min', 0))
        results['sample_data_min'] = min_val >= 1
    except ValueError:
        results['sample_data_min'] = False

    try:
        max_val = int(config.get('sample_data_max', 0))
        results['sample_data_max'] = max_val > int(config.get('sample_data_min', 0))
    except ValueError:
        results['sample_data_max'] = False

    return results


def generate_sample_data(filename: str, config: dict) -> None:
    """
    Generate a file with random numbers for testing, one number per row with no header.
    Uses config parameters for number of rows and range.
    """
    rows = int(config['sample_data_rows'])
    min_val = int(config['sample_data_min'])
    max_val = int(config['sample_data_max'])

    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w') as f:
        for _ in range(rows):
            f.write(str(random.randint(min_val, max_val)) + '\n')


def calculate_statistics(data: list) -> dict:
    """
    Calculate basic statistics.
    """
    count = len(data)
    total = sum(data)
    mean = statistics.mean(data) if count > 0 else 0
    median = statistics.median(data) if count > 0 else 0

    return {'mean': mean, 'median': median, 'sum': total, 'count': count}


if __name__ == '__main__':
    config = parse_config('q2_config.txt')
    validation = validate_config(config)
    print("Validation Results:", validation)

    if not all(validation.values()):
        print("❌ Invalid configuration. Please fix q2_config.txt and rerun.")
        exit(1)

    sample_file = 'data/sample_data.csv'
    generate_sample_data(sample_file, config)
    print(f"Sample data generated in {sample_file}")

    with open(sample_file, 'r') as f:
        data = [int(line.strip()) for line in f if line.strip().isdigit()]

    stats = calculate_statistics(data)

    os.makedirs('output', exist_ok=True)
    with open('output/statistics.txt', 'w') as f:
        for key, value in stats.items():
            f.write(f"{key}: {value}\n")

    print("Statistics saved to output/statistics.txt")
