from gettext import GNUTranslations
from pathlib import Path
from typing import Literal

_DEFAULT_LOCALES_PATH: Path = Path(__file__).parents[1].joinpath('locale')
DEFAULT_LOCALES_PATH: str = _DEFAULT_LOCALES_PATH.as_posix()

def translate_with_gettext(lang: Literal['pt_BR', 'en_US']) -> GNUTranslations:
    import gettext
    gettext.bindtextdomain('app', localedir=DEFAULT_LOCALES_PATH)
    gettext.textdomain('app')

    translate = gettext.translation('app', localedir=DEFAULT_LOCALES_PATH, languages=[lang])
    
    return translate
