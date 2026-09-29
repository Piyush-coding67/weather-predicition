"""
gui/app.py - The main window of the Weather Prediction App.

This file handles what the user SEES and CLICKS.
All data fetching is done by weather_service.py, and all
translating (codes -> words/icons/themes) is done by utils.py.
"""

import customtkinter as ctk

import config
import utils
import weather_service
from gui.cards import InfoCard, ForecastCard


class WeatherApp(ctk.CTk):
    """The main application window."""

    def __init__(self):
        super().__init__()

        # ---- Window settings ----
        ctk.set_appearance_mode("dark")
        self.title(config.APP_NAME)
        self.geometry("980x780")
        self.minsize(760, 600)

        self.has_results = False        # becomes True after the first successful search
        self.mode = "dark"              # NEW: "dark" or "light"
        self.current_theme = "default"  # NEW: remembers which weather theme is active

        self.build_ui()
        self.apply_theme("default")

    # -----------------------------------------------------------
    # Building the interface
    # -----------------------------------------------------------
    def build_ui(self):
        """Create the page and all its sections, top to bottom."""

        # A scrollable page: if the window is small, the user can scroll down
        self.page = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.page.pack(fill="both", expand=True, padx=10, pady=10)

        self.build_header()
        self.build_search_section()

        # Message line (used for errors and "Searching...")
        self.message_label = ctk.CTkLabel(
            self.page, text="", font=ctk.CTkFont(size=14),
            text_color=config.MUTED_TEXT, wraplength=700,
        )
        self.message_label.pack(pady=(10, 0))

        # Welcome text, shown until the first successful search
        self.welcome_label = ctk.CTkLabel(
            self.page, text="🌍  Search for a city to see its weather",
            font=ctk.CTkFont(size=22), text_color=config.MUTED_TEXT,
        )
        self.welcome_label.pack(pady=80)

        # All the weather cards live in this frame (hidden until we have data)
        self.content_frame = ctk.CTkFrame(self.page, fg_color="transparent")
        self.build_main_card()
        self.build_info_cards()
        self.build_forecast_section()

    def build_header(self):
        # CHANGED: two columns - title on the left, light/dark switch on the right
        header = ctk.CTkFrame(self.page, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(10, 0))
        header.grid_columnconfigure(0, weight=1)

        title_column = ctk.CTkFrame(header, fg_color="transparent")
        title_column.grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(
            title_column, text="🌤️  Weather Prediction App",
            font=ctk.CTkFont(size=30, weight="bold"),
        ).pack(anchor="w")

        ctk.CTkLabel(
            title_column, text="Live forecasts for any city in the world",
            font=ctk.CTkFont(size=14), text_color=config.MUTED_TEXT,
        ).pack(anchor="w")

        # NEW: the light/dark switch
        self.mode_switch = ctk.CTkSwitch(
            header, text="Light mode", font=ctk.CTkFont(size=14),
            command=self.toggle_mode,
        )
        self.mode_switch.grid(row=0, column=1, sticky="e")

    def build_search_section(self):
        self.search_card = ctk.CTkFrame(self.page, corner_radius=16, fg_color=config.CARD_COLOR)
        self.search_card.pack(fill="x", padx=20, pady=(18, 0))
        self.search_card.grid_columnconfigure(0, weight=1)   # search box stretches

        self.search_entry = ctk.CTkEntry(
            self.search_card, height=44, border_width=0, fg_color=config.INPUT_COLOR,
            placeholder_text="Search a city, e.g. Kathmandu, Tokyo, London...",
            font=ctk.CTkFont(size=15),
        )
        self.search_entry.grid(row=0, column=0, sticky="ew", padx=(16, 10), pady=14)

        self.search_button = ctk.CTkButton(
            self.search_card, text="Search", width=110, height=44,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color=config.ACCENT, hover_color=config.ACCENT_HOVER,
            command=self.search_weather,
        )
        self.search_button.grid(row=0, column=1, padx=(0, 16), pady=14)

        # Pressing the Enter key also starts a search
        self.search_entry.bind("<Return>", lambda event: self.search_weather())

    def build_main_card(self):
        """The big card: city, icon, temperature, condition."""
        self.main_card = ctk.CTkFrame(self.content_frame, corner_radius=24, fg_color=config.CARD_COLOR)
        self.main_card.pack(fill="x", padx=20)

        self.city_label = ctk.CTkLabel(self.main_card, text="", font=ctk.CTkFont(size=28, weight="bold"))
        self.city_label.pack(anchor="w", padx=28, pady=(22, 0))

        self.time_label = ctk.CTkLabel(
            self.main_card, text="", font=ctk.CTkFont(size=14), text_color=config.MUTED_TEXT,
        )
        self.time_label.pack(anchor="w", padx=28)

        row = ctk.CTkFrame(self.main_card, fg_color="transparent")
        row.pack(anchor="w", padx=28, pady=(10, 0))

        self.icon_label = ctk.CTkLabel(row, text="", font=ctk.CTkFont(family="Segoe UI Emoji", size=84))
        self.icon_label.pack(side="left", padx=(0, 24))

        text_column = ctk.CTkFrame(row, fg_color="transparent")
        text_column.pack(side="left")

        self.temperature_label = ctk.CTkLabel(text_column, text="", font=ctk.CTkFont(size=72, weight="bold"))
        self.temperature_label.pack(anchor="w")

        self.condition_label = ctk.CTkLabel(text_column, text="", font=ctk.CTkFont(size=22))
        self.condition_label.pack(anchor="w")

        self.summary_label = ctk.CTkLabel(
            self.main_card, text="", font=ctk.CTkFont(size=15), text_color=config.MUTED_TEXT,
        )
        self.summary_label.pack(anchor="w", padx=28, pady=(8, 22))

    def build_info_cards(self):
        """Six small cards in a 3-column grid."""
        info_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        info_frame.pack(fill="x", padx=14, pady=(14, 0))

        for column in range(3):
            info_frame.grid_columnconfigure(column, weight=1, uniform="info")

        definitions = [
            ("feels_like", "Feels like", "🌡️"),
            ("humidity", "Humidity", "💧"),
            ("wind", "Wind", "💨"),
            ("pressure", "Pressure", "🎚️"),
            ("visibility", "Visibility", "👁️"),
            ("uv", "UV index", "☀️"),
        ]

        self.info_cards = {}
        for i, (key, title, icon) in enumerate(definitions):
            card = InfoCard(info_frame, title, icon)
            card.grid(row=i // 3, column=i % 3, sticky="nsew", padx=6, pady=6)
            self.info_cards[key] = card

    def build_forecast_section(self):
        """Five cards, one for each forecast day."""
        ctk.CTkLabel(
            self.content_frame, text="5-Day Forecast",
            font=ctk.CTkFont(size=20, weight="bold"),
        ).pack(anchor="w", padx=20, pady=(18, 4))

        forecast_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        forecast_frame.pack(fill="x", padx=14)

        for column in range(5):
            forecast_frame.grid_columnconfigure(column, weight=1, uniform="forecast")

        self.forecast_cards = []
        for column in range(5):
            card = ForecastCard(forecast_frame)
            card.grid(row=0, column=column, sticky="nsew", padx=6, pady=6)
            self.forecast_cards.append(card)

        # Data source credit at the bottom
        ctk.CTkLabel(
            self.content_frame, text=config.DATA_SOURCE,
            font=ctk.CTkFont(size=12), text_color=config.MUTED_TEXT,
        ).pack(pady=(14, 10))

    # -----------------------------------------------------------
    # Colors: weather theme + light/dark mode
    # -----------------------------------------------------------
    def apply_theme(self, theme_name):
        """Repaint the window using a weather theme in the current light/dark mode."""
        # CHANGED: choose the light or dark set of themes
        palette = config.LIGHT_THEMES if self.mode == "light" else config.THEMES
        theme = palette.get(theme_name, palette["default"])
        self.current_theme = theme_name   # NEW: remember it for when the mode changes

        self.configure(fg_color=theme["bg"])
        self.page.configure(fg_color=theme["bg"])
        self.search_card.configure(fg_color=theme["card"])
        self.search_entry.configure(fg_color=theme["input"])
        self.search_button.configure(fg_color=theme["accent"], hover_color=theme["accent_hover"])
        self.main_card.configure(fg_color=theme["card"])

        for card in self.info_cards.values():
            card.set_color(theme["card"])
        for card in self.forecast_cards:
            card.set_color(theme["card"])

    def toggle_mode(self):
        """NEW: called when the user flips the light/dark switch."""
        self.mode = "light" if self.mode_switch.get() == 1 else "dark"
        ctk.set_appearance_mode(self.mode)      # switches text colors automatically
        self.apply_theme(self.current_theme)    # repaint the same weather theme

    # -----------------------------------------------------------
    # What happens when the user searches
    # -----------------------------------------------------------
    def search_weather(self):
        """Read the search box, fetch the weather, and show the result."""
        city_name = self.search_entry.get()

        self.show_message("Searching...", config.MUTED_TEXT)
        self.update_idletasks()   # redraw the window right now

        try:
            city = weather_service.search_city(city_name)
            weather = weather_service.get_weather(city["latitude"], city["longitude"])
        except weather_service.WeatherError as error:
            # Our service gives friendly messages, so we just display them
            self.show_message(str(error), config.ERROR_COLOR)
            return

        self.show_message("", config.MUTED_TEXT)
        self.show_weather(city, weather)

    def show_weather(self, city, weather):
        """Put the fetched data into all the labels and cards."""
        current = weather["current"]
        today = weather["daily"][0]

        # First successful search: hide the welcome text, reveal the cards
        if not self.has_results:
            self.welcome_label.pack_forget()
            self.content_frame.pack(fill="x")
            self.has_results = True

        # Pick and apply the theme that matches this weather
        theme_name = utils.get_theme_name(current["weather_code"], current["is_day"])
        self.apply_theme(theme_name)

        description, icon = utils.describe_weather(current["weather_code"], current["is_day"])

        place = city["name"]
        if city["country"]:
            place += f", {city['country']}"

        # ---- Main card ----
        self.city_label.configure(text=place)
        self.time_label.configure(text="Local time: " + utils.format_local_datetime(current["time"]))
        self.icon_label.configure(text=icon)
        self.temperature_label.configure(text=utils.format_temperature(current["temperature"]))
        self.condition_label.configure(text=description)
        self.summary_label.configure(
            text=(
                f"High {utils.format_temperature(today['temp_max'])}   ·   "
                f"Low {utils.format_temperature(today['temp_min'])}   ·   "
                f"Rain chance {today['rain_chance']}%"
            )
        )

        # ---- Information cards ----
        self.info_cards["feels_like"].set_value(
            utils.format_temperature(current["feels_like"]),
            f"Actual: {utils.format_temperature(current['temperature'])}",
        )
        self.info_cards["humidity"].set_value(
            f"{current['humidity']}%", "Moisture in the air",
        )
        direction = utils.wind_direction_to_text(current["wind_direction"])
        self.info_cards["wind"].set_value(
            f"{round(current['wind_speed'])} km/h",
            f"From the {direction} ({round(current['wind_direction'])}°)",
        )
        self.info_cards["pressure"].set_value(
            f"{round(current['pressure'])} hPa", "Sea-level pressure",
        )

        # Visibility and UV can be missing (None), so we check first
        if current["visibility"] is None:
            self.info_cards["visibility"].set_value("N/A", "Not available")
        else:
            self.info_cards["visibility"].set_value(
                f"{current['visibility'] / 1000:.1f} km", "How far you can see",
            )

        if current["uv_index"] is None:
            self.info_cards["uv"].set_value("N/A", "Not available")
        else:
            self.info_cards["uv"].set_value(
                f"{current['uv_index']:.1f}", utils.describe_uv(current["uv_index"]),
            )

        # ---- Forecast cards ----
        for index, (card, day) in enumerate(zip(self.forecast_cards, weather["daily"])):
            _, day_icon = utils.describe_weather(day["weather_code"], True)
            rain = day["rain_chance"]
            card.set_data(
                day_name=utils.format_day_name(day["date"], index),
                icon=day_icon,
                high_text=utils.format_temperature(day["temp_max"]),
                low_text=utils.format_temperature(day["temp_min"]),
                rain_text="--" if rain is None else f"{rain}%",
            )

    def show_message(self, text, color):
        """Update the message line under the search box."""
        self.message_label.configure(text=text, text_color=color)