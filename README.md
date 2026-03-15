# Kitchen Prep Time (KPT) Prediction System

A production-grade machine learning system for predicting kitchen preparation time in food delivery platforms. This system simulates real-world scenarios with dataset generation, telemetry modeling, ground truth reconstruction, and prediction capabilities.

## 🚀 Live Demo

**[PrepSense Streamlit Dashboard](https://zomathon-repository-dcr3grxm3ryk6r3wyopgv7.streamlit.app/)** – Interactive demo with signal intelligence, prediction engine, and dispatch optimization.

## 📋 Table of Contents

- [System Overview](#system-overview)
- [Repository Structure](#repository-structure)
- [Installation](#installation)
- [Dataset Generation](#dataset-generation)
- [Model Training](#model-training)
- [API Usage](#api-usage)
- [System Architecture](#system-architecture)

## 🎯 System Overview

### Problem Statement

Kitchen Prep Time (KPT) is defined as:
```
KPT = packed_time − order_time
```

The main challenge is that `packed_time` is not directly observed reliably. Instead, we observe:
- `order_time`: When the order is placed
- `rider_arrival_time`: When the delivery rider arrives at the restaurant
- `pickup_time`: When the rider picks up the order

### Solution Approach

We reconstruct `packed_time` using:
```
packed_time = pickup_time − handover_delay
```

Where `handover_delay` is a stochastic variable dependent on restaurant load. The system:
1. **Generates synthetic data** simulating realistic order processing scenarios
2. **Reconstructs ground truth** from observed telemetry data
3. **Trains ML models** to predict prep time based on kitchen load indicators
4. **Provides API service** for real-time predictions

### Key Features

- **Synthetic Dataset Generation**: Creates realistic order data with 5000+ samples
- **Ground Truth Reconstruction**: Estimates `packed_time` from observable events
- **XGBoost Regression Model**: Predicts prep time with high accuracy
- **RESTful API**: Production-ready Flask service for predictions
- **Comprehensive Evaluation**: MAE, RMSE, R² metrics with visualizations

## 📁 Repository Structure

```
.
├── data/
│   └── dataset.csv              # Generated synthetic dataset
├── models/
│   └── kpt_model.pkl            # Trained XGBoost model
├── notebooks/
│   └── kpt_prediction.ipynb     # Model training notebook
├── src/
│   ├── generate_dataset.py      # Dataset generation script
│   ├── ground_truth.py          # Ground truth reconstruction module
│   └── telemetry_simulation.py  # Telemetry simulation module
├── api/
│   └── app.py                   # Flask API service
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. **Clone or navigate to the repository**
   ```bash
   cd "ZOMATHON PS 1"
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

   Or install individually:
   ```bash
   pip install flask pandas numpy scikit-learn xgboost matplotlib seaborn jupyter
   ```

## 📊 Dataset Generation

The system generates synthetic datasets that simulate realistic food delivery order processing.

### Generate Dataset

Run the dataset generation script:

```bash
python3 src/generate_dataset.py
```

This will create `data/dataset.csv` with at least 5000 rows.

### Dataset Schema

| Column | Type | Description |
|--------|------|-------------|
| `order_id` | string | Unique order identifier |
| `restaurant_id` | int | Restaurant identifier (1-100) |
| `order_time` | datetime | Timestamp when order was placed |
| `queue_length` | int | Number of orders in queue (0-20) |
| `orders_last_10min` | int | Orders received in last 10 minutes (0-50) |
| `rider_arrival_time` | datetime | When rider arrived at restaurant |
| `handover_delay` | float | Delay between packing and pickup (minutes) |
| `pickup_time` | datetime | When rider picked up the order |
| `packed_time` | datetime | When order was packed (ground truth) |
| `actual_prep_time` | float | Actual preparation time (minutes) |

### Data Generation Logic

The `actual_prep_time` is calculated as:
```python
actual_prep_time = base_prep_time + queue_length * load_factor + random_noise
```

Where:
- `base_prep_time`: Random between 5-10 minutes
- `load_factor`: Random between 0.5-1.5 minutes per queue item
- `random_noise`: Normal distribution noise

Relationships:
- `packed_time = order_time + actual_prep_time`
- `pickup_time = packed_time + handover_delay`
- `handover_delay`: Correlates with restaurant load (1-5 minutes base, plus load impact)

## 🤖 Model Training

### Training the Model

1. **Open the Jupyter notebook**
   ```bash
   jupyter notebook notebooks/kpt_prediction.ipynb
   ```

2. **Run all cells** to:
   - Load and explore the dataset
   - Prepare features (`queue_length`, `orders_last_10min`, `handover_delay`)
   - Train XGBoost regression model
   - Evaluate performance (MAE, RMSE, R²)
   - Generate visualizations
   - Save model to `models/kpt_model.pkl`

### Model Features

**Input Features:**
- `queue_length`: Number of orders in queue (0-20)
- `orders_last_10min`: Orders in last 10 minutes (0-50)
- `handover_delay`: Estimated handover delay (minutes)

**Target Variable:**
- `actual_prep_time`: Kitchen preparation time (minutes)

### Model Architecture

- **Algorithm**: XGBoost Regression
- **Parameters**:
  - `n_estimators`: 100
  - `max_depth`: 6
  - `learning_rate`: 0.1
  - `subsample`: 0.8
  - `colsample_bytree`: 0.8

### Evaluation Metrics

The notebook calculates:
- **MAE (Mean Absolute Error)**: Primary metric for prep time prediction
- **RMSE (Root Mean Squared Error)**: Penalizes larger errors
- **R² Score**: Coefficient of determination

### Visualizations

The notebook includes:
- Predicted vs Actual prep time scatter plots
- Residuals analysis
- Feature importance charts
- Distribution plots

## 🔌 API Usage

### Starting the API Server

1. **Navigate to the api directory** (optional, paths are relative)
   ```bash
   cd api
   ```

2. **Start the Flask server**
   ```bash
   python3 app.py
   ```

   The server will start on `http://localhost:5000`

### API Endpoints

#### 1. Health Check

**GET** `/health`

Check if the API is running.

**Response:**
```json
{
  "status": "healthy",
  "message": "KPT Prediction API is running"
}
```

#### 2. API Documentation

**GET** `/`

Get API information and usage examples.

**Response:**
```json
{
  "name": "Kitchen Prep Time (KPT) Prediction API",
  "version": "1.0.0",
  "endpoints": { ... },
  "example_request": { ... }
}
```

#### 3. Predict Prep Time

**POST** `/predict`

Predict kitchen prep time based on restaurant load indicators.

**Request Body:**
```json
{
  "queue_length": 10,
  "orders_last_10min": 25
}
```

**Response:**
```json
{
  "predicted_prep_time": 18.5234,
  "queue_length": 10,
  "orders_last_10min": 25,
  "estimated_handover_delay": 3.2
}
```

### Example Usage

#### Using cURL

```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "queue_length": 15,
    "orders_last_10min": 30
  }'
```

#### Using Python

```python
import requests
import json

url = "http://localhost:5000/predict"
data = {
    "queue_length": 15,
    "orders_last_10min": 30
}

response = requests.post(url, json=data)
result = response.json()

print(f"Predicted prep time: {result['predicted_prep_time']} minutes")
```

#### Using JavaScript (fetch)

```javascript
fetch('http://localhost:5000/predict', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    queue_length: 15,
    orders_last_10min: 30
  })
})
.then(response => response.json())
.then(data => {
  console.log('Predicted prep time:', data.predicted_prep_time, 'minutes');
});
```

### Error Handling

The API returns appropriate HTTP status codes:

- **200**: Success
- **400**: Bad Request (missing/invalid input)
- **500**: Server Error (model not found, prediction failed)

**Error Response Example:**
```json
{
  "error": "Missing required field: queue_length"
}
```

### Note on Handover Delay

The model was trained with 3 features (`queue_length`, `orders_last_10min`, `handover_delay`), but the API only receives 2 inputs. The API automatically estimates `handover_delay` based on `queue_length` using a correlation observed in the training data:

```python
estimated_delay = base_delay + queue_length * factor + noise
```

This maintains realistic predictions while simplifying the API interface.

## 🏗️ System Architecture

### Data Flow

```
Order Placed
    ↓
[Dataset Generation]
    ↓
Synthetic Order Data
    ↓
[Ground Truth Reconstruction]
    ↓
Reconstructed packed_time
    ↓
[Model Training]
    ↓
Trained XGBoost Model
    ↓
[API Service]
    ↓
Real-time Predictions
```

### Components

1. **Dataset Generator** (`src/generate_dataset.py`)
   - Creates synthetic order data
   - Models realistic relationships between variables
   - Generates timestamps and delays

2. **Ground Truth Module** (`src/ground_truth.py`)
   - Reconstructs `packed_time` from observable events
   - Estimates handover delays

3. **Telemetry Simulation** (`src/telemetry_simulation.py`)
   - Simulates rider arrival and pickup events
   - Models stochastic delays

4. **ML Model** (`notebooks/kpt_prediction.ipynb`)
   - Trains XGBoost regression model
   - Evaluates performance
   - Saves trained model

5. **API Service** (`api/app.py`)
   - RESTful endpoint for predictions
   - Loads trained model
   - Handles requests and responses

## 📝 Notes

- This is a **simulation system** designed for hackathon/demonstration purposes
- All timestamps are realistic and follow logical causality
- The model estimates `handover_delay` when not provided in API requests
- For production use, consider:
  - Model retraining pipeline
  - API authentication/authorization
  - Request rate limiting
  - Logging and monitoring
  - Using a production WSGI server (e.g., gunicorn)

## 🤝 Contributing

This is a hackathon project. Feel free to extend it with:
- Additional features (restaurant-specific models, time-of-day features)
- Model improvements (hyperparameter tuning, feature engineering)
- API enhancements (batch predictions, model versioning)
- Monitoring and logging

## 📄 License

This project is created for hackathon purposes.

---

**Built for ZOMATHON PS 1** 🚀
