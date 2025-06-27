# Inventory Forecast Service

## Описание
Микросервис для прогнозирования спроса на товары и управления складскими запасами с использованием SARIMA-модели, GXBoost-модели, LSTM-модели. Сервис предоставляет REST API для:
- Прогнозирования спроса на заданный период
- Рекомендаций по оптимальному уровню запасов
- Переобучения модели на новых данных

## Технологии
- Python 3.9
- FastAPI
- Pandas
- Statsmodels (SARIMA)
- Docker

## Запуск через Docker (рекомендуется)

docker build -t inventory-service .

docker run --rm `
  -v ${PWD}/app/storage:/app/app/storage `
  -v ${PWD}/data:/app/data `
  inventory-service python train_model.py

docker run -d `
  -p 8000:8000 `
  -v ${PWD}/app/storage:/app/app/storage `
  -v ${PWD}/data:/app/data `
  --name inventory-service `
  inventory-service

## Ручная установка
bash
pip install -r requirements.txt  
python train_model.py  # Обучение модели  
uvicorn app.main:app --host 0.0.0.0 --port 8000  

## API Endpoints
GET / - **Проверка работоспособности**  
Ответ:  
json
{
  "status": "OK",
  "message": "Сервис прогнозирования запасов работает"
}


POST /forecast - **Прогнозирование запасов**  
Параметры запроса:  
json
{
  "days": 30,
  "current_stock": 500,
  "avg_price": 100,
  "safety_percent": 20
}  
Ответ:  
json
{
  "forecast_demand": 1250.45,
  "recommended_stock": 1500.54,
  "current_coverage_percent": 40.0,
  "safety_stock": 250.09,
  "daily_forecast": [41.2, 42.3, 40.5, ...]
}

POST /train - **Обучение модели**
Ответ:  
json
{
  "status": "success",
  "message": "Модель успешно обучена"
}