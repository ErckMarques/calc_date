import polib
from pathlib import Path
from typing import cast, TypeAlias

StrOrPathPOFile: TypeAlias = Path | str

def _compile_po_2_mo(po_file: StrOrPathPOFile, domain: str = 'app'):
    if isinstance(po_file, str):
        file = Path(po_file)

    file = cast(Path, po_file)
    if isinstance(file, Path):
        if not file.is_file() or not file.exists():
            raise IsADirectoryError("Passed argument is either not a file or does not exist.")
    
    mo_file = file.as_posix().replace(".po", ".mo")
    nfile = polib.pofile(file)
    nfile.save_as_mofile(mo_file)


if __name__ == "__main__":
    # C:\Users\PC\python_projects\calc_dates\src\date_calc\locale
    LOCALE_DIR = Path(__file__).parents[1].joinpath('locale')

    # C:\Users\PC\python_projects\calc_dates\src\date_calc\locale\pt
    for dir in LOCALE_DIR.iterdir():
        # C:\Users\PC\python_projects\calc_dates\src\date_calc\locale\pt\LC_MESSAGENS\app.po
        _compile_po_2_mo(dir.joinpath('LC_MESSAGENS', 'app.po'))