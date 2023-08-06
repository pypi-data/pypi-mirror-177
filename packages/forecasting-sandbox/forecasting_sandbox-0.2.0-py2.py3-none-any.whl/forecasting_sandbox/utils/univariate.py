import os
import numpy as np
import pandas as pd

from datetime import datetime
from .unimultivariate import get_frequency


def format_univariate_forecast(date_formatting, output_dates, horizon, fcast):

    if date_formatting == "ms":

        try: 
            output_dates_ = [
                int(
                    datetime.strptime(str(output_dates[i]), "%Y-%m-%d").timestamp()
                    * 1000
                )
                for i in range(horizon)
            ]
        except:
            output_dates_ = [int(output_dates[i].timestamp()* 1000) for i in range(len(output_dates))]

    else: # 'any other case: original', or None, or empty, etc.
        
        output_dates_ = [
            datetime.strftime(output_dates[i], "%Y-%m-%d")
            for i in range(horizon)
        ]

    averages = [
        [output_dates_[i], fcast["mean"][i]] for i in range(horizon)
    ]
    ranges = [
        [output_dates_[i], fcast["lower"][i], fcast["upper"][i]]
        for i in range(horizon)
    ]

    return averages, ranges, output_dates_
