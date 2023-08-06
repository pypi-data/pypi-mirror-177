import numpy as np
import pandas as pd
import warnings

from datetime import datetime
from scipy.stats import norm 
from statsmodels.tsa.stattools import acf 
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.holtwinters import SimpleExpSmoothing

from ..utils import get_zt
from ..utils import univariate as uv
from ..utils import unimultivariate as umv
from ..utils import get_frequency

# adapted from https://github.com/MinhDg00/theta/blob/master/src/ses_theta.py

class Theta(object):
    """Univariate Theta forecasting

    Parameters:

        h: an integer;
            forecasting horizon

        level: an integer;
            Confidence level for prediction intervals
        
        date_formatting: a string;
            Currently:
            - "original": yyyy-mm-dd
            - "ms": milliseconds

    Attributes:

        fcast_: a dict;
            contains mean forecast, plus lower and upper bounds
            of prediction intervals

        averages_: a list;
            mean forecast in a list

        ranges_: a list;
            lower and upper prediction intervals in a list

        output_dates_: a list;
            a list of output dates (associated to forecast)

        mean_: a numpy array
            contains series mean forecast as a numpy array 

        lower_: a numpy array 
            contains series lower bound forecast as a numpy array   

        upper_: a numpy array 
            contains series upper bound forecast as a numpy array   

        result_df_: a data frame;
            contains 3 columns, mean forecast, lower + upper
            prediction intervals, and a date index

    Examples:

    ```python
    import pandas as pd
    from forecasting_sandbox import Theta

    # Data frame containing the time series
    dataset = {
    'date' : ['2020-01-01', '2020-02-01', '2020-03-01', '2020-04-01', '2020-05-01'],
    'value' : [34, 30, 35.6, 33.3, 38.1]}

    df = pd.DataFrame(dataset).set_index('date')
    print(df)

    # univariate time series forecasting
    t1 = Theta(h = 5)
    t1.forecast(df)
    print(t1.result_df_)
    ```

    """

    def __init__(
        self,
        h=5,
        level=95,
        date_formatting="original",        
    ):

        self.h = h
        self.level = level
        self.date_formatting = date_formatting
        self.fcast_ = {"mean": [], "residuals": [],"lower": [], "upper": []}
        self.averages_ = None
        self.ranges_ = None
        self.output_dates_ = []
        self.mean_ = None
        self.lower_ = None
        self.upper_ = None
        self.result_df_ = None

    def forecast(self, df, start_training=None, n_training=None):
        """Theta forecasting method

        Parameters:

            df: a data frame;
                a data frame containing the input time series (see example)

            start_training: an integer;
                starting index for the training set (default is None)
                starts at 1, if provided (!) not 0

            n_training: an integer;
                number of points in training set (default is None)

        """                            

        if ((start_training is not None) and (n_training is not None)):  
            assert start_training >= 1, "`start_training` must be >= 1"
            assert n_training >= 1, "`n_training` must be >= 1"       
            assert (start_training - 1 + n_training + self.h) <= df.shape[0], "check `start_training` and `n_training` again"
            self.start_training_ = start_training
            self.n_training_ = n_training
            start_training_python = start_training - 1
            self.input_df = df.iloc[start_training_python:(start_training_python + self.n_training_), :]
        else:
            self.input_df = df            

        # obtain dates 'forecast' -----

        (output_dates, frequency) = umv.compute_output_dates(
            self.input_df, self.h
        )

        # obtain time series forecast ----- 

        y = self.input_df['value']
        x = y.copy()
        x.index = pd.DatetimeIndex(x.index, freq=frequency)
        n = len(y)
        m = get_frequency(frequency) 

        if m > 1 and n > 2 * m:
            r = (acf(x, nlags = m))[1:]
            temp = np.delete(r, m-1)
            stat = np.sqrt((1 + 2 * np.sum(np.square(temp))) / n)
            seasonal = (abs(r[m - 1])/stat) > norm.cdf(0.95)
        else:
            seasonal = False

        # Seasonal Decomposition
        origx = x.copy()
        if seasonal:
            decomp = seasonal_decompose(x, model = 'multiplicative')
            if np.any(np.abs(decomp.seasonal.values) < 1e-4) :
                warnings.warn('Seasonal indexes equal to zero. Using non-seasonal Theta method')
            else:
                x = decomp.observed/decomp.seasonal

        # Find theta lines
        model = SimpleExpSmoothing(x).fit()
        self.fcast_['fitted'] = model.fittedvalues
        self.fcast_['mean'] = model.forecast(self.h)
        num = np.array(range(0, n))      
        A = np.vstack([np.ones(len(num)), num]).T        
        coef_slope = np.linalg.lstsq(a = A, b = x, rcond=None)[0][1]
        tmp2 = coef_slope/2
        alpha = np.maximum(1e-10, model.params['smoothing_level'])
        self.fcast_['mean'] += tmp2 * (np.array(range(0, self.h)) + (1 - (1 - alpha)**n)/alpha)

        # Reseasonalize
        if seasonal:
            tmp = np.repeat(decomp.seasonal[-m:], (1 + self.h//m))[:self.h]
            tmp.index = self.fcast_['mean'].index
            self.fcast_['mean'] *= tmp
            self.fcast_['fitted'] *= decomp.seasonal            
        else:
            self.fcast_['fitted'] = model.predict(x.index[0], x.index[n-1])  

        # prediction intervals             
        self.fcast_['residuals'] = origx - self.fcast_['fitted']
        sigma = np.std(self.fcast_['residuals'], ddof=2)        
        zt = get_zt(self.level/100)
        
        # zt * sigma * np.sqrt(1 + i*alpha**2)
        self.fcast_["lower"] = []
        self.fcast_["upper"] = []
        for i in range(self.h):
            self.fcast_["lower"].append(self.fcast_['mean'].values[i] - zt * sigma * np.sqrt(1 + i*alpha**2)) 
            self.fcast_["upper"].append(self.fcast_['mean'].values[i] + zt * sigma * np.sqrt(1 + i*alpha**2)) 
        
        # result -----

        (
            self.averages_,
            self.ranges_,
            self.output_dates_,
        ) = uv.format_univariate_forecast(
            date_formatting=self.date_formatting,
            output_dates=output_dates,
            horizon=self.h,
            fcast=self.fcast_,
        )

        self.mean_ = np.asarray(self.fcast_['mean'])
        self.lower_= np.asarray(self.fcast_['lower'])
        self.upper_= np.asarray(self.fcast_['upper'])

        self.result_df_ = umv.compute_result_df(self.averages_, self.ranges_)
        
        return self
