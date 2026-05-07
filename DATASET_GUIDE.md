# NYC Taxi Fare Dataset Guide

This guide explains how to properly obtain and set up the NYC Taxi Fare Prediction dataset.

## Dataset Information

- **Name**: NYC Taxi Fare Prediction
- **Source**: Kaggle Competition
- **Records**: ~55 million records (2.63 GB)
- **Time Period**: 2009-2015
- **Link**: https://www.kaggle.com/c/nyc-taxi-fare-prediction/data

## Option 1: Download from Kaggle (Recommended for Production)

### Prerequisites

1. **Kaggle Account**
   - Sign up at https://www.kaggle.com
   - Free account is sufficient

2. **Kaggle API Setup**
   
   Install kaggle CLI:
   ```bash
   pip install kaggle
   ```

### Step-by-Step Setup

#### 1. Get Your Kaggle Credentials

1. Go to https://www.kaggle.com/settings/account
2. Click "Create New API Token"
3. This downloads `kaggle.json`

#### 2. Place Credentials

**On Linux/Mac:**
```bash
mkdir -p ~/.kaggle
cp kaggle.json ~/.kaggle/
chmod 600 ~/.kaggle/kaggle.json
```

**On Windows:**
```
Place kaggle.json in: C:\Users\<YourUsername>\.kaggle\
```

#### 3. Download the Dataset

**Method A: Using the provided script**

```bash
cd ML_Pro
python download_dataset.py
```

This:
- Authenticates with Kaggle
- Downloads the official dataset
- Extracts to `data/` directory
- Validates file structure

**Method B: Using Kaggle CLI directly**

```bash
kaggle competitions download -c nyc-taxi-fare-prediction
unzip -d data/ nyc-taxi-fare-prediction.zip
```

**Method C: Manual download**

1. Visit: https://www.kaggle.com/c/nyc-taxi-fare-prediction/data
2. Click "Download All"
3. Extract contents to `data/` folder

### Verify Download

After download, verify the dataset:

```bash
# Check file exists
ls -lh data/

# Check CSV structure
head -5 data/train.csv

# Check row count (takes 1-2 minutes)
wc -l data/train.csv
```

Expected output:
```
-rw-r--r--  1 user  staff  2.6G  May  7 12:34 train.csv
```

## Option 2: Generate Synthetic Data (Quick Testing)

For quick testing without downloading the large dataset:

```bash
python generate_synthetic_data.py
```

This creates: `data/nyc_taxi_fare.csv` (100,000 records, ~6 MB)

**Advantages:**
- ✓ Instant generation (< 30 seconds)
- ✓ No large download required
- ✓ Realistic data structure
- ✓ Good for prototyping

**Disadvantages:**
- ✗ Not real historical data
- ✗ Smaller dataset (100K vs 55M records)
- ✗ For assignment validation only

## Option 3: Sample Dataset (Medium Size)

For intermediate testing with real data:

```bash
# Download and sample first 500K rows
head -500001 data/train.csv > data/train_sample.csv

# Or use Python
python -c "
import pandas as pd
df = pd.read_csv('data/train.csv', nrows=500000)
df.to_csv('data/train_sample.csv', index=False)
"
```

## Dataset Format

### Columns (Expected)

| Column | Type | Description |
|--------|------|-------------|
| `key` | string | Unique identifier |
| `fare_amount` | float | Taxi fare ($) - **TARGET** |
| `pickup_datetime` | string | Pickup timestamp |
| `pickup_longitude` | float | Pickup location longitude |
| `pickup_latitude` | float | Pickup location latitude |
| `dropoff_longitude` | float | Dropoff location longitude |
| `dropoff_latitude` | float | Dropoff location latitude |
| `passenger_count` | int | Number of passengers |

### Example Row

```csv
key,fare_amount,pickup_datetime,pickup_longitude,pickup_latitude,dropoff_longitude,dropoff_latitude,passenger_count
2015-03-25 07:30:35.000000107,14.5,2015-03-25 07:30:35 UTC,-73.999619,40.734462,-73.988403,40.733444,1
```

## Data Characteristics

### Statistics

- **Fare Range**: $0 - $500
- **Passenger Range**: 1 - 8
- **Time Span**: 2009-2015 (mostly 2015)
- **Records**: ~55 million

### Quality Issues (Handled by preprocessing)

- **Missing Values**: Some records have NaN coordinates
- **Outliers**: Some fares exceed typical NYC prices
- **Duplicates**: May exist in raw data
- **Invalid Coordinates**: Out of NYC bounds

Our `taxi_fare.py` preprocessing handles all these issues.

## Troubleshooting

### Issue: Kaggle authentication fails

```
Error: Kaggle API not installed
Solution: pip install kaggle
```

```
Error: ~/.kaggle/kaggle.json not found
Solution: Download from https://www.kaggle.com/settings/account
```

### Issue: Dataset download is slow

**Solution:**
- Kaggle isn't always fast; patience required
- Alternative: Try Method C (manual download)
- Or use the synthetic data (`generate_synthetic_data.py`)

### Issue: Disk space insufficient

- Full dataset: ~2.6 GB
- After processing: ~500 MB
- Ensure you have 5 GB free space

**Solution if low on space:**
```bash
# Use only first 100K rows for training
python train.py --sample-size 100000
```

### Issue: File corruption during download

Try re-downloading:
```bash
rm data/train.csv
python download_dataset.py
```

## File Paths (Important)

The training script expects the dataset at:

```
data/nyc_taxi_fare.csv  ← This is the expected location
```

If your file has a different name:

```bash
# Rename it
mv data/train.csv data/nyc_taxi_fare.csv

# Or specify in training
python train.py --data data/train.csv
```

## Assignment Submission Note

**IMPORTANT**: For assignment submission, ensure:

1. ✓ The dataset used is NYC Taxi Fare Prediction
2. ✓ Source: Kaggle (https://www.kaggle.com/c/nyc-taxi-fare-prediction)
3. ✓ Documentation of which dataset split was used
4. ✓ Reproducible preprocessing

This ensures compliance with assignment requirements.

## Additional Resources

- **Kaggle Competition**: https://www.kaggle.com/c/nyc-taxi-fare-prediction
- **Kaggle API Documentation**: https://docs.kaggle.com/api
- **NYC Taxi Data Blog**: https://chriswhong.com/open-data/

## Quick Start Checklist

- [ ] Choose Option 1, 2, or 3 above
- [ ] Download and extract dataset
- [ ] Place at `data/nyc_taxi_fare.csv`
- [ ] Run: `python train.py`
- [ ] Check: `artifacts/taxi_fare_ann_model.joblib` created
- [ ] Success: Metrics displayed in console

---

**Last Updated:** May 7, 2026  
**Status:** ✓ All options validated
