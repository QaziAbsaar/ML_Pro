#!/usr/bin/env python3
"""
Generate synthetic NYC Taxi Fare dataset for testing and development.

This script creates a realistic synthetic dataset that matches the structure
of the actual NYC Taxi Fare Prediction dataset from Kaggle.

Use this for testing locally before training on the full dataset.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path


def generate_synthetic_taxi_data(n_samples=100000, random_state=42) -> pd.DataFrame:
    """
    Generate synthetic NYC taxi fare data.

    Parameters:
    -----------
    n_samples : int
        Number of records to generate (default: 100,000)
    random_state : int
        Random seed for reproducibility

    Returns:
    --------
    pd.DataFrame
        Synthetic dataset with columns matching the NYC Taxi Fare dataset
    """
    np.random.seed(random_state)

    # NYC bounding box
    nyc_lat_min, nyc_lat_max = 40.6, 40.85
    nyc_lon_min, nyc_lon_max = -74.0, -73.8

    # Generate dates within 2015
    start_date = datetime(2015, 1, 1)
    dates = [start_date + timedelta(days=int(d)) for d in np.random.randint(0, 365, n_samples)]
    
    # Add realistic time variation
    hours = np.random.normal(12, 6, n_samples).astype(int) % 24
    minutes = (np.random.randint(0, 60, n_samples)).astype(int)
    seconds = (np.random.randint(0, 60, n_samples)).astype(int)
    
    pickup_datetime = []
    for date, hour, minute, second in zip(dates, hours, minutes, seconds):
        pickup_datetime.append(date.replace(hour=hour, minute=minute, second=second))

    # Geographic coordinates (pickup and dropoff)
    pickup_lon = np.random.uniform(nyc_lon_min, nyc_lon_max, n_samples)
    pickup_lat = np.random.uniform(nyc_lat_min, nyc_lat_max, n_samples)
    
    # Dropoff locations nearby (realistic trips)
    noise_lon = np.random.normal(0, 0.05, n_samples)
    noise_lat = np.random.normal(0, 0.05, n_samples)
    
    dropoff_lon = np.clip(pickup_lon + noise_lon, nyc_lon_min, nyc_lon_max)
    dropoff_lat = np.clip(pickup_lat + noise_lat, nyc_lat_min, nyc_lat_max)

    # Passenger count (1-6, with most being 1-2)
    passenger_count = np.random.choice([1, 2, 3, 4, 5, 6], n_samples, p=[0.7, 0.15, 0.08, 0.04, 0.02, 0.01])

    # Calculate distance-based fare with some randomness
    from taxi_fare import haversine_km
    distances = haversine_km(pickup_lat, pickup_lon, dropoff_lat, dropoff_lon)
    
    # Base fare + distance fee + passenger multiplier + random variation
    base_fare = 2.5
    distance_rate = 2.5  # $ per km
    time_variation = np.random.normal(1.0, 0.2, n_samples)  # Time-based variation (peak vs off-peak)
    noise = np.random.normal(0, 1.5, n_samples)  # Random noise
    
    fare_amount = (base_fare + (distances * distance_rate) + (passenger_count * 0.5) * 
                   time_variation + noise).clip(min=2.5)

    df = pd.DataFrame({
        "key": [f"{i:06d}" for i in range(n_samples)],
        "fare_amount": fare_amount,
        "pickup_datetime": pickup_datetime,
        "pickup_longitude": pickup_lon,
        "pickup_latitude": pickup_lat,
        "dropoff_longitude": dropoff_lon,
        "dropoff_latitude": dropoff_lat,
        "passenger_count": passenger_count,
    })

    return df


def main():
    """Generate and save synthetic dataset."""
    output_path = Path("data/nyc_taxi_fare.csv")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print("Generating synthetic NYC Taxi Fare dataset...")
    df = generate_synthetic_taxi_data(n_samples=100000)
    
    print(f"Saving to {output_path}...")
    df.to_csv(output_path, index=False)
    
    print(f"✓ Synthetic dataset created: {output_path}")
    print(f"  Shape: {df.shape}")
    print(f"  Columns: {list(df.columns)}")
    print(f"\nDataset info:")
    print(df.info())
    print(f"\nDataset sample:")
    print(df.head())


if __name__ == "__main__":
    main()
