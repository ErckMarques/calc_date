import logging

from pathlib import Path
ICON_PATH: Path = Path(__file__).parent.joinpath("assets")


import ttkbootstrap as ttk
type TkContainer = ttk.Window | ttk.Frame | ttk.Labelframe


from rich.traceback import install
try:
    install(show_locals=True)
    logging.info("Rich traceback installed successfully.")
except Exception as e:
    logging.warning(f"Failed to install rich traceback: {e}")


from date_calc.config import config_locale_app
config_locale_app()


import gettext
from date_calc.translate import translate_with_gettext
try:
    # using gettext
    _translate = translate_with_gettext(lang='pt_BR')
    _translate.install()
    t = _translate.gettext
except FileNotFoundError as e:
    logging.warning(f"Translation files not found. Using NullTranslations. Error: {e}")
    t = gettext.NullTranslations().gettext
except Exception as e:
    logging.warning(f"Error loading translations: {e}")
    t = gettext.NullTranslations().gettext