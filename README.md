# NYC Taxi Fare Prediction

This project predicts taxi fare amounts using the **NYC Taxi Fare Prediction** dataset and an **Artificial Neural Network** implemented with `scikit-learn`'s `MLPRegressor`.

## What is included

- Data preprocessing and feature engineering
- ANN model training for fare prediction
- Gradio user interface for live predictions
- Hugging Face Spaces deployment entrypoint
- Notebook-style documentation for submission

## Dataset requirement

The assignment requires the **NYC Taxi Fare Prediction** dataset.

Place the CSV file at:

```text
data/nyc_taxi_fare.csv
```

If your file has a different name, pass it with `--data` when training.

## Files

- `train.py` trains the ANN and saves the model
- `app.py` runs the Gradio interface
- `taxi_fare.py` contains preprocessing and feature engineering
- `requirements.txt` lists dependencies
- `assignment_notebook.ipynb` documents the workflow

## Train the model

```bash
python train.py --data data/nyc_taxi_fare.csv --output-dir artifacts
```

This saves:

- `artifacts/taxi_fare_ann_model.joblib`
- `artifacts/metrics.json`
- `artifacts/training_summary.txt`

## Run the app locally

```bash
python app.py
```

## Hugging Face deployment

Use this folder as a Gradio Space and upload:

- `app.py`
- `taxi_fare.py`
- `requirements.txt`
- `artifacts/taxi_fare_ann_model.joblib`

## Notes

- The model uses feature engineering for pickup time and trip distance.
- The implementation follows the assignment requirement by using an ANN rather than tree-based models.
- Because the dataset can be large and noisy, the training script includes cleaning and optional sampling.
