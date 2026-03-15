"""
Survival Prediction - Probabilistic Preparation Time Prediction

Uses survival analysis to predict completion times.
"""

import numpy as np
from scipy import stats
from scipy.integrate import quad


class SurvivalPrediction:
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
        self.prep_times = []
    
    def fit(self, prep_times):
        """
        Fit survival model to data.
        
        Parameters:
        -----------
        prep_times : array-like
            Observed preparation times
        """
        prep_times = np.array(prep_times)
        prep_times = prep_times[prep_times > 0]
        self.prep_times = prep_times
        
        if len(prep_times) == 0:
            return
        
        if self.distribution == 'gamma':
            shape, loc, scale = stats.gamma.fit(prep_times, floc=0)
            self.fitted_params = {'shape': shape, 'scale': scale}
        elif self.distribution == 'lognormal':
            s, loc, scale = stats.lognorm.fit(prep_times, floc=0)
            self.fitted_params = {'s': s, 'scale': scale}
        elif self.distribution == 'weibull':
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
        return None
    
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
        return None
    
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
        
        S_t = np.maximum(S_t, 1e-10)
        return f_t / S_t
    
    def expected_prep_time(self):
        """
        Expected preparation time E[T] = integral(t * f(t) dt).
        
        Returns:
        --------
        float
            Expected preparation time
        """
        if self.fitted_params is None:
            return None
        
        def integrand(t):
            return t * self.pdf(t)
        
        try:
            result, _ = quad(integrand, 0, 100)
            return result
        except:
            return np.mean(self.prep_times) if len(self.prep_times) > 0 else None
    
    def variance(self):
        """
        Compute variance of preparation time.
        
        Returns:
        --------
        float
            Variance
        """
        if self.fitted_params is None:
            return np.var(self.prep_times) if len(self.prep_times) > 0 else None
        
        if self.distribution == 'gamma':
            shape = self.fitted_params['shape']
            scale = self.fitted_params['scale']
            return shape * scale ** 2
        elif self.distribution == 'lognormal':
            s = self.fitted_params['s']
            scale = self.fitted_params['scale']
            return (np.exp(s**2) - 1) * np.exp(2 * np.log(scale) + s**2)
        elif self.distribution == 'weibull':
            c = self.fitted_params['c']
            scale = self.fitted_params['scale']
            return scale**2 * (stats.gamma(1 + 2/c).mean() - stats.gamma(1 + 1/c).mean()**2)
        
        return None
    
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
    
    def confidence_interval(self, confidence=0.95):
        """
        Compute confidence interval.
        
        KPT = mu_T ± z*sigma_T
        
        Parameters:
        -----------
        confidence : float
            Confidence level (default 0.95)
        
        Returns:
        --------
        tuple
            (lower_bound, upper_bound)
        """
        mu = self.expected_prep_time()
        var = self.variance()
        
        if mu is None or var is None:
            return None, None
        
        sigma = np.sqrt(var)
        z = stats.norm.ppf((1 + confidence) / 2)
        
        lower = mu - z * sigma
        upper = mu + z * sigma
        
        return lower, upper
