"""
Dispatch Optimizer - Optimal Rider Assignment Timing

Optimizes rider dispatch to minimize idle time and delays.
"""

import numpy as np


class DispatchOptimizer:
    """Optimize rider dispatch timing."""
    
    def __init__(self, cost_idle=1.0, cost_delay=2.0):
        """
        Initialize optimizer.
        
        Parameters:
        -----------
        cost_idle : float
            Cost per unit idle time
        cost_delay : float
            Cost per unit delay
        """
        self.cost_idle = cost_idle
        self.cost_delay = cost_delay
    
    def compute_idle_time(self, packed_time, assign_time):
        """
        Compute rider idle time.
        
        Idle = max(0, T_p - T_assign)
        
        Parameters:
        -----------
        packed_time : float
            Packed time (minutes from order)
        assign_time : float
            Assignment time (minutes from order)
        
        Returns:
        --------
        float
            Idle time
        """
        return max(0, packed_time - assign_time)
    
    def compute_delay(self, packed_time, assign_time):
        """
        Compute delivery delay.
        
        Delay = max(0, T_assign - T_p)
        
        Parameters:
        -----------
        packed_time : float
            Packed time (minutes from order)
        assign_time : float
            Assignment time (minutes from order)
        
        Returns:
        --------
        float
            Delay time
        """
        return max(0, assign_time - packed_time)
    
    def compute_cost(self, packed_time, assign_time):
        """
        Compute total cost.
        
        Cost = C1 * Idle + C2 * Delay
        
        Parameters:
        -----------
        packed_time : float
            Packed time
        assign_time : float
            Assignment time
        
        Returns:
        --------
        float
            Total cost
        """
        idle = self.compute_idle_time(packed_time, assign_time)
        delay = self.compute_delay(packed_time, assign_time)
        cost = self.cost_idle * idle + self.cost_delay * delay
        return cost
    
    def optimal_assignment(self, mean_prep_time, std_prep_time, k=1.0):
        """
        Find optimal assignment time.
        
        T_assign* = mu + k*sigma
        
        Parameters:
        -----------
        mean_prep_time : float
            Mean preparation time
        std_prep_time : float
            Standard deviation
        k : float
            Safety factor
        
        Returns:
        --------
        float
            Optimal assignment time
        """
        optimal_time = mean_prep_time + k * std_prep_time
        return optimal_time
    
    def batch_optimize(self, prep_times, k=1.0):
        """
        Optimize assignment for batch of orders.
        
        Parameters:
        -----------
        prep_times : array-like
            Preparation times
        k : float
            Safety factor
        
        Returns:
        --------
        dict
            Optimization results
        """
        prep_times = np.array(prep_times)
        mean_prep = np.mean(prep_times)
        std_prep = np.std(prep_times)
        
        optimal_assign = self.optimal_assignment(mean_prep, std_prep, k)
        
        idle_times = [self.compute_idle_time(pt, optimal_assign) for pt in prep_times]
        delays = [self.compute_delay(pt, optimal_assign) for pt in prep_times]
        
        avg_idle = np.mean(idle_times)
        avg_delay = np.mean(delays)
        total_cost = self.cost_idle * avg_idle + self.cost_delay * avg_delay
        
        return {
            'optimal_assignment_time': optimal_assign,
            'mean_idle_time': avg_idle,
            'mean_delay': avg_delay,
            'total_cost': total_cost,
            'mean_prep_time': mean_prep,
            'std_prep_time': std_prep,
            'idle_times': idle_times,
            'delays': delays
        }
    
    def compare_baseline_vs_prepsense(self, baseline_prep_times, prepsense_prep_times, k=1.0):
        """
        Compare baseline vs PrepSense optimization.
        
        Parameters:
        -----------
        baseline_prep_times : array-like
            Baseline preparation times
        prepsense_prep_times : array-like
            PrepSense preparation times
        k : float
            Safety factor
        
        Returns:
        --------
        dict
            Comparison results
        """
        baseline_opt = self.batch_optimize(baseline_prep_times, k)
        prepsense_opt = self.batch_optimize(prepsense_prep_times, k)
        
        idle_reduction = ((baseline_opt['mean_idle_time'] - prepsense_opt['mean_idle_time']) /
                         baseline_opt['mean_idle_time']) * 100 if baseline_opt['mean_idle_time'] > 0 else 0
        
        delay_reduction = ((baseline_opt['mean_delay'] - prepsense_opt['mean_delay']) /
                          baseline_opt['mean_delay']) * 100 if baseline_opt['mean_delay'] > 0 else 0
        
        cost_reduction = ((baseline_opt['total_cost'] - prepsense_opt['total_cost']) /
                         baseline_opt['total_cost']) * 100 if baseline_opt['total_cost'] > 0 else 0
        
        return {
            'baseline': baseline_opt,
            'prepsense': prepsense_opt,
            'idle_reduction_percent': idle_reduction,
            'delay_reduction_percent': delay_reduction,
            'cost_reduction_percent': cost_reduction
        }
