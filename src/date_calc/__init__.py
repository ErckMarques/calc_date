from pathlib import Path
import ttkbootstrap as ttk

ICON_PATH: Path = Path(__file__).parents[1].joinpath("assets")

type TkContainer = ttk.Window | ttk.Frame | ttk.Labelframe

from date_calc.config import config_locale_app

config_locale_app()
