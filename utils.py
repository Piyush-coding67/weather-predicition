"""
utils.py - Small helper functions used by the rest of the app.
"""
from datetime import datetime

# WMO weather codes -> (description, day icon, night icon)
# These codes are an international standard used by weather services.
WEATHER_CODES = {
    0:  ("Clear sky", "☀️", "🌙"),
    1:  ("Mainly clear", "🌤️", "🌙"),
    2:  ("Partly cloudy", "⛅", "☁️"),
    3:  ("Overcast", "☁️", "☁️"),
    45: ("Fog", "🌫️", "🌫️"),
    48: ("Freezing fog", "🌫️", "🌫️"),
    51: ("Light drizzle", "🌦️", "🌧️"),
    53: ("Moderate drizzle", "🌦️", "🌧️"),
    55: ("Dense drizzle", "🌧️", "🌧️"),
    56: ("Light freezing drizzle", "🌧️", "🌧️"),
    57: ("Dense freezing drizzle", "🌧️", "🌧️"),
    61: ("Light rain", "🌦️", "🌧️"),
    63: ("Moderate rain", "🌧️", "🌧️"),
    65: ("Heavy rain", "🌧️", "🌧️"),
    66: ("Light freezing rain", "🌧️", "🌧️"),
    67: ("Heavy freezing rain", "🌧️", "🌧️"),
    71: ("Light snow", "🌨️", "🌨️"),
    73: ("Moderate snow", "❄️", "❄️"),
    75: ("Heavy snow", "❄️", "❄️"),
    77: ("Snow grains", "❄️", "❄️"),
    80: ("Light rain showers", "🌦️", "🌧️"),
    81: ("Moderate rain showers", "🌧️", "🌧️"),
    82: ("Violent rain showers", "⛈️", "⛈️"),
    85: ("Light snow showers", "🌨️", "🌨️"),
    86: ("Heavy snow showers", "🌨️", "🌨️"),
    95: ("Thunderstorm", "⛈️", "⛈️"),
    96: ("Thunderstorm with light hail", "⛈️", "⛈️"),
    99: ("Thunderstorm with heavy hail", "⛈️", "⛈️"),
}


def describe_weather(code, is_day=True):
    """Turn a weather code into (description, icon).
    Uses a moon icon at night where it makes sense."""
    description, day_icon, night_icon = WEATHER_CODES.get(code, ("Unknown", "❓", "❓"))
    icon = day_icon if is_day else night_icon
    return description, icon


def wind_direction_to_text(degrees):
    """Turn a compass angle (0-360) into letters like 'NW'.
    The circle is split into 8 slices of 45 degrees each."""
    names = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    index = round(degrees / 45) % 8
    return names[index]


def celsius_to_fahrenheit(celsius):
    """Formula: F = C x 9/5 + 32"""
    return celsius * 9 / 5 + 32


def format_temperature(celsius, unit="C"):
    """Return text like '27°C' or '80°F', rounded to a whole number."""
    if unit == "F":
        return f"{round(celsius_to_fahrenheit(celsius))}°F"
    return f"{round(celsius)}°C"

def format_day_name(date_text, index):
    """'2026-09-30' -> 'Wed'. The first day is shown as 'Today'."""
    if index == 0:
        return "Today"
    return datetime.strptime(date_text, "%Y-%m-%d").strftime("%a")


def format_local_datetime(iso_text):
    """'2026-09-29T12:45' -> 'Tuesday, 29 September  ·  12:45 PM'"""
    moment = datetime.strptime(iso_text, "%Y-%m-%dT%H:%M")
    return moment.strftime("%A, %d %B") + "  ·  " + moment.strftime("%I:%M %p").lstrip("0")


def describe_uv(uv_index):
    """Turn the UV number into a safety level (World Health Organization scale)."""
    if uv_index is None:
        return ""
    if uv_index < 3:
        return "Low"
    if uv_index < 6:
        return "Moderate"
    if uv_index < 8:
        return "High"
    if uv_index < 11:
        return "Very high"
    return "Extreme"

def get_theme_name(code, is_day):
    """Decide which color theme matches the weather code (and day/night)."""
    if code in (0, 1, 2):
        return "clear_day" if is_day else "clear_night"
    if code == 3:
        return "cloudy"
    if code in (45, 48):
        return "fog"
    if code in (51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82):
        return "rain"
    if code in (71, 73, 75, 77, 85, 86):
        return "snow"
    if code in (95, 96, 99):
        return "storm"
    return "default"