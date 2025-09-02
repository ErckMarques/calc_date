import sys
import ttkbootstrap as ttk
from pathlib import Path

if sys.platform.startswith("win"):
    ICON_PATH: Path = Path(__file__).parents[2].joinpath("assets", "icon")
else:
    ICON_PATH: Path = Path(__file__).parents[2].joinpath("assets", "png")

# fix this
def find_image(name: str) -> Path | str:
    """Find an image file in the icon path."""
    if sys.platform.startswith("win"):
        return ICON_PATH.joinpath(f"{name}.ico")
    return ICON_PATH.joinpath(f"{name}.png")

type TkContainer = ttk.Window | ttk.Frame | ttk.Labelframe

def main():
    from date_calc.gui.twindow import TWindow
    from date_calc.gui.frame_date_difference import FrameDateDifference
    from date_calc.gui.frame_data_interval import FrameDateWithInterval
    from date_calc import config_locale_app

    config_locale_app()
    
    window = TWindow(title="Date Calculator", themename="darkly")
    window.mainloop()

if __name__ == "__main__":
    main()