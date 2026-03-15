# PrepSense - Kitchen Preparation Time Prediction System

A full-stack prototype for predicting kitchen preparation times in food delivery platforms using telemetry reconstruction and advanced mathematical models.

## 🚀 Quick Start

### Installation

```bash
pip install -r requirements.txt
```

### Run Dashboard

```bash
streamlit run dashboard.py
```

## 📁 Project Structure

- `simulator.py` - Order and kitchen simulation with Poisson arrivals
- `telemetry.py` - Rider arrival and pickup telemetry generation
- `reconstruction.py` - PrepSense signal reconstruction algorithms
- `survival_model.py` - Survival analysis for prep time prediction
- `dispatch_optimizer.py` - Rider assignment optimization
- `event_filter.py` - Weighted event filtering
- `dataset_generator.py` - Synthetic dataset generation
- `graphs.py` - Visualization utilities
- `dashboard.py` - Streamlit interactive dashboard

## 🎯 Features

- **Real-time Simulation**: Poisson process order arrivals
- **Telemetry Reconstruction**: Accurate prep time estimation
- **Survival Modeling**: Probabilistic prep time prediction
- **Dispatch Optimization**: Minimize idle time and delays
- **Interactive Dashboard**: Zomato-inspired UI with real-time metrics

## 📊 Mathematical Framework

### Order Arrivals
- Poisson process: N(t) ~ Poisson(λ)

### Service Rate
- μ(t) = μ₀ / (1 + γ·L(t))

### True Prep Time
- KPT_true = 1 / μ(t)

### Reconstruction
- T̂ = T_pickup - mean_handover
- KPT_reconstructed = T̂ - T_order

## 🎨 Color Scheme

- Primary: #CB472C (Warm reddish-orange)
- Secondary: #FFF7EB (Light cream)
- Accent: #FFD94F (Golden yellow)
- Text: #A52A2A (Dark reddish-brown)

## 📈 Dashboard Features

- Key performance metrics
- Signal distribution comparison
- Variance reduction analysis
- Idle time optimization
- Confidence interval visualization
- Kitchen load analysis

## 🔧 Configuration

Adjust parameters via sidebar:
- Order arrival rate (λ)
- Noise level (σ)
- Kitchen capacity
- Number of orders

## 📝 License

Created for Zomathon hackathon.
