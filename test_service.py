"""Temporary test: checks that weather_service.py works and handles errors."""

import weather_service


def test_city(name):
    print(f"\n--- Testing: '{name}' ---")
    try:
        city = weather_service.search_city(name)
        print("Found:", city["name"], "|", city["region"], "|", city["country"])
        weather = weather_service.get_weather(city["latitude"], city["longitude"])
        now = weather["current"]
        print("Temperature :", now["temperature"], "°C (feels like", now["feels_like"], "°C)")
        print("Humidity    :", now["humidity"], "%")
        print("Pressure    :", now["pressure"], "hPa")
        print("Wind        :", now["wind_speed"], "km/h from", now["wind_direction"], "degrees")
        print("Visibility  :", now["visibility"], "m")
        print("UV index    :", now["uv_index"])
        print("Days loaded :", len(weather["daily"]))
        print("Day 1       :", weather["daily"][0])
    except weather_service.WeatherError as error:
        print("Friendly error message ->", error)


test_city("Kathmandu")
test_city("Tokyo")
test_city("asdfghjklxyz")   # a city that does not exist
test_city("")               # empty search