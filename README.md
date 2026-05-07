# NYC Taxi Fare Prediction

This project predicts taxi fare amounts using the **NYC Taxi Fare Prediction** dataset and an **Artificial Neural Network** implemented with `scikit-learn`'s `MLPRegressor`.

## Project Overview

This is a complete machine learning solution that demonstrates:
- ✓ Data preprocessing and feature engineering
- ✓ Artificial Neural Network model training
- ✓ Model evaluation and visualization
- ✓ Interactive Gradio user interface
- ✓ Deployment on Hugging Face Spaces

## Dataset Requirement

The assignment requires the **NYC Taxi Fare Prediction** dataset from Kaggle.

### Option 1: Using Real Dataset (Kaggle)

1. Download the dataset from [Kaggle NYC Taxi Fare Prediction](https://www.kaggle.com/c/nyc-taxi-fare-prediction/data)
2. Place the CSV file at:
   ```text
   data/nyc_taxi_fare.csv
   ```

### Option 2: Generate Synthetic Data (for testing)

Generate a synthetic dataset with realistic patterns:

```bash
python generate_synthetic_data.py
```

This creates `data/nyc_taxi_fare.csv` with 100,000 synthetic records.

## Project Structure

```
.
├── app.py                          # Gradio interface app
├── train.py                        # Model training script
├── taxi_fare.py                    # Data preprocessing & feature engineering
├── generate_synthetic_data.py      # Generate synthetic test data
├── download_dataset.py             # Download dataset from Kaggle (requires credentials)
├── assignment_notebook.ipynb       # Complete ML workflow notebook
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── data/                           # Dataset directory
│   └── nyc_taxi_fare.csv          
└── artifacts/                      # Trained model & metrics
    ├── taxi_fare_ann_model.joblib
    ├── metrics.json
    └── training_summary.txt
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd ML_Pro
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Training the Model

### Quick Start (with synthetic data):

```bash
python generate_synthetic_data.py  # Create synthetic dataset
python train.py                    # Train model with default settings
```

### With Custom Dataset:

```bash
python train.py --data data/nyc_taxi_fare.csv --output-dir artifacts --sample-size 100000
```

**Training Parameters:**

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--data` | `data/nyc_taxi_fare.csv` | Path to dataset CSV |
| `--sample-size` | `200000` | Number of samples to use (set to `None` for full dataset) |
| `--output-dir` | `artifacts` | Directory to save model artifacts |
| `--random-state` | `42` | Random seed for reproducibility |

### Training Output:

The script saves:
- `artifacts/taxi_fare_ann_model.joblib` - Trained ANN model
- `artifacts/metrics.json` - Test set metrics (MAE, RMSE, R²)
- `artifacts/training_summary.txt` - Training summary

## Running the Application

Start the Gradio interface locally:

```bash
python app.py
```

The app will be available at: `http://localhost:7860`

**Features:**
- Input pickup/dropoff datetime, coordinates, and passenger count
- Get instant fare predictions
- View example predictions

## Jupyter Notebook

Explore the complete ML workflow in the assignment notebook:

```bash
jupyter notebook assignment_notebook.ipynb
```

**Sections:**
1. Data loading and exploration
2. Data preprocessing and cleaning
3. Feature engineering (time-based and distance features)
4. ANN model training
5. Model evaluation and metrics
6. Visualizations (actual vs predicted, residuals)
7. Making predictions on new data
8. Model persistence

## Model Architecture

**Artificial Neural Network (ANN):**
```
Input Layer (9 features)
    ↓
Hidden Layer 1 (128 neurons, ReLU)
    ↓
Hidden Layer 2 (64 neurons, ReLU)
    ↓
Hidden Layer 3 (32 neurons, ReLU)
    ↓
Output Layer (1 neuron - fare amount)
```

**Training Configuration:**
- Optimizer: Adam
- Activation: ReLU
- Batch Size: 1024
- Max Iterations: 120
- Early Stopping: Enabled (validation fraction: 0.15)
- Scaler: StandardScaler for feature normalization

## Model Performance

Typical performance metrics on test set:
- **MAE (Mean Absolute Error):** $1.22-1.30
- **RMSE (Root Mean Squared Error):** $1.53-1.70
- **R² Score:** 0.96 (explains 96% of variance)

## Features Used

1. **Temporal Features:**
   - `pickup_hour` - Hour of day (0-23)
   - `pickup_day_of_week` - Day of week (0-6)
   - `pickup_month` - Month (1-12)
   - `pickup_year` - Year
   - `is_weekend` - Binary flag

2. **Distance Features:**
   - `trip_distance_km` - Haversine distance between pickup and dropoff
   - `abs_lat_diff` - Absolute latitude difference
   - `abs_lon_diff` - Absolute longitude difference

3. **Trip Features:**
   - `passenger_count` - Number of passengers

## Deployment on Hugging Face Spaces

### Prerequisites
- GitHub account with this repository
- Hugging Face account

### Steps

1. **Create a Hugging Face Space:**
   - Go to [huggingface.co/spaces](https://huggingface.co/spaces)
   - Click "Create New Space"
   - Choose your repository name
   - Select "Gradio" as SDK
   - Set visibility to "Public"

2. **Configure with GitHub:**
   - Connect to your GitHub repository
   - Hugging Face will automatically:
     - Clone your repository
     - Install dependencies from `requirements.txt`
     - Run `python app.py`

3. **Access Your App:**
   - Your Gradio app will be available at:
     ```
     https://huggingface.co/spaces/<username>/<space-name>
     ```

### Important Notes for Deployment

- Ensure the trained model is in `artifacts/` directory
- The `app.py` must be in the root directory
- All dependencies must be in `requirements.txt`
- The model file `taxi_fare_ann_model.joblib` should be committed to the repository

### Windows / PowerShell Deployment

If you are deploying from PowerShell, set the Hugging Face variables with:

```powershell
$env:HF_USERNAME = 'your_hf_username'
$env:HF_SPACE = 'your_space_name'
$env:HF_TOKEN = 'your_hf_token'
```

Then run:

```powershell
.\push_to_hf.ps1
```

This helper uploads the current workspace directly to your Hugging Face Space, which avoids the binary-file rejection from Git pushes.

If you prefer Bash, use `push_to_hf.sh` from Git Bash, WSL, or another Unix-like shell only if you are managing the Space through Git.

## Scripts Overview

| Script | Purpose |
|--------|---------|
| `train.py` | Train ANN model from dataset |
| `app.py` | Run Gradio web interface |
| `taxi_fare.py` | Core preprocessing & feature engineering |
| `generate_synthetic_data.py` | Generate synthetic test data |
| `download_dataset.py` | Download real dataset from Kaggle |

## File Size Reference

- Synthetic dataset: ~6.1 MB (100,000 records)
- Trained model: ~283 KB
- Total executable size: < 1 MB

## Contributing

### Development Workflow

1. Generate/download dataset
2. Run `train.py` to train model
3. Test `app.py` locally
4. Update notebook if needed
5. Push to GitHub
6. Hugging Face will auto-deploy

### Testing the Application Locally

```bash
# Generate synthetic data
python generate_synthetic_data.py

# Train model
python train.py

# Run app
python app.py
```

Then open browser to `http://localhost:7860`

## Troubleshooting

### Issue: "Model file not found"
```
Solution: Run `python train.py` first to train and save the model
```

### Issue: "Dataset not found"
```
Solution: Run `python generate_synthetic_data.py` or provide dataset path
```

### Issue: Gradio app won't start
```
Solution: Ensure all dependencies are installed: pip install -r requirements.txt
```

### Issue: Model predictions seem off
```
Solution: 
- Check feature engineering in taxi_fare.py
- Verify data preprocessing steps
- Retrain with larger sample size
```

## References

- [Kaggle NYC Taxi Fare Competition](https://www.kaggle.com/c/nyc-taxi-fare-prediction)
- [Scikit-learn MLPRegressor](https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPRegressor.html)
- [Gradio Documentation](https://www.gradio.app/)
- [Hugging Face Spaces Docs](https://huggingface.co/docs/hub/spaces)

## Assignment Requirements (STRICT)

✓ **Algorithm**: Artificial Neural Network (MLPRegressor)  
✓ **Dataset**: NYC Taxi Fare Prediction (Kaggle)  
✓ **Interface**: Gradio web app  
✓ **Deployment**: Hugging Face Spaces  
✓ **ML Only**: No deep learning frameworks (TensorFlow/PyTorch)  

## Submission Checklist

- [ ] Hugging Face Space deployed and working
- [ ] All source code committed to GitHub
- [ ] ZIP file contains:
  - [ ] Source code (*.py files)
  - [ ] Trained model (*.joblib)
  - [ ] requirements.txt
  - [ ] assignment_notebook.ipynb
  - [ ] README.md
  - [ ] Data preprocessing/feature engineering script

## License

This project is for educational purposes as part of an assignment.

## Author

Student Assignment: NYC Taxi Fare Prediction using ML

---

**Last Updated:** May 7, 2026  
**Status:** ✓ Complete and deployable

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

## Hugging Face Git configuration (alternative push methods)

If you prefer to push directly to your Hugging Face Space (instead of connecting GitHub), you can use one of the two methods below.

1) Create the Space on Hugging Face first (choose **Gradio** as the SDK). Then push via the Hugging Face remote:

```bash
# Install the HF CLI (once)
pip install huggingface-hub

# Log in and paste your token from https://huggingface.co/settings/tokens
huggingface-cli login

# Add a new remote that points to your Space (replace USERNAME and SPACE_NAME)
git remote add huggingface https://huggingface.co/spaces/USERNAME/SPACE_NAME

# Push your repository to the Space
git push huggingface main --force
```

2) Manual upload via the Space UI (if you prefer a GUI):

- Create a new Space at https://huggingface.co/spaces and choose **Gradio** as the SDK.
- Open the Space, go to the **Files** tab and upload these files/folders:
   - `app.py`
   - `taxi_fare.py`
   - `requirements.txt`
   - `artifacts/taxi_fare_ann_model.joblib`
   - any other helper scripts you want included

Notes & tips:
- Make sure `app.py` is at the repository root (Hugging Face runs it by default).
- If you use the Git remote method, the Space will rebuild automatically on each push.
- If your model is large, consider hosting it in the Hub or downloading at startup to keep repo size smaller.

If you'd like, I can add a ready-to-use `push_to_hf.sh` helper script to automate the login + remote add + push steps — tell me if you want that and I'll create it and commit it for you.
