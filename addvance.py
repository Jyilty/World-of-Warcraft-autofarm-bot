import requests
import pandas as pd

# URL для API WoW
API_URL = "https://api.github.com/gists/public"  # Здесь можно использовать API для квестов, если доступно

def get_current_events(region="us", faction="all"):
    """
    Получение текущих квестов и событий в WoW.
    :param region: Регион (по умолчанию 'us').
    :param faction: Фракция (по умолчанию 'all').
    :return: Список квестов.
    """
    try:
        # Здесь нужно будет заменить на реальный API WoW, если таковой имеется
        response = requests.get(API_URL)
        response.raise_for_status()  # Проверка на ошибки
        events = response.json()     # Декодирование JSON

        # Фильтрация событий по фракции (если нужно)
        if faction != "all":
            events = [event for event in events if event["faction"] == faction]

        return events

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP ошибка: {http_err}")
    except Exception as err:
        print(f"Ошибка: {err}")
        
    return []

def save_events_to_csv(events, filename="current_events.csv"):
    """
    Сохранение событий в CSV файл.
    :param events: Список событий.
    :param filename: Имя файла для сохранения.
    """
    df = pd.DataFrame(events)
    df.to_csv(filename, index=False)
    print(f"Данные сохранены в {filename}")

def main():
    region = input("Введите регион (например, 'us'): ")
    faction = input("Введите фракцию (например, 'all', 'horde', 'alliance'): ")

    print("Получение текущих квестов и событий...")
    events = get_current_events(region, faction)

    if events:
        print("Найдены квесты:")
        for event in events:
            print(f"{event['name']} - {event['description']}")
        
        save_events_to_csv(events)
    else:
        print("Квесты не найдены.")

if __name__ == "__main__":
    main()
