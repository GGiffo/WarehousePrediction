from app.models import SarimaModel

if __name__ == "__main__":
    print("Обучение SARIMA модели...")
    model = SarimaModel()
    model.train("data/3_year_product_demand_dataset.csv")
    print("Модель успешно обучена и сохранена")