"""
The dataset includes:
- Order metadata (order_id, restaurant_id, order_time)
- Kitchen load indicators (queue_length, orders_last_10min)
- Rider telemetry (rider_arrival_time, pickup_time)
- Handover delays
- Ground truth prep times
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os


def generate_dataset(n_samples=5000, start_date=None, random_seed=42):
    """
    Parameters:
    -----------
    n_samples : int
        Number of orders to generate (default: 5000)
    start_date : datetime
        Starting date for order times (default: current date - 30 days)
    random_seed : int
        Random seed for reproducibility
    
    Returns:
    --------
    pd.DataFrame
        Dataset with all required columns
    """
    np.random.seed(random_seed)
    
    # Set start date if not provided
    if start_date is None:
        start_date = datetime.now() - timedelta(days=30)
    
    # Initialize lists to store data
    data = {
        'order_id': [],
        'restaurant_id': [],
        'order_time': [],
        'queue_length': [],
        'orders_last_10min': [],
        'rider_arrival_time': [],
        'handover_delay': [],
        'pickup_time': [],
        'packed_time': [],
        'actual_prep_time': []
    }
    
    # Generate data for each order
    for i in range(n_samples):
        # Order ID and Restaurant ID
        order_id = f"ORD_{i+1:06d}"
        restaurant_id = np.random.randint(1, 101)  # 100 restaurants
        
        # Order time: random timestamp within the date range
        days_offset = np.random.uniform(0, 30)
        hours_offset = np.random.uniform(0, 24)
        order_time = start_date + timedelta(days=days_offset, hours=hours_offset)
        
        # Kitchen load indicators
        queue_length = np.random.randint(0, 21)  # 0-20
        orders_last_10min = np.random.randint(0, 51)  # 0-50
        
        # Calculate actual prep time based on kitchen load
        # Base prep time: 5-10 minutes
        base_prep_time = np.random.uniform(5, 10)
        
        # Load factor: 0.5-1.5 minutes per queue item
        load_factor = np.random.uniform(0.5, 1.5)
        
        # Random noise: normal distribution with mean 0, std 2 minutes
        noise = np.random.normal(0, 2)
        
        # Actual prep time calculation
        actual_prep_time = base_prep_time + queue_length * load_factor + noise
        
        # Ensure prep time is positive (realistic constraint)
        actual_prep_time = max(actual_prep_time, 1.0)
        
        # Packed time: when kitchen finishes preparing the order
        packed_time = order_time + timedelta(minutes=actual_prep_time)
        
        # Handover delay: time between packing and rider pickup (1-5 minutes)
        # This delay depends on restaurant load (higher load = longer delay)
        # We model this stochastically
        base_handover_delay = np.random.uniform(1, 5)
        # Add some correlation with queue_length (more load = slightly longer delay)
        load_impact = queue_length * 0.1  # 0.1 min per queue item
        handover_delay = base_handover_delay + load_impact + np.random.normal(0, 0.5)
        handover_delay = max(handover_delay, 0.5)  # Minimum 0.5 minutes
        
        # Pickup time: when rider actually picks up the order
        pickup_time = packed_time + timedelta(minutes=handover_delay)
        
        # Rider arrival time: when rider arrives at restaurant
        # This can be before or after packed_time (rider might wait)
        # We model this as: order_time + random delay (rider dispatched after order)
        rider_dispatch_delay = np.random.uniform(2, 15)  # Rider dispatched 2-15 min after order
        rider_arrival_time = order_time + timedelta(minutes=rider_dispatch_delay)
        
        # Ensure rider arrives before or at pickup time (logical constraint)
        if rider_arrival_time > pickup_time:
            # If rider arrives after pickup time, adjust to arrive slightly before
            rider_arrival_time = pickup_time - timedelta(minutes=np.random.uniform(0.5, 2))
        
        # Store data
        data['order_id'].append(order_id)
        data['restaurant_id'].append(restaurant_id)
        data['order_time'].append(order_time)
        data['queue_length'].append(queue_length)
        data['orders_last_10min'].append(orders_last_10min)
        data['rider_arrival_time'].append(rider_arrival_time)
        data['handover_delay'].append(handover_delay)
        data['pickup_time'].append(pickup_time)
        data['packed_time'].append(packed_time)
        data['actual_prep_time'].append(actual_prep_time)
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Convert timedelta columns to minutes for easier analysis
    return df


def save_dataset(df, output_path='data/dataset.csv'):
    """
    This will save dataset to CSV file.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Dataset to save
    output_path : str
        Path to save the CSV file
    """
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Save to CSV
    df.to_csv(output_path, index=False)
    print(f"Dataset saved to {output_path}")
    print(f"Shape: {df.shape}")
    print(f"\nFirst few rows:")
    print(df.head())
    print(f"\nDataset statistics:")
    print(df.describe())


if __name__ == "__main__":
    # Generate dataset
    print("Generating synthetic dataset for KPT prediction...")
    df = generate_dataset(n_samples=5000)
    
    # Save dataset
    save_dataset(df, output_path='data/dataset.csv')
    
    print("\nDataset generation complete!")
