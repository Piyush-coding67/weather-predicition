# 🌤️ Weather Prediction App

A modern desktop weather application built with **Python**. Search for any city in the world and see its live weather, a 5-day forecast, and a colour theme that changes automatically to match the weather.

Built as a **Science Exhibition project** to show how computers collect, process and display real weather data.

---

## 📸 Screenshots

| Dark mode | Light mode |
|:---:|:---:|
| ![Dark mode](screenshots/dark-mode.png) | ![Light mode](screenshots/light-mode.png) |

---

## ✨ Features

- 🔍 **Search any city or place worldwide**
- 🌡️ **Current temperature** and weather condition with an icon
- 🤔 **Feels-like temperature**
- 💧 **Humidity**
- 💨 **Wind speed and direction** (for example "From the NW")
- 🎚️ **Atmospheric pressure**
- 👁️ **Visibility** and ☀️ **UV index** with a safety level (Low, Moderate, High...)
- 📅 **5-day forecast** with daily high/low temperature and rain chance
- 🕒 **Local time** of the searched city
- 🎨 **Dynamic weather themes**: the whole window changes colour for clear day, clear night, cloudy, rain, storm, snow and fog
- 🌗 **Light / Dark mode** switch
- ⚠️ **Friendly error messages** for empty searches, unknown cities, no internet connection and API problems
- 📝 **Data source credit** shown in the app

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| **Python 3.13** | Main programming language |
| **CustomTkinter** | Modern-looking graphical user interface |
| **Requests** | Sends requests to the weather API |
| **Open-Meteo API** | Free weather and geocoding data (no API key needed) |
| **Git & GitHub** | Version control and sharing |

---

## ⚙️ How It Works

```
   User types "Tokyo"
          │
          ▼
  ┌───────────────────┐
  │  GUI (gui/app.py) │  ← what the user sees and clicks
  └─────────┬─────────┘
            │ asks
            ▼
  ┌──────────────────────────┐
  │ weather_service.py       │  ← talks to the internet
  └─────────┬────────────────┘
            │ 1. Geocoding API: "Tokyo" → latitude & longitude
            │ 2. Forecast API: coordinates → weather data (JSON)
            ▼
  ┌───────────────────┐
  │ Open-Meteo servers │
  └─────────┬─────────┘
            │ JSON reply
            ▼
  weather_service.py cleans the data into Python dictionaries
            │
            ▼
  utils.py converts codes → words, icons, wind letters, themes
            │
            ▼
  GUI displays the cards and repaints the theme
```

1. The user types a city name.
2. The **geocoding API** converts the name into latitude and longitude.
3. The **forecast API** returns weather data for those coordinates as **JSON**.
4. Our program converts the raw data into clean Python dictionaries.
5. Helper functions translate numbers into human-friendly information (for example weather code `63` becomes "Moderate rain" with a 🌧️ icon).
6. The interface displays the results and chooses a colour theme that matches the weather.

The "brain" (`weather_service.py`) is kept separate from the "face" (`gui/`). If the data looks wrong, we check the brain; if a button looks wrong, we check the face.

---

## 📁 Project Structure

```
weather-prediction/
├── main.py              # Starts the app
├── config.py            # Settings: web addresses, colours, themes
├── weather_service.py   # Fetches and cleans weather data, handles errors
├── utils.py             # Helpers: weather codes, wind direction, unit conversion
├── gui/
│   ├── __init__.py
│   ├── app.py           # Main window and layout
│   └── cards.py         # Reusable cards (info card, forecast card)
├── assets/              # Images and icons
├── screenshots/         # Screenshots used in this README
├── test_service.py      # Tests the weather service and error handling
├── test_themes.py       # Previews every colour theme
├── requirements.txt     # Libraries needed to run the project
├── .gitignore           # Files Git should not upload
└── README.md
```

---

## 🚀 Installation

**You need:** Python 3.10 or newer (built and tested with Python 3.13) and an internet connection.

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/<repository-name>.git
cd <repository-name>
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate it

**Windows (PowerShell):**

```powershell
.\venv\Scripts\Activate.ps1
```

If Windows says "running scripts is disabled", run this once and try again:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

**Mac / Linux:**

```bash
source venv/bin/activate
```

You should now see `(venv)` at the start of your terminal line.

### 4. Install the libraries

```bash
pip install -r requirements.txt
```

---

## ▶️ How to Run

```bash
python main.py
```

Type a city name (for example `Kathmandu`, `Tokyo`, `London`, `New York` or `Sydney`) and press **Search** or the **Enter** key.

### Optional tests

```bash
python test_service.py    # checks data fetching and error messages
python test_themes.py     # previews all weather colour themes
```

---

## 🌐 API Information

This project uses the free **[Open-Meteo](https://open-meteo.com/)** services:

| Service | Used for |
|---|---|
| Geocoding API | Converts a city name into latitude and longitude |
| Forecast API | Current weather and daily forecast |

- ✅ Free for non-commercial use
- ✅ **No API key required**, so there are no secrets in this repository
- 🌍 Covers locations worldwide

**Attribution:** Weather data by [Open-Meteo.com](https://open-meteo.com/) (shown inside the app as well).

---

## 🔬 The Science Behind the Project

### What is weather?
Weather is the condition of the atmosphere at a particular place and time: temperature, humidity, air pressure, wind, cloud and precipitation.

### What is weather forecasting?
Forecasting means predicting how the atmosphere will change. Meteorologists use **weather models**: computer programs that apply the laws of physics to measurements of the atmosphere.

### How is weather data collected?
- 🌡️ Ground weather stations
- 🎈 Weather balloons
- 🛰️ Satellites
- 🌊 Ships and ocean buoys
- ✈️ Aircraft
- 📡 Radar

Professional weather services combine these measurements into models that calculate future conditions. **Our app does not build the forecast model itself.** It retrieves forecast data from Open-Meteo, which is based on such models, and presents it clearly.

### What is an API?
An **API** (Application Programming Interface) lets one program ask another program for information. It works like a waiter in a restaurant: our program places an "order" (a web address with a location and the weather values we want), and the server sends back the answer as **JSON**, a text format that Python can turn into dictionaries and lists.

### What the measurements mean

| Measurement | Unit | Meaning |
|---|---|---|
| Temperature | °C | How hot or cold the air is |
| Feels like | °C | How warm it seems to a person, affected by humidity and wind |
| Humidity | % | How much water vapour is in the air |
| Pressure | hPa | Weight of the air above us. Low pressure often brings clouds and rain; high pressure often brings clear skies |
| Wind speed | km/h | How fast the air is moving |
| Wind direction | degrees | Direction the wind comes **from** (0° = N, 90° = E, 180° = S, 270° = W) |
| Visibility | km | How far you can see |
| UV index | 0–11+ | Strength of the Sun's ultraviolet radiation |
| Rain chance | % | Probability of precipitation |

### How does the computer process the data?
1. Send a request over the internet.
2. Receive JSON data.
3. Convert it into Python dictionaries and lists.
4. Use rules and lookup tables (for example WMO weather codes) to turn numbers into descriptions, icons and themes.
5. Display the result in the interface.

### Real-world uses of weather forecasting
Farming, aviation and shipping, disaster warnings (storms, floods, heatwaves), construction, energy planning, travel, sports and everyday decisions such as carrying an umbrella.

### Why are forecasts not always 100% accurate?
The atmosphere is a **chaotic system**: tiny errors in the starting measurements grow into bigger errors over time. There are also gaps in the measurements, models work on a grid that cannot capture every hill and valley, and the further ahead we look the less certain the prediction becomes. That is why a rain chance is given as a **probability**, not a guarantee.

---

## ⚠️ Limitations

- Requires an internet connection
- Accuracy depends on the Open-Meteo data and its weather models
- Weather values are for a grid point near the searched location, not the exact spot
- The search uses the first (best) match, so cities with the same name in different countries may need a more specific search
- Temperatures are shown in Celsius only
- Weather icons use system emoji, so their look can differ between computers
- The window can pause briefly while waiting for the internet

---

## 🔮 Future Improvements

- ⏱️ Hourly forecast
- 🌅 Sunrise and sunset times
- 🔄 Refresh button and "last updated" time
- 🌡️ Celsius / Fahrenheit switch
- ⏳ Loading indicator while data downloads
- 📍 Use the current location
- 🖼️ Custom image icons and smooth animations
- 🏙️ Choose between several matching cities
- 🕘 Search history and favourite cities

---

## 👩‍🎓 Team / Student Credits

| Name | Role |
|---|---|
| Piyush Joshi | Developer |
| Abhishek Ghimire | Developer |
| Prajesh Sherpa | Researcher |
| Pratik Timalsina | Researcher |
| Ramit Dahal| Presentation Designer |

**School:** Bright Future Secondary School
**Event:** Science Exhibition _2026_
**Teacher / Guide:** Mohan G.C

---

## 🙏 Acknowledgements

- Weather data by [Open-Meteo.com](https://open-meteo.com/)
- GUI built with [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)