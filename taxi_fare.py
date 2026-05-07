from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd

REQUIRED_RAW_COLUMNS = [
    "pickup_datetime",
    "pickup_longitude",
    "pickup_latitude",
    "dropoff_longitude",
    "dropoff_latitude",
    "passenger_count",
]

FEATURE_COLUMNS = [
    "passenger_count",
    "pickup_hour",
    "pickup_day_of_week",
    "pickup_month",
    "pickup_year",
    "is_weekend",
    "trip_distance_km",
    "abs_lat_diff",
    "abs_lon_diff",
]

NYC_LAT_BOUNDS = (40.0, 42.0)
NYC_LON_BOUNDS = (-75.5, -72.5)
FARE_BOUNDS = (0.0, 500.0)


@dataclass(frozen=True)
class DatasetStats:
    rows_before: int
    rows_after: int
    rows_dropped: int


def haversine_km(lat1, lon1, lat2, lon2):
    """Vectorized haversine distance in kilometers."""
    earth_radius_km = 6371.0088
    lat1_rad = np.radians(lat1)
    lon1_rad = np.radians(lon1)
    lat2_rad = np.radians(lat2)
    lon2_rad = np.radians(lon2)

    delta_lat = lat2_rad - lat1_rad
    delta_lon = lon2_rad - lon1_rad
    a = np.sin(delta_lat / 2.0) ** 2 + np.cos(lat1_rad) * np.cos(lat2_rad) * np.sin(delta_lon / 2.0) ** 2
    return 2.0 * earth_radius_km * np.arcsin(np.sqrt(a))


def _to_datetime(series: pd.Series) -> pd.Series:
    return pd.to_datetime(series, errors="coerce", utc=False)


def clean_raw_data(df: pd.DataFrame) -> tuple[pd.DataFrame, DatasetStats]:
    rows_before = len(df)
    data = df.copy()

    data = data.dropna(subset=REQUIRED_RAW_COLUMNS + ["fare_amount"])
    data = data[data["fare_amount"].between(*FARE_BOUNDS)]
    data = data[data["passenger_count"].between(1, 8)]

    data["pickup_datetime"] = _to_datetime(data["pickup_datetime"])
    data = data.dropna(subset=["pickup_datetime"])

    lat_mask = (
        data["pickup_latitude"].between(*NYC_LAT_BOUNDS)
        & data["dropoff_latitude"].between(*NYC_LAT_BOUNDS)
    )
    lon_mask = (
        data["pickup_longitude"].between(*NYC_LON_BOUNDS)
        & data["dropoff_longitude"].between(*NYC_LON_BOUNDS)
    )
    data = data[lat_mask & lon_mask]

    data = data[data["pickup_latitude"] != data["dropoff_latitude"]]
    data = data[data["pickup_longitude"] != data["dropoff_longitude"]]

    rows_after = len(data)
    return data.reset_index(drop=True), DatasetStats(rows_before, rows_after, rows_before - rows_after)


def add_time_and_distance_features(df: pd.DataFrame) -> pd.DataFrame:
    data = df.copy()
    pickup_datetime = _to_datetime(data["pickup_datetime"])

    data["pickup_hour"] = pickup_datetime.dt.hour.fillna(0).astype(int)
    data["pickup_day_of_week"] = pickup_datetime.dt.dayofweek.fillna(0).astype(int)
    data["pickup_month"] = pickup_datetime.dt.month.fillna(0).astype(int)
    data["pickup_year"] = pickup_datetime.dt.year.fillna(0).astype(int)
    data["is_weekend"] = (pickup_datetime.dt.dayofweek >= 5).astype(int)
    data["trip_distance_km"] = haversine_km(
        data["pickup_latitude"],
        data["pickup_longitude"],
        data["dropoff_latitude"],
        data["dropoff_longitude"],
    )
    data["abs_lat_diff"] = (data["pickup_latitude"] - data["dropoff_latitude"]).abs()
    data["abs_lon_diff"] = (data["pickup_longitude"] - data["dropoff_longitude"]).abs()

    return data[FEATURE_COLUMNS].astype(float)


def load_dataset(dataset_path: str | Path, sample_size: int | None = None, random_state: int = 42) -> pd.DataFrame:
    path = Path(dataset_path)
    if not path.exists():
        raise FileNotFoundError(
            f"Dataset not found at {path}. Place the NYC Taxi Fare Prediction CSV there and retry."
        )

    df = pd.read_csv(path)
    if sample_size is not None and len(df) > sample_size:
        df = df.sample(n=sample_size, random_state=random_state).reset_index(drop=True)
    return df


def prepare_training_frame(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series, DatasetStats]:
    cleaned, stats = clean_raw_data(df)
    features = add_time_and_distance_features(cleaned)
    target = cleaned["fare_amount"].astype(float).reset_index(drop=True)
    return features.reset_index(drop=True), target, stats


def prepare_inference_frame(
    pickup_datetime: str,
    pickup_longitude: float,
    pickup_latitude: float,
    dropoff_longitude: float,
    dropoff_latitude: float,
    passenger_count: int,
) -> pd.DataFrame:
    raw = pd.DataFrame(
        [
            {
                "pickup_datetime": pickup_datetime,
                "pickup_longitude": pickup_longitude,
                "pickup_latitude": pickup_latitude,
                "dropoff_longitude": dropoff_longitude,
                "dropoff_latitude": dropoff_latitude,
                "passenger_count": passenger_count,
            }
        ]
    )
    return add_time_and_distance_features(raw)


def format_metrics(metrics: dict[str, float]) -> str:
    return "\n".join(f"{key}: {value:.4f}" for key, value in metrics.items())
