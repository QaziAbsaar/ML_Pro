from __future__ import annotations

import argparse
import json
from pathlib import Path

import joblib
import numpy as np
from sklearn.exceptions import ConvergenceWarning
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from taxi_fare import (
    FEATURE_COLUMNS,
    format_metrics,
    load_dataset,
    prepare_training_frame,
)

import warnings

warnings.filterwarnings("ignore", category=ConvergenceWarning)


def build_model(random_state: int = 42) -> Pipeline:
    return Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            (
                "ann",
                MLPRegressor(
                    hidden_layer_sizes=(128, 64, 32),
                    activation="relu",
                    solver="adam",
                    alpha=0.0001,
                    batch_size=1024,
                    learning_rate_init=0.001,
                    max_iter=120,
                    early_stopping=True,
                    validation_fraction=0.15,
                    n_iter_no_change=12,
                    random_state=random_state,
                    verbose=False,
                ),
            ),
        ]
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Train an ANN fare prediction model on NYC Taxi Fare Prediction data.")
    parser.add_argument("--data", type=str, default="data/nyc_taxi_fare.csv", help="Path to the dataset CSV.")
    parser.add_argument("--sample-size", type=int, default=200000, help="Optional training sample size.")
    parser.add_argument("--output-dir", type=str, default="artifacts", help="Directory for model artifacts.")
    parser.add_argument("--random-state", type=int, default=42, help="Random seed.")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    raw = load_dataset(args.data, sample_size=args.sample_size, random_state=args.random_state)
    features, target, stats = prepare_training_frame(raw)

    x_train, x_test, y_train, y_test = train_test_split(
        features,
        target,
        test_size=0.2,
        random_state=args.random_state,
    )

    model = build_model(random_state=args.random_state)
    model.fit(x_train, y_train)

    predictions = model.predict(x_test)
    mse = mean_squared_error(y_test, predictions)
    metrics = {
        "mae": mean_absolute_error(y_test, predictions),
        "rmse": float(np.sqrt(mse)),
        "r2": r2_score(y_test, predictions),
    }

    joblib.dump(model, output_dir / "taxi_fare_ann_model.joblib")
    (output_dir / "metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    (output_dir / "training_summary.txt").write_text(
        "\n".join(
            [
                f"feature_columns: {FEATURE_COLUMNS}",
                f"rows_before_cleaning: {stats.rows_before}",
                f"rows_after_cleaning: {stats.rows_after}",
                f"rows_dropped: {stats.rows_dropped}",
                format_metrics(metrics),
            ]
        ),
        encoding="utf-8",
    )

    print("Training complete")
    print(format_metrics(metrics))
    print(f"Saved model to {output_dir / 'taxi_fare_ann_model.joblib'}")


if __name__ == "__main__":
    main()
