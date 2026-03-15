"""
Dataset Generator for PrepSense Kitchen Preparation Time Simulation

Generates synthetic order data with realistic telemetry signals.
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import os


class DatasetGenerator:
    """Generate synthetic order dataset for PrepSense simulation."""
    
    def __init__(self, n_samples=5000, noise_level=3.0, arrival_rate=0.5, 
                 kitchen_capacity=20, random_seed=42):
        """
        Initialize dataset generator.
        
        Parameters:
        -----------
        n_samples : int
            Number of orders to generate
        noise_level : float
            Standard deviation for observed noise
        arrival_rate : float
            Order arrival rate (lambda)
        kitchen_capacity : int
            Kitchen capacity for load simulation
        random_seed : int
            Random seed for reproducibility
        """
        self.n_samples = n_samples
        self.noise_level = noise_level
        self.arrival_rate = arrival_rate
        self.kitchen_capacity = kitchen_capacity
        np.random.seed(random_seed)
    
    def generate_orders(self):
        """
        Generate synthetic order dataset.
        
        Returns:
        --------
        pd.DataFrame
            Generated dataset with all required fields
        """
        print(f"Generating {self.n_samples} orders...")
        
        data = {
            'StoreID': [],
            'OrderTime': [],
            'ArrivalTime': [],
            'PickupTime': [],
            'ObservedPrepTime': [],
            'ReconstructedPrepTime': [],
            'KitchenLoad': [],
            'QueueLength': [],
            'IdleTime': []
        }
        
        for i in range(self.n_samples):
            # Store ID
            store_id = np.random.randint(1, 101)
            
            # Order time
            days_offset = np.random.uniform(0, 30)
            hours_offset = np.random.uniform(0, 24)
            order_time = datetime.now() - timedelta(days=days_offset, hours=hours_offset)
            
            # Kitchen load and queue length (based on capacity)
            max_queue = min(self.kitchen_capacity, 50)
            queue_length = np.random.randint(0, max_queue + 1)
            # Kitchen load scales with capacity
            load_factor = queue_length / max(1, self.kitchen_capacity)
            kitchen_load = load_factor * self.kitchen_capacity
            
            # True preparation time (depends on load)
            base_prep_time = np.random.uniform(5, 15)
            load_factor = 1 + 0.1 * kitchen_load
            true_prep_time = base_prep_time * load_factor + np.random.normal(0, 1)
            true_prep_time = max(1.0, true_prep_time)
            
            # Observed prep time (with noise based on slider)
            noise_observed = np.random.normal(0, self.noise_level)
            observed_prep_time = true_prep_time + noise_observed
            observed_prep_time = max(0.5, observed_prep_time)
            
            # Reconstructed prep time (less noise - 50% of observed noise)
            noise_reconstructed = np.random.normal(0, self.noise_level * 0.5)
            reconstructed_prep_time = true_prep_time + noise_reconstructed
            reconstructed_prep_time = max(0.5, reconstructed_prep_time)
            
            # Timestamps
            arrival_time = order_time + timedelta(minutes=true_prep_time)
            handover_delay = np.random.normal(2, 1)
            handover_delay = max(0.5, handover_delay)
            pickup_time = arrival_time + timedelta(minutes=handover_delay)
            
            # Rider idle time
            rider_arrival_gap = np.random.uniform(8, 15)
            idle_time = max(0, true_prep_time - rider_arrival_gap)
            
            # Store data
            data['StoreID'].append(store_id)
            data['OrderTime'].append(order_time)
            data['ArrivalTime'].append(arrival_time)
            data['PickupTime'].append(pickup_time)
            data['ObservedPrepTime'].append(observed_prep_time)
            data['ReconstructedPrepTime'].append(reconstructed_prep_time)
            data['KitchenLoad'].append(kitchen_load)
            data['QueueLength'].append(queue_length)
            data['IdleTime'].append(idle_time)
        
        df = pd.DataFrame(data)
        print(f"Generated {len(df)} orders")
        return df
    
    def save_dataset(self, df, output_path='prepsense/data/orders.csv'):
        """
        Save dataset to CSV.
        
        Parameters:
        -----------
        df : pd.DataFrame
            Dataset to save
        output_path : str
            Output file path
        """
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_csv(output_path, index=False)
        print(f"Dataset saved to {output_path}")


if __name__ == "__main__":
    generator = DatasetGenerator(n_samples=5000)
    df = generator.generate_orders()
    generator.save_dataset(df)
