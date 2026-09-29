"""Temporary test: shows every theme, changing every 2 seconds."""

from gui.app import WeatherApp

app = WeatherApp()
app.welcome_label.pack_forget()          # hide the welcome text
app.content_frame.pack(fill="x")         # show the (empty) cards

names = list(__import__("config").THEMES.keys())
state = {"i": 0}

def next_theme():
    name = names[state["i"] % len(names)]
    app.apply_theme(name)
    app.title(f"Theme: {name}")
    state["i"] += 1
    if state["i"] <= len(names):
        app.after(2000, next_theme)

next_theme()
app.mainloop()