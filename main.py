"""
main.py - Start the Weather Prediction App.
Run this file to launch the program:  python main.py
"""

from gui.app import WeatherApp


if __name__ == "__main__":
    app = WeatherApp()
    app.mainloop()   # keeps the window open and listening for clicks