"""
This module provides a function for compiling the '.mo' binary files, used by gettext, through the "polib" lib.
"""
import polib
from pathlib import Path
from typing import cast, TypeAlias, Optional

from date_calc.translate.raises import IsNotPOFileError

StrOrPath: TypeAlias = Path | str

def _validate_locale_path(p: StrOrPath) -> Path:
    """Validates that the path to the 'locale' folder is valid."""

    if not isinstance(p, (str, Path)):
        msg = "The 'path' argument must be of type 'str' or 'Path'."
        raise TypeError(msg)
    
    if isinstance(p, str):
        try:
            p = Path(p).resolve()
        except Exception as e:
            msg = f"Error resolving path: {e}"
            raise ValueError(msg)
    
    if not p.exists() or not p.is_dir():
        msg = f"Invalid path: '{p}'. Directory does not exist or not an accessible directory."
        raise FileNotFoundError(msg)

    return p

def _validate_pofile_path(p: StrOrPath) -> Path:
    """Validates that the 'locale' directory structure complies with the 'gettext' specification."""

    locale = _validate_locale_path(p)

    pofile = locale.joinpath('LC_MESSAGES', 'app.po')

    if not pofile.exists() or not pofile.is_file():
        msg = f"Invalid path: '{p}'. File does not exist or is not an accessible file."
        raise FileNotFoundError(msg)

    if pofile.suffix != '.po':
        msg = f"The passed file is not of type '.po', \nPath: {pofile.as_posix()}"
        raise IsNotPOFileError(msg)

    return pofile

def _compile_po_2_mo(po_file: StrOrPath):
    """
    This function takes a string or a pathlib.Path object,
    representing the path of the '.po' file and saves it in the same folder or path.

    Args:
        po_file (StrOrPathPOFile: TypeAlias = Path | str): file path
        domain(str): file name

    """
    file = _validate_locale_path(po_file)
        
    
    mo_file: str = file.with_suffix(".mo").as_posix()
    nfile: polib.POFile = polib.pofile(file)
    nfile.save_as_mofile(mo_file)

def compile_po_2_mo(locale_path: StrOrPath, domain: str = 'app'):
    """
    This function takes a string or a pathlib.Path object,
    representing the path of the '.po' file and saves it in the same folder or path.

    Args:
        locale_path (StrOrPath): Path to the 'locale' folder containing the .po files
        domain(str): file name
    """
    try:
        if locale_path is None:
            # calc_dates\src\date_calc\locale
            LOCALE_DIR = Path(__file__).parents[2].joinpath('locale')

            # calc_dates\src\date_calc\locale\pt
            for dir in LOCALE_DIR.iterdir():
                # calc_dates\src\date_calc\locale\pt\LC_MESSAGES\app.po
                _compile_po_2_mo(dir.joinpath('LC_MESSAGES', 'app.po'))
        else:
            for dir in locale_path.iterdir():
                po_file = dir.joinpath('LC_MESSAGES', f'{domain}.po')
                if not po_file.exists():
                    msg = f"No '.po' file found in the path: {po_file.as_posix()}"
                    raise FileNotFoundError(msg)
            _compile_po_2_mo(po_file, domain)
    except Exception as e:
        raise e

if __name__ == "__main__":
    compile_po_2_mo()