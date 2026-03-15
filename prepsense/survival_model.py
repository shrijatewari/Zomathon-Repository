"""
Survival Model for Preparation Time Prediction

Models preparation time distribution and computes expected values.
"""

import numpy as np
from scipy import stats
from scipy.integrate import quad


class SurvivalModel:
    """Survival model for KPT prediction."""
    
    def __init__(self, distribution='gamma'):
        """
        Initialize survival model.
        
        Parameters:
        -----------
        distribution : str
            Distribution type ('gamma', 'lognormal', 'weibull')
        """
        self.distribution = distribution
        self.fitted_params = None
    
    def fit(self, prep_times):
        """
        Fit survival model to data.
        
        Parameters:
        -----------
        prep_times : array-like
            Observed preparation times
        """
        prep_times = np.array(prep_times)
        prep_times = prep_times[prep_times > 0]  # Remove non-positive values
        
        if self.distribution == 'gamma':
            # Fit gamma distribution
            shape, loc, scale = stats.gamma.fit(prep_times, floc=0)
            self.fitted_params = {'shape': shape, 'scale': scale}
        elif self.distribution == 'lognormal':
            # Fit lognormal distribution
            s, loc, scale = stats.lognorm.fit(prep_times, floc=0)
            self.fitted_params = {'s': s, 'scale': scale}
        elif self.distribution == 'weibull':
            # Fit Weibull distribution
            c, loc, scale = stats.weibull_min.fit(prep_times, floc=0)
            self.fitted_params = {'c': c, 'scale': scale}
    
    def pdf(self, t):
        """
        Probability density function f(t).
        
        Parameters:
        -----------
        t : float or array
            Time values
        
        Returns:
        --------
        float or array
            PDF values
        """
        if self.fitted_params is None:
            return None
        
        if self.distribution == 'gamma':
            return stats.gamma.pdf(t, self.fitted_params['shape'], 
                                  scale=self.fitted_params['scale'])
        elif self.distribution == 'lognormal':
            return stats.lognorm.pdf(t, self.fitted_params['s'],
                                     scale=self.fitted_params['scale'])
        elif self.distribution == 'weibull':
            return stats.weibull_min.pdf(t, self.fitted_params['c'],
                                       scale=self.fitted_params['scale'])
    
    def survival(self, t):
        """
        Survival function S(t) = P(T > t).
        
        Parameters:
        -----------
        t : float or array
            Time values
        
        Returns:
        --------
        float or array
            Survival probabilities
        """
        if self.fitted_params is None:
            return None
        
        if self.distribution == 'gamma':
            return 1 - stats.gamma.cdf(t, self.fitted_params['shape'],
                                      scale=self.fitted_params['scale'])
        elif self.distribution == 'lognormal':
            return 1 - stats.lognorm.cdf(t, self.fitted_params['s'],
                                        scale=self.fitted_params['scale'])
        elif self.distribution == 'weibull':
            return 1 - stats.weibull_min.cdf(t, self.fitted_params['c'],
                                            scale=self.fitted_params['scale'])
    
    def hazard_rate(self, t):
        """
        Hazard rate h(t) = f(t) / S(t).
        
        Parameters:
        -----------
        t : float or array
            Time values
        
        Returns:
        --------
        float or array
            Hazard rates
        """
        f_t = self.pdf(t)
        S_t = self.survival(t)
        
        if f_t is None or S_t is None:
            return None
        
        # Avoid division by zero
        S_t = np.maximum(S_t, 1e-10)
        return f_t / S_t
    
    def expected_prep_time(self):
        """
        Expected preparation time E[T] = integral t f(t) dt.
        
        Returns:
        --------
        float
            Expected preparation time
        """
        if self.fitted_params is None:
            return None
        
        # Integrate from 0 to a large value
        def integrand(t):
            return t * self.pdf(t)
        
        result, _ = quad(integrand, 0, 100)
        return result
    
    def predict(self):
        """
        Predict KPT using expected value.
        
        KPT_predicted = E[T]
        
        Returns:
        --------
        float
            Predicted preparation time
        """
        return self.expected_prep_time()
