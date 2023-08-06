import numpy as np
import pandas as pd
from datetime import datetime

from ..utils import get_zt
from ..utils import univariate as uv
from ..utils import unimultivariate as umv


class Benchmark(object):
    """Univariate mean and random walk forecasting

    Parameters:

        h: an integer;
            forecasting horizon

        level: an integer;
            Confidence level for prediction intervals

        method: a string;
            Mean forecast ("mean") or Random Walk forecast ("rw")    
        
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
    from forecasting_sandbox import Benchmark

    # Data frame containing the time series
    dataset = {
    'date' : ['2020-01-01', '2020-02-01', '2020-03-01', '2020-04-01', '2020-05-01'],
    'value' : [34, 30, 35.6, 33.3, 38.1]}

    df = pd.DataFrame(dataset).set_index('date')
    print(df)

    # univariate time series forecasting
    m1 = Benchmark(h = 5)
    m1.forecast(df)
    print(m1.result_df_)
    ```

    """

    def __init__(
        self,
        h=5,
        level=95,
        method = "mean",
        date_formatting="original",        
    ):

        self.h = h
        self.level = level
        self.method = method
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
        """Mean and Random Walk forecasting method

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
            assert (start_training - 1 + n_training) <= df.shape[0], "check `start_training` and `n_training` again"
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

        # mean forecast                       
        if (self.method == "mean"): 
            fcast_mean = np.mean(self.input_df["value"].values) 
            self.fcast_["mean"] = [fcast_mean for _ in range(self.h)]
            self.fcast_["residuals"] = self.input_df["value"].values - fcast_mean
            sigma = np.std(self.fcast_['residuals'], ddof=1)  
            fcast_se = sigma * np.sqrt(1 + 1/len(self.fcast_["residuals"]))
            zt = get_zt(self.level/100)
            self.fcast_["lower"] = [fcast_mean - zt * fcast_se for _ in range(self.h)]
            self.fcast_["upper"] = [fcast_mean + zt * fcast_se for _ in range(self.h)]

            
        # random walk
        if (self.method == "rw"):
            last_point_value = df["value"].values[-1]
            self.fcast_["mean"] = [last_point_value for _ in range(self.h)]
            self.fcast_["residuals"] = self.input_df["value"].values - last_point_value
            sigma = np.std(self.fcast_['residuals'], ddof=1)
            zt = get_zt(self.level/100)
            self.fcast_["lower"] = [last_point_value - zt * sigma * np.sqrt(i) for i in range(1, self.h + 1)]
            self.fcast_["upper"] = [last_point_value + zt * sigma * np.sqrt(i) for i in range(1, self.h + 1)]


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
