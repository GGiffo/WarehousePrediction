from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class ForecastRequest(BaseModel):
    days: int = Field(..., gt=0, le=365, description="Количество дней для прогноза")
    current_stock: int = Field(..., ge=0, description="Текущий уровень запасов")
    avg_price: float = Field(..., gt=0, description="Средняя цена товара")
    safety_percent: float = Field(20, ge=0, le=100, description="Процент страхового запаса")
    lead_time: Optional[int] = Field(3, description="Время доставки в днях")

class ForecastResponse(BaseModel):
    forecast_demand: float
    recommended_stock: float
    current_coverage_percent: float
    safety_stock: float
    daily_forecast: list[float]