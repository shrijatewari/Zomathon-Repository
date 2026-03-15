# PrepSense Quick Start Guide

## 🚀 Running the Dashboard

### Step 1: Install Dependencies

```bash
cd prepsense
pip install -r requirements.txt
```

### Step 2: Run the Dashboard

```bash
streamlit run dashboard.py
```

The dashboard will open in your browser at `http://localhost:8501`

## 📊 Dashboard Features

### Interactive Controls (Sidebar)
- **Order Arrival Rate (λ)**: Adjust Poisson process rate
- **Noise Level (σ)**: Control observation noise
- **Kitchen Capacity**: Set maximum kitchen load
- **Number of Orders**: Dataset size

### Visualizations
1. **Key Metrics**: Real-time KPT, variance, idle time, prediction error
2. **Signal Distribution**: Histogram comparison of observed vs reconstructed
3. **Variance Comparison**: Bar chart showing improvement
4. **Idle Time Analysis**: Operational efficiency metrics
5. **Queue Analysis**: Kitchen load impact visualization
6. **Confidence Intervals**: Prediction uncertainty bands
7. **Service Rate Analysis**: Load vs service rate relationship

## 🎨 Design

The dashboard uses a Zomato-inspired color scheme:
- **Primary**: Warm reddish-orange (#CB472C)
- **Secondary**: Light cream (#FFF7EB)
- **Accent**: Golden yellow (#FFD94F)
- **Text**: Dark reddish-brown (#A52A2A)

## 🔧 System Components

### Core Modules
- `simulator.py`: Kitchen queue simulation
- `telemetry.py`: Rider tracking signals
- `reconstruction.py`: PrepSense signal reconstruction
- `survival_model.py`: Probabilistic predictions
- `dispatch_optimizer.py`: Rider assignment optimization
- `event_filter.py`: Weighted event filtering

### Data & Visualization
- `dataset_generator.py`: Synthetic data generation
- `graphs.py`: Plotting utilities
- `dashboard.py`: Streamlit interface

## 📈 Mathematical Framework

### Order Arrivals
```
N(t) ~ Poisson(λ)
```

### Service Rate
```
μ(t) = μ₀ / (1 + γ·L(t))
```

### True Prep Time
```
KPT_true = 1 / μ(t)
```

### Reconstruction
```
T̂ = T_pickup - mean_handover
KPT_reconstructed = T̂ - T_order
```

## 🧪 Testing

Run the test script to verify all components:

```bash
python3 test_system.py
```

## 📝 Notes

- First run will generate a dataset automatically
- All visualizations update in real-time
- Metrics are computed on-the-fly
- Data is cached for performance

## 🐛 Troubleshooting

**Import Errors**: Make sure you're in the `prepsense` directory

**Missing Data**: The system will auto-generate data on first run

**Port Already in Use**: Change port with `streamlit run dashboard.py --server.port 8502`
