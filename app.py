from __future__ import annotations

from pathlib import Path

import gradio as gr
import joblib

from taxi_fare import prepare_inference_frame

MODEL_PATH = Path("artifacts/taxi_fare_ann_model.joblib")


def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model file not found at {MODEL_PATH}. Train the model first with train.py."
        )
    return joblib.load(MODEL_PATH)


try:
    model = load_model()
except FileNotFoundError:
    model = None


def predict_fare(pickup_datetime, pickup_longitude, pickup_latitude, dropoff_longitude, dropoff_latitude, passenger_count):
    if model is None:
        raise gr.Error("Model file is missing. Train the model first and place artifacts/taxi_fare_ann_model.joblib in the project.")

    features = prepare_inference_frame(
        pickup_datetime=pickup_datetime,
        pickup_longitude=pickup_longitude,
        pickup_latitude=pickup_latitude,
        dropoff_longitude=dropoff_longitude,
        dropoff_latitude=dropoff_latitude,
        passenger_count=passenger_count,
    )
    prediction = float(model.predict(features)[0])
    return round(max(prediction, 0.0), 2)


with gr.Blocks() as demo:
    gr.Markdown(
        """
        # NYC Taxi Fare Prediction
        Predict taxi fare using an Artificial Neural Network trained on the NYC Taxi Fare Prediction dataset.
        """
    )

    with gr.Row():
        pickup_datetime = gr.Textbox(
            label="Pickup datetime",
            value="2015-01-01 12:00:00",
            placeholder="YYYY-MM-DD HH:MM:SS",
        )
        passenger_count = gr.Number(label="Passenger count", value=1, precision=0)

    with gr.Row():
        pickup_longitude = gr.Number(label="Pickup longitude", value=-73.985428)
        pickup_latitude = gr.Number(label="Pickup latitude", value=40.748817)

    with gr.Row():
        dropoff_longitude = gr.Number(label="Dropoff longitude", value=-73.985130)
        dropoff_latitude = gr.Number(label="Dropoff latitude", value=40.758896)

    predict_button = gr.Button("Predict Fare")
    output = gr.Number(label="Predicted fare amount ($)")

    predict_button.click(
        fn=predict_fare,
        inputs=[
            pickup_datetime,
            pickup_longitude,
            pickup_latitude,
            dropoff_longitude,
            dropoff_latitude,
            passenger_count,
        ],
        outputs=output,
    )

    gr.Examples(
        examples=[
            ["2015-01-01 12:00:00", -73.985428, 40.748817, -73.985130, 40.758896, 1],
            ["2015-06-18 18:30:00", -73.985656, 40.758896, -73.971249, 40.7831, 2],
        ],
        inputs=[
            pickup_datetime,
            pickup_longitude,
            pickup_latitude,
            dropoff_longitude,
            dropoff_latitude,
            passenger_count,
        ],
        label="Sample trips",
    )


if __name__ == "__main__":
    demo.launch(theme=gr.themes.Soft(), title="NYC Taxi Fare Prediction")
