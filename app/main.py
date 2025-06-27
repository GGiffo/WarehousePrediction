from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from .models import SarimaModel
from .schemas import ForecastRequest, ForecastResponse
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Inventory Forecast Service")
model = SarimaModel()

@app.on_event("startup")
async def startup_event():
    try:
        model.load()
        logger.info("Модель успешно загружена")
    except Exception as e:
        logger.error(f"Ошибка загрузки модели: {str(e)}")
        raise RuntimeError("Не удалось загрузить модель. Обучите модель сначала.")


@app.get("/", summary="Проверка работоспособности")
async def read_root():
    return {"status": "OK", "message": "Сервис прогнозирования запасов работает"}


@app.post("/forecast", response_model=ForecastResponse, summary="Прогнозирование запасов")
async def forecast(request: ForecastRequest):
    """
    Параметры:
    - days: период прогнозирования в днях
    - current_stock: текущий запас на складе
    - avg_price: средняя цена товара
    - safety_percent: процент страхового запаса
    """
    try:
        # Генерация будущих экзогенных переменных
        dates = pd.date_range(
            start=datetime.now(),
            periods=request.days,
            freq='D'
        )

        exog_data = pd.DataFrame({
            'date': dates,
            'price': np.full(request.days, request.avg_price),
            'promotion': np.zeros(request.days),
            'is_holiday': np.zeros(request.days)
        }).set_index('date')

        # Прогнозирование
        forecast = model.predict(request.days, exog_data)

        if forecast is None or len(forecast) == 0:
            raise HTTPException(status_code=500, detail="Ошибка прогнозирования")

        # Расчеты запасов
        total_demand = forecast.sum()
        safety_stock = request.safety_percent * total_demand / 100
        recommended_stock = total_demand + safety_stock
        current_coverage = (request.current_stock / total_demand * 100) if total_demand > 0 else 0

        return {
            "forecast_demand": round(total_demand, 2),
            "recommended_stock": round(recommended_stock, 2),
            "current_coverage_percent": round(current_coverage, 2),
            "safety_stock": round(safety_stock, 2),
            "daily_forecast": [round(x, 2) for x in forecast.tolist()]
        }

    except Exception as e:
        logger.error(f"Ошибка прогнозирования: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/train", summary="Обучение модели")
async def train_model():
    try:
        model.train("data/3_year_product_demand_dataset.csv")
        logger.info("Модель успешно переобучена")
        return {"status": "success", "message": "Модель успешно обучена"}
    except Exception as e:
        logger.error(f"Ошибка обучения модели: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))