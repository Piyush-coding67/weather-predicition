"""
weather_service.py - Talks to the Open-Meteo API and returns clean data.

Two steps happen here:
  1. Geocoding: city name  -> latitude & longitude
  2. Forecast:  coordinates -> weather data

This file knows nothing about buttons or windows. It only fetches data.
"""

import requests

import config


# ---------------------------------------------------------------
# Custom errors: each one has a friendly message for the user
# ---------------------------------------------------------------
class WeatherError(Exception):
    """Base class for all errors in our weather service."""


class EmptySearchError(WeatherError):
    """The user pressed Search without typing anything."""


class CityNotFoundError(WeatherError):
    """The API could not find a place with that name."""


class NetworkError(WeatherError):
    """No internet connection, or the server took too long to reply."""


class APIError(WeatherError):
    """The server replied, but with an error or unexpected data."""


# ---------------------------------------------------------------
# Helper: send a request and return the JSON reply as a dictionary
# ---------------------------------------------------------------
def _get_json(url, params):
    try:
        response = requests.get(url, params=params, timeout=config.REQUEST_TIMEOUT)
    except requests.exceptions.Timeout:
        raise NetworkError("The server took too long to respond. Please try again.")
    except requests.exceptions.ConnectionError:
        raise NetworkError("No internet connection. Please check your network.")
    except requests.exceptions.RequestException:
        raise APIError("Something went wrong while contacting the weather service.")

    # 200 means success; anything else means the API had a problem
    if response.status_code != 200:
        raise APIError(f"Weather service error (code {response.status_code}).")

    try:
        return response.json()
    except ValueError:
        raise APIError("The weather service sent data we could not read.")


# ---------------------------------------------------------------
# Step 1: city name -> coordinates
# ---------------------------------------------------------------
def search_city(city_name):
    """Return a dictionary with the city's name, country, latitude, longitude."""
    city_name = city_name.strip()
    if not city_name:
        raise EmptySearchError("Please type a city name first.")

    params = {"name": city_name, "count": 1, "language": "en", "format": "json"}
    data = _get_json(config.GEOCODING_URL, params)

    # If nothing matches, the API sends no "results" key at all
    results = data.get("results")
    if not results:
        raise CityNotFoundError(f"Could not find a place called '{city_name}'.")

    place = results[0]
    return {
        "name": place.get("name", city_name),
        "region": place.get("admin1", ""),      # state / province
        "country": place.get("country", ""),
        "latitude": place["latitude"],
        "longitude": place["longitude"],
    }


# ---------------------------------------------------------------
# Step 2: coordinates -> weather
# ---------------------------------------------------------------
def get_weather(latitude, longitude):
    """Fetch current weather and a 5-day daily forecast, as clean Python data."""
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": ",".join([
            "temperature_2m", "apparent_temperature", "relative_humidity_2m",
            "pressure_msl", "wind_speed_10m", "wind_direction_10m",
            "weather_code", "is_day", "visibility", "uv_index",
        ]),
        "daily": ",".join([
            "weather_code", "temperature_2m_max", "temperature_2m_min",
            "precipitation_probability_max", "sunrise", "sunset", "uv_index_max",
        ]),
        "timezone": "auto",       # use the local time of the searched place
        "forecast_days": 5,
    }
    data = _get_json(config.FORECAST_URL, params)

    # Convert the raw reply into a tidy structure our GUI can use easily
    try:
        current = data["current"]
        daily = data["daily"]

        weather = {
            "timezone": data["timezone"],
            "current": {
                "time": current["time"],
                "temperature": current["temperature_2m"],          # °C
                "feels_like": current["apparent_temperature"],     # °C
                "humidity": current["relative_humidity_2m"],       # %
                "pressure": current["pressure_msl"],               # hPa
                "wind_speed": current["wind_speed_10m"],           # km/h
                "wind_direction": current["wind_direction_10m"],   # degrees
                "weather_code": current["weather_code"],
                "is_day": current["is_day"] == 1,
                "visibility": current.get("visibility"),           # metres (may be None)
                "uv_index": current.get("uv_index"),               # may be None
            },
            "daily": [],
        }

        # Build one small dictionary per day
        for i in range(len(daily["time"])):
            weather["daily"].append({
                "date": daily["time"][i],
                "weather_code": daily["weather_code"][i],
                "temp_max": daily["temperature_2m_max"][i],
                "temp_min": daily["temperature_2m_min"][i],
                "rain_chance": daily["precipitation_probability_max"][i],
                "sunrise": daily["sunrise"][i],
                "sunset": daily["sunset"][i],
                "uv_index_max": daily["uv_index_max"][i],
            })
        return weather

    except (KeyError, IndexError, TypeError):
        raise APIError("The weather data was in an unexpected format.")