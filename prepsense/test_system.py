"""
Test script for PrepSense system components.
"""

import numpy as np
from datetime import datetime
from simulator import KitchenSimulator
from telemetry import TelemetryGenerator
from reconstruction import PrepSenseReconstructor
from survival_model import SurvivalModel
from dispatch_optimizer import DispatchOptimizer
from event_filter import EventFilter

print("Testing PrepSense System Components...")
print("="*50)

# Test Kitchen Simulator
print("\n1. Testing Kitchen Simulator...")
sim = KitchenSimulator(arrival_rate=0.5)
order_time = datetime.now()
result = sim.process_order(order_time)
print(f"   ✓ Queue Length: {result['queue_length']}")
print(f"   ✓ Kitchen Load: {result['kitchen_load']:.2f}")
print(f"   ✓ KPT True: {result['kpt_true']:.2f} min")

# Test Telemetry Generator
print("\n2. Testing Telemetry Generator...")
telemetry = TelemetryGenerator()
telemetry_data = telemetry.generate_telemetry(order_time, result['packed_time'])
print(f"   ✓ Arrival Time: {telemetry_data['arrival_time']}")
print(f"   ✓ Pickup Time: {telemetry_data['pickup_time']}")
print(f"   ✓ Waiting Time: {telemetry_data['waiting_time']:.2f} min")

# Test Reconstruction
print("\n3. Testing PrepSense Reconstructor...")
reconstructor = PrepSenseReconstructor()
kpt_recon = reconstructor.reconstruct_kpt(order_time, telemetry_data['pickup_time'])
print(f"   ✓ Reconstructed KPT: {kpt_recon:.2f} min")

# Test Survival Model
print("\n4. Testing Survival Model...")
prep_times = np.random.gamma(2, 5, 100)
survival_model = SurvivalModel(distribution='gamma')
survival_model.fit(prep_times)
expected = survival_model.expected_prep_time()
print(f"   ✓ Expected Prep Time: {expected:.2f} min")

# Test Dispatch Optimizer
print("\n5. Testing Dispatch Optimizer...")
optimizer = DispatchOptimizer()
opt_result = optimizer.batch_optimize(prep_times, k=1.0)
print(f"   ✓ Optimal Assignment: {opt_result['optimal_assignment_time']:.2f} min")
print(f"   ✓ Mean Idle Time: {opt_result['mean_idle_time']:.2f} min")

# Test Event Filter
print("\n6. Testing Event Filter...")
event_filter = EventFilter()
for i in range(5):
    obs = np.random.normal(10, 2)
    var = np.random.uniform(1, 4)
    event_filter.add_event(obs, var)
filtered = event_filter.compute_filtered_estimate()
print(f"   ✓ Filtered Estimate: {filtered:.2f} min")

print("\n" + "="*50)
print("All tests passed! ✓")
