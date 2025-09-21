"""
This module provides a function for compiling the '.mo' binary files, used by gettext, through the "polib" lib.
"""
import logging
import polib
from pathlib import Path
from typing import cast, TypeAlias, Optional

from date_calc.translate.raises import IsNotPOFileError

StrOrPath: TypeAlias = Path | str

def _validate_pofile_path(p: Path) -> Path:
    """Validates whether the pathlib.Path object represents a valid .po file."""

    if not p.exists() or not p.is_file():
        msg = f"Invalid path: '{p}'. File does not exist or is not an accessible file."
        raise FileNotFoundError(msg)

    if p.suffix != '.po':
        msg = f"The passed file is not of type '.po', \nPath: {p.as_posix()}"
        raise IsNotPOFileError(msg)

    return p

def _compile_po_2_mo(po_file: Path):
    """
    This function takes a pathlib.Path object,
    representing the path of the '.po' file and saves it in the same folder or path.

    Args:
        po_file (Path): file path to the '.po' file
    """   
    mo_file: str = po_file.with_suffix(".mo").as_posix()
    nfile: polib.POFile = polib.pofile(po_file)
    nfile.save_as_mofile(mo_file)

def compile_po_2_mo(locale_path: StrOrPath):
    """
    This function takes a string or a pathlib.Path object,
    representing the path of the '.po' file and saves it in the same folder or path.

    Args:
        locale_path (StrOrPath): Path to the 'locale' folder containing the .po files
    """
    for po_file in Path(locale_path).rglob('*.po'):
        try:
            file: Path = _validate_pofile_path(cast(Path, po_file) if isinstance(po_file, str) else Path(po_file))
            _compile_po_2_mo(file)
            logging.info(f"Successfully compiled '{file.as_posix()}' to '{file.with_suffix('.mo').as_posix()}'")
        except (FileNotFoundError, IsNotPOFileError) as e:
            logging.error(f"Error: {e}")
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
    

if __name__ == "__main__":
    locale_path: Path = Path(input('Enter the path to the locale folder: ')).expanduser().resolve()
    domain: Optional[str] = input('Enter the domain (press Enter to use "messages"): ') or "messages"

    compile_po_2_mo(locale_path)