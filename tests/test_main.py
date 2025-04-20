import pytest
import requests
from unittest.mock import patch, MagicMock
import weather_api

@patch("weather_api.requests.get")
def test_get_weather_success(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "cod": 200,
        "name": "London",
        "main": {"temp": 10},
        "weather": [{"description": "clear sky"}]
    }
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = weather_api.get_weather("London", "fake_api_key")
    assert result["city"] == "London"
    assert result["temperature"] == 10
    assert result["description"] == "clear sky"

@patch("weather_api.requests.get")
def test_get_weather_api_error(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {"cod": "404", "message": "city not found"}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = weather_api.get_weather("UnknownCity", "fake_api_key")
    assert "error" in result
    assert result["error"] == "city not found"

@patch("weather_api.requests.get", side_effect=requests.exceptions.ConnectionError)
def test_get_weather_connection_error(mock_get):
    result = weather_api.get_weather("London", "fake_api_key")
    assert "Ошибка соединения" in result["error"]

def test_get_weather_empty_city():
    with pytest.raises(ValueError):
        weather_api.get_weather("", "fake_api_key")

def test_get_weather_invalid_city_type():
    with pytest.raises(AttributeError):
        weather_api.get_weather(None, "fake_api_key")

@patch("weather_api.requests.get", side_effect=Exception("Test error log"))
def test_logging_error_written(mock_get, tmp_path):
    log_file = tmp_path / "error.log"

    import logging
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    logging.basicConfig(filename=log_file, level=logging.ERROR)

    weather_api.get_weather("City", "fake_api_key")

    with open(log_file, "r", encoding="utf-8") as f:
        logs = f.read()

    assert "Test error log" in logs
