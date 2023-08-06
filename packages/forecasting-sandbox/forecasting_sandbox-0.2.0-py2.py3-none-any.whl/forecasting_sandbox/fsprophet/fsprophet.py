import numpy as np
import pandas as pd
from prophet import Prophet

from ..utils import unimultivariate as umv
from ..utils import univariate as uv


class fsProphet(object):
    """Univariate FB Prophet forecasting

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
    from forecasting_sandbox import Prophet

    # Data frame containing the time series
    dataset = {
    'date' : ['2020-01-01', '2020-02-01', '2020-03-01', '2020-04-01', '2020-05-01'],
    'value' : [34, 30, 35.6, 33.3, 38.1]}

    df = pd.DataFrame(dataset).set_index('date')
    print(df)

    # univariate time series forecasting
    t1 = fsProphet(h = 5)
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
        """Adapted from Prophet forecasting method, for a unified interface

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

        df_prophet = pd.DataFrame()
        df_prophet["ds"] = pd.DatetimeIndex(self.input_df.index)
        df_prophet["y"] = self.input_df["value"].values                                

        np.random.seed(seed=123)
        m = Prophet(interval_width=self.level/100)
        m.fit(df_prophet)

        frequency = pd.infer_freq(df_prophet['ds'])

        output_dates = pd.date_range(start=df_prophet["ds"].values[-1], 
                                     periods=self.h + 1, 
                                     freq=frequency)[1:]        
        future = pd.DataFrame({"ds": output_dates})
        forecast_df = m.predict(future)
        
        self.mean_ = forecast_df[['yhat']].values.flatten()
        self.lower_= forecast_df[['yhat_lower']].values.flatten()
        self.upper_= forecast_df[['yhat_upper']].values.flatten()

        self.fcast_["mean"] = self.mean_.tolist()
        self.fcast_["lower"] = self.lower_.tolist()
        self.fcast_["upper"] = self.upper_.tolist()

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

        self.result_df_ = umv.compute_result_df(self.averages_, self.ranges_)
   
        return self
