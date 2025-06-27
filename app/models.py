import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.tsa.statespace.sarimax import SARIMAX
from joblib import dump, load
import os


class SarimaModel:
    def __init__(self):
        self.model = None
        self.model_path = "app/storage/sarima_model.joblib"

    def train(self, data_path: str):
        df = pd.read_csv(data_path, parse_dates=['date'])
        df = df.set_index('date').asfreq('D')


        y = df['demand']
        exog = df[['price', 'promotion', 'is_holiday']]

        order = (1, 1, 1)
        seasonal_order = (1, 1, 1, 7)  # Недельная сезонность

        self.model = SARIMAX(
            y,
            order=order,
            seasonal_order=seasonal_order,
            exog=exog,
            enforce_stationarity=False
        ).fit(disp=False)

        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        dump(self.model, self.model_path)

    def predict(self, days: int, exog_data: pd.DataFrame) -> pd.Series:
        if not self.model:
            self.load()
        return self.model.get_forecast(steps=days, exog=exog_data).predicted_mean

    def load(self):
        self.model = load(self.model_path)