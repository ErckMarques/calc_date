from gettext import GNUTranslations
from pathlib import Path
from typing import Literal

LOCALE_PATH_DIR: str = Path(__file__).parent.joinpath('locale').as_posix()

def translate_with_gettext(lang: Literal['pt', 'en']) -> GNUTranslations:
    import gettext
    gettext.bindtextdomain('app', localedir=LOCALE_PATH_DIR)
    gettext.textdomain('app')

    translate = gettext.translation('app', localedir=LOCALE_PATH_DIR, languages=lang)
    
    return translate
