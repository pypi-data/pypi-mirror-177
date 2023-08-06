import os
import numpy as np
import pandas as pd

from datetime import datetime
from .unimultivariate import get_frequency


def format_multivariate_forecast(
    n_series, date_formatting, output_dates, horizon, fcast
):

    if date_formatting == "original":
        output_dates_ = [
            datetime.strftime(output_dates[i], "%Y-%m-%d")
            for i in range(horizon)
        ]

    if date_formatting == "ms":
        output_dates_ = [
            int(
                datetime.strptime(str(output_dates[i]), "%Y-%m-%d").timestamp()
                * 1000
            )
            for i in range(horizon)
        ]

    averages = []
    ranges = []

    for j in range(n_series):
        averages_series_j = []
        ranges_series_j = []
        for i in range(horizon):
            date_i = output_dates_[i]
            index_i_j = i + j * horizon
            averages_series_j.append([date_i, fcast["mean"][index_i_j]])
            ranges_series_j.append(
                [
                    date_i,
                    fcast["lower"][index_i_j],
                    fcast["upper"][index_i_j],
                ]
            )
        averages.append(averages_series_j)
        ranges.append(ranges_series_j)

    return averages, ranges, output_dates_
