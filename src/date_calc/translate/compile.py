"""
This module provides a function for compiling the '.mo' binary files, used by gettext, through the "polib" lib.
"""
import polib
from pathlib import Path
from typing import cast, TypeAlias, Optional

from date_calc.translate.raises import IsNotPOFileError

StrOrPathPOFile: TypeAlias = Path | str

def _compile_po_2_mo(po_file: StrOrPathPOFile, domain: str = 'app'):
    """
    This function takes a string or a pathlib.Path object,
    representing the path of the '.po' file and saves it in the same folder or path.

    Args:
        po_file (StrOrPathPOFile: TypeAlias = Path | str): file path
        domain(str): file name

    """
    if isinstance(po_file, str):
        file = Path(po_file)

    file = cast(Path, po_file)

    if isinstance(file, Path):
        if not file.is_file() or not file.exists():
            msg = f"Passed argument is either not a file or does not exist. \nPath: {file.as_posix()}"
            raise FileNotFoundError(msg)
        
    if file.suffix != '.po':
        msg = f"The passed file is not of type '.po', \nPath: {file.as_posix()}"
        raise IsNotPOFileError(msg)
    
    mo_file = file.with_suffix(".mo").as_posix()
    nfile = polib.pofile(file)
    nfile.save_as_mofile(mo_file)

def compile_po_2_mo(po_file: Optional[StrOrPathPOFile] = None, domain: str = 'app'):
    """
    This function takes a string or a pathlib.Path object,
    representing the path of the '.po' file and saves it in the same folder or path.

    Args:
        po_file (StrOrPathPOFile: TypeAlias = Path | str): file path
        domain(str): file name
    """
    try:
        if po_file is None:
            # calc_dates\src\date_calc\locale
            LOCALE_DIR = Path(__file__).parents[2].joinpath('locale')

            # calc_dates\src\date_calc\locale\pt
            for dir in LOCALE_DIR.iterdir():
                # calc_dates\src\date_calc\locale\pt\LC_MESSAGES\app.po
                _compile_po_2_mo(dir.joinpath('LC_MESSAGES', 'app.po'))
        else:
            _compile_po_2_mo(po_file, domain)
    except Exception as e:
        raise e

if __name__ == "__main__":
    compile_po_2_mo()