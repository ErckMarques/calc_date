from pathlib import Path
import ttkbootstrap as ttk

ICON_PATH: Path = Path(__file__).parents[1].joinpath("assets")

type TkContainer = ttk.Window | ttk.Frame | ttk.Labelframe

from date_calc.config import config_locale_app, translate_dict
from date_calc.translate import translate_with_gettext

config_locale_app()

t = translate_dict()

# using gettext
# _translate = translate_with_gettext(lang='pt')
# _translate.install()
# t = _translate.gettext