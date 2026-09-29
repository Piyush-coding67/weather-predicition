"""
config.py - Central place for settings.
If a web address, color or setting changes, we only edit it here.
"""

APP_NAME = "Weather Prediction App"

# Open-Meteo free services (no API key needed)
GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

# How many seconds to wait for the internet before giving up
REQUEST_TIMEOUT = 10

# Attribution: we must credit our data source
DATA_SOURCE = "Weather data by Open-Meteo.com"

# ---------------- Colors (dark theme) ----------------
BG_COLOR = "#0f172a"        # window background (deep navy)
CARD_COLOR = "#1e293b"      # cards (lighter navy)
INPUT_COLOR = "#0f172a"     # search box
ACCENT = "#3b82f6"          # buttons (blue)
ACCENT_HOVER = "#2563eb"    # button when the mouse is over it
MUTED_TEXT = ("#475569", "#cbd5e1")   # softer grey text (light mode, dark mode)
ERROR_COLOR = ("#dc2626", "#f87171")  # red for error messages

# ---------------- Weather themes ----------------
# Each theme has: background, card color, search-box color, button colors
THEMES = {
    "default":     {"bg": "#0f172a", "card": "#1e293b", "input": "#0f172a", "accent": "#3b82f6", "accent_hover": "#2563eb"},
    "clear_day":   {"bg": "#0e5a9e", "card": "#1976c2", "input": "#0b4a82", "accent": "#f59e0b", "accent_hover": "#d97706"},
    "clear_night": {"bg": "#0b1026", "card": "#1a2244", "input": "#070b1c", "accent": "#6366f1", "accent_hover": "#4f46e5"},
    "cloudy":      {"bg": "#3b4657", "card": "#536073", "input": "#2c3541", "accent": "#38bdf8", "accent_hover": "#0ea5e9"},
    "rain":        {"bg": "#1e3a4f", "card": "#2c5670", "input": "#16303f", "accent": "#38bdf8", "accent_hover": "#0284c7"},
    "storm":       {"bg": "#1f1b2e", "card": "#363050", "input": "#15121f", "accent": "#a78bfa", "accent_hover": "#8b5cf6"},
    "snow":        {"bg": "#4a6a8a", "card": "#6688aa", "input": "#3a5570", "accent": "#0ea5e9", "accent_hover": "#0284c7"},
    "fog":         {"bg": "#4b5563", "card": "#6b7280", "input": "#3b424c", "accent": "#14b8a6", "accent_hover": "#0d9488"},
}

# ---------------- Light-mode versions of the same themes ----------------
LIGHT_THEMES = {
    "default":     {"bg": "#e8eef7", "card": "#ffffff", "input": "#f1f5f9", "accent": "#3b82f6", "accent_hover": "#2563eb"},
    "clear_day":   {"bg": "#cfe8ff", "card": "#eaf5ff", "input": "#ffffff", "accent": "#f59e0b", "accent_hover": "#d97706"},
    "clear_night": {"bg": "#c7cdf0", "card": "#e6e9fb", "input": "#f5f6ff", "accent": "#6366f1", "accent_hover": "#4f46e5"},
    "cloudy":      {"bg": "#d5dbe3", "card": "#eef1f5", "input": "#ffffff", "accent": "#0ea5e9", "accent_hover": "#0284c7"},
    "rain":        {"bg": "#c9dfeb", "card": "#e8f3f9", "input": "#ffffff", "accent": "#0ea5e9", "accent_hover": "#0284c7"},
    "storm":       {"bg": "#d6d0ea", "card": "#efeaf9", "input": "#ffffff", "accent": "#8b5cf6", "accent_hover": "#7c3aed"},
    "snow":        {"bg": "#dbe8f5", "card": "#f4f9ff", "input": "#ffffff", "accent": "#0ea5e9", "accent_hover": "#0284c7"},
    "fog":         {"bg": "#dcdfe3", "card": "#f1f2f4", "input": "#ffffff", "accent": "#14b8a6", "accent_hover": "#0d9488"},
}