import requests
import logging

logging.basicConfig(filename="error.log", level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

def get_weather(city: str, api_key: str) -> dict:
    if not isinstance(city, str):
        error_msg = "Тип города должен быть строкой"
        logging.error(error_msg)
        raise AttributeError(error_msg)

    if not city.strip():
        error_msg = "Город не может быть пустым"
        logging.error(error_msg)
        raise ValueError(error_msg)

    try:
        url = f"https://api.openweathermap.org/data/2.5/weather"
        params = {"q": city, "appid": api_key, "units": "metric", "lang": "en"}
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if data.get("cod") != 200:
            error_msg = data.get("message", "Неизвестная ошибка")
            logging.error(f"API error: {error_msg}")
            return {"error": error_msg}

        return {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"]
        }

    except requests.exceptions.HTTPError:
        logging.error("HTTP error occurred")
        return {"error": "Ошибка HTTP. Проверьте API-ключ или город."}
    except requests.exceptions.ConnectionError:
        logging.error("Connection error occurred")
        return {"error": "Ошибка соединения. Проверьте интернет-соединение."}
    except requests.exceptions.Timeout:
        logging.error("Timeout occurred")
        return {"error": "Время ожидания запроса истекло."}
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return {"error": f"Произошла ошибка: {e}"}
