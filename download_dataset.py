#!/usr/bin/env python3
"""
Download NYC Taxi Fare Prediction dataset from Kaggle.

This script uses the Kaggle API to download the dataset.
Make sure your Kaggle API credentials are set up in ~/.kaggle/kaggle.json

To set up credentials:
1. Go to https://www.kaggle.com/settings/account
2. Click "Create New API Token" to download kaggle.json
3. Place it in ~/.kaggle/kaggle.json
"""

import os
import sys
from pathlib import Path


def download_dataset():
    """Download the NYC Taxi Fare Prediction dataset from Kaggle."""
    dataset_name = "nyc-taxi-fare-prediction"
    output_dir = Path("data")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Check if Kaggle API is available
    try:
        from kaggle.api.kaggle_api_extended import KaggleApi
    except ImportError:
        print("Error: kaggle package not installed.")
        print("Install it with: pip install kaggle")
        sys.exit(1)

    # Check if Kaggle credentials are set up
    kaggle_json = Path.home() / ".kaggle" / "kaggle.json"
    if not kaggle_json.exists():
        print("Error: Kaggle credentials not found at ~/.kaggle/kaggle.json")
        print("\nTo set up credentials:")
        print("1. Go to https://www.kaggle.com/settings/account")
        print("2. Click 'Create New API Token' to download kaggle.json")
        print("3. Place it in ~/.kaggle/kaggle.json")
        sys.exit(1)

    # Authenticate and download
    api = KaggleApi()
    api.authenticate()

    print(f"Downloading {dataset_name} dataset...")
    try:
        api.dataset_download_files(dataset_name, path=output_dir, unzip=True)
        print(f"✓ Dataset downloaded to {output_dir}/")
    except Exception as e:
        print(f"Error downloading dataset: {e}")
        sys.exit(1)


def verify_dataset():
    """Verify that the dataset was downloaded correctly."""
    csv_files = list(Path("data").glob("*.csv"))
    if not csv_files:
        print("Error: No CSV files found in data/ directory")
        return False

    print(f"Found {len(csv_files)} CSV file(s):")
    for f in csv_files:
        size_mb = f.stat().st_size / (1024 * 1024)
        print(f"  - {f.name} ({size_mb:.2f} MB)")

    return True


if __name__ == "__main__":
    download_dataset()
    if verify_dataset():
        print("\n✓ Dataset ready for training!")
