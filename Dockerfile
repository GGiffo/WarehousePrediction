FROM python:3.9-slim

WORKDIR /app

# Установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    mkdir -p /app/app/storage && \
    mkdir -p /app/data

# Копирование файлов
COPY . .

# Обучение модели при сборке (раскомментировать для production)
# RUN python train_model.py

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]