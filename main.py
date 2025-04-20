import argparse
from weather_api import get_weather

def display_weather(data: dict):
    if "error" in data:
        print(f"[!] Ошибка: {data['error']}")
    else:
        print(f"\nПогода в {data['city']}:")
        print(f"  Температура: {data['temperature']}°C")
        print(f"  Описание: {data['description'].capitalize()}")
        print("-" * 30)

def main():
    parser = argparse.ArgumentParser(description="Узнай текущую погоду в любом городе.")
    parser.add_argument("city", help="Название города, для которого нужно получить погоду.")
    parser.add_argument("--key", required=True, help="Ваш API-ключ от OpenWeatherMap.")

    args = parser.parse_args()

    print(f"[DEBUG] Запрашиваем погоду для города: {args.city}")
    
    weather_data = get_weather(args.city, args.key)
    
    display_weather(weather_data)

if __name__ == "__main__":
    main()