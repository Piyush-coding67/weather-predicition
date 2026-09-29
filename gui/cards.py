"""
gui/cards.py - Reusable card widgets.
InfoCard     -> small card showing one measurement (humidity, wind, ...)
ForecastCard -> small card showing one day of the forecast
"""

import customtkinter as ctk

import config


class InfoCard(ctk.CTkFrame):
    """A card with a title, a big value, and a small detail line."""

    def __init__(self, parent, title, icon):
        super().__init__(parent, corner_radius=16, fg_color=config.CARD_COLOR)

        self.title_label = ctk.CTkLabel(
            self, text=f"{icon}  {title}",
            font=ctk.CTkFont(size=13), text_color=config.MUTED_TEXT,
        )
        self.title_label.pack(anchor="w", padx=16, pady=(14, 0))

        self.value_label = ctk.CTkLabel(
            self, text="--", font=ctk.CTkFont(size=28, weight="bold"),
        )
        self.value_label.pack(anchor="w", padx=16, pady=(2, 0))

        self.detail_label = ctk.CTkLabel(
            self, text="", font=ctk.CTkFont(size=12), text_color=config.MUTED_TEXT,
        )
        self.detail_label.pack(anchor="w", padx=16, pady=(0, 14))

    def set_value(self, value, detail=""):
        """Update what the card displays."""
        self.value_label.configure(text=value)
        self.detail_label.configure(text=detail)

    def set_color(self, color):
        """Change the card's background color."""
        self.configure(fg_color=color)


class ForecastCard(ctk.CTkFrame):
    """A card for one forecast day: name, icon, high/low, rain chance."""

    def __init__(self, parent):
        super().__init__(parent, corner_radius=16, fg_color=config.CARD_COLOR)

        self.day_label = ctk.CTkLabel(
            self, text="--", font=ctk.CTkFont(size=15, weight="bold"),
        )
        self.day_label.pack(pady=(14, 0))

        self.icon_label = ctk.CTkLabel(
            self, text="", font=ctk.CTkFont(family="Segoe UI Emoji", size=36),
        )
        self.icon_label.pack(pady=4)

        self.temp_label = ctk.CTkLabel(
            self, text="--", font=ctk.CTkFont(size=15, weight="bold"),
        )
        self.temp_label.pack()

        self.rain_label = ctk.CTkLabel(
            self, text="", font=ctk.CTkFont(size=12), text_color=config.MUTED_TEXT,
        )
        self.rain_label.pack(pady=(0, 14))

    def set_data(self, day_name, icon, high_text, low_text, rain_text):
        """Update what the card displays."""
        self.day_label.configure(text=day_name)
        self.icon_label.configure(text=icon)
        self.temp_label.configure(text=f"{high_text} / {low_text}")
        self.rain_label.configure(text=f"💧 {rain_text}")

    def set_color(self, color):
        """Change the card's background color."""
        self.configure(fg_color=color)