import requests
import json
import csv
import datetime
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import time

# URL для API WoW
API_URL = "https://api.wowtoken.info/v1/wowtoken"

historical_data = []

def get_wow_token_price():
    """Получение текущей цены токенов WoW."""
    try:
        response = requests.get(API_URL)
        response.raise_for_status()  # Проверка на ошибки
        data = response.json()       # Декодирование JSON
        
        price = data['price']
        timestamp = data['lastUpdated']
        return price, timestamp
        
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP ошибка: {http_err}")
    except Exception as err:
        print(f"Ошибка: {err}")

def log_data(price, timestamp):
    """Запись данных в исторический массив."""
    date_time = datetime.datetime.fromtimestamp(timestamp)
    historical_data.append((date_time, price))
    print(f"Логировано: {date_time} - {price} золота")

def save_to_csv(filename):
    """Сохранение исторических данных в CSV файл."""
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Date', 'Price'])
        for data in historical_data:
            writer.writerow(data)
    print(f"Данные сохранены в {filename}")

def load_from_csv(filename):
    """Загрузка исторических данных из CSV файла."""
    global historical_data
    try:
        with open(filename, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Пропустить заголовок
            historical_data = [(datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S"), float(row[1])) for row in reader]
        print(f"Данные загружены из {filename}")
    except FileNotFoundError:
        print(f"Файл {filename} не найден.")
    except Exception as err:
        print(f"Ошибка при загрузке: {err}")

def plot_data():
    """Построение графика цен на токены."""
    if not historical_data:
        print("Нет доступных данных для построения графика.")
        return

    dates, prices = zip(*historical_data)

    plt.figure(figsize=(10, 5))
    plt.plot(dates, prices, marker='o', linestyle='-')
    plt.title('Исторические цены на WOW Token')
    plt.xlabel('Дата')
    plt.ylabel('Цена (золота)')
    plt.xticks(rotation=45)
    plt.gca().xaxis.set_major_formatter(DateFormatter('%Y-%m-%d %H:%M'))
    plt.tight_layout()
    plt.grid()
    plt.show()

def main():
    """Основная функция."""
    filename = "wow_token_price_history.csv"

    # Загрузка исторических данных из файла
    load_from_csv(filename)

    while True:
        price, timestamp = get_wow_token_price()
        if price is not None:
            log_data(price, timestamp)
            save_to_csv(filename)
            
            # Отображение графика с обновленными данными
            plot_data()
        
        # Спим перед следующим запросом
        time.sleep(3600)  # Запрос раз в час

if __name__ == "__main__":
    main()
