import argparse
import textwrap
import rich_argparse

from pathlib import Path

from datetime import datetime, timedelta
from date_calc.translate.translate import _DEFAULT_LOCALES_PATH

def valid_date(s: str) -> datetime:
    try:
        return datetime.strptime(s, '%d-%m-%Y')
    except ValueError:
        msg = f"Invalid date: '{s}'. Use DD-MM-YYYY."
        raise argparse.ArgumentTypeError(msg)

def int_to_timedelta(days: str) -> timedelta:
    """Transform an integer number of days into a timedelta object."""
    try:
        return timedelta(days=int(days))
    except ValueError:
        msg = f"'Days' parameter provided({days}), cannot be converted to timedelta. Please provide a valid value."
        raise argparse.ArgumentTypeError(msg)

def _validate_path_to_locales_folder(p: str) -> Path:
    path = Path(p).resolve()
    if not path.exists() or not path.is_dir():
        raise argparse.ArgumentTypeError(f"Invalid path: '{p}'. Directory does not exist or not an accessible directory.")
    return path

def convert_path_to_locales_folder(p: str) -> Path:
    return _validate_path_to_locales_folder(p)

def create_parser() -> argparse.ArgumentParser:
    """Create and return the argument parser for the CLI."""
    parser = argparse.ArgumentParser(
        prog='dtcalc',
        usage='%(prog)s <command> [options]',
        description=textwrap.dedent("""
            Performs operations between dates and dates and day ranges.
            This package uses the datetime library, native to Python, to perform operations/calculations between dates.
        """),
        formatter_class=rich_argparse.RawDescriptionRichHelpFormatter
    )

    subparsers = parser.add_subparsers(dest='command', required=True)

    ####### Action SubParser
    calc_parser = subparsers.add_parser(
        'calc',
        usage='%(prog)s [<DATE>] [<DAYS | INTERVAL OF DAYS>]',
        description=textwrap.dedent("""
            Performs calculations with a specific date and a range of days.
            This command operates by receiving the date ([<DATE>] -> dd-mm-yyyy) and
            a positive or negative integer number of days ([<DAYS | RANGE OF DAYS>]), then performing the addition (add)
            or subtraction (sub) between the date and the number of days entered.
        """),
        help='Performs sum and difference operations between a date and a range of days.',
        formatter_class=rich_argparse.RawDescriptionRichHelpFormatter
    )
    calc_parser.set_defaults(command='calc')

    calc_parser.add_argument(
        'date',
        metavar='DATE',
        type=valid_date,
        help='Start date (DD-MM-YYYY)'
    )

    calc_parser.add_argument(
        'interval',
        metavar='DAYS',
        type=int_to_timedelta,
        help='Number of days to add or subtract.'
    )

    ####### Diff parser
    diff_parser = subparsers.add_parser(
        'diff',
        usage='%(prog)s [<START_DATE>] [<END_DATE>]',
        description=textwrap.dedent("""
            Calculates the difference in days between two dates.
            This command receives two dates ([<START_DATE>] and [<END_DATE>]) in the format dd-mm-yyyy,
            and returns the difference in days between them.
            It reports errors if the dates are the same or the initial date is less than the final date.
        """),
        help='Calculates the difference between two dates.',
        formatter_class=rich_argparse.RawDescriptionRichHelpFormatter
    )
    diff_parser.set_defaults(command='diff')

    diff_parser.add_argument(
        'start',
        type=valid_date,
        help='Start date (DD-MM-YYYY)'
    )

    diff_parser.add_argument(
        'end',
        type=valid_date,
        help='End date (DD-MM-YYYY)'
    )

    ####### Compile .po -> .mo parser
    compile_parser = subparsers.add_parser(
        'compile',
        usage='%(prog)s compile [<PATH_TO_LOCALES_FOLDER>]',
        description=textwrap.dedent("""
            Compiles .po files to .mo files for localization.
            This command searches for all .po files in the locales directory and compiles them into .mo files.
        """),
        help='Compiles .po files to .mo files for localization.',
        formatter_class=rich_argparse.RawDescriptionRichHelpFormatter
    )
    compile_parser.set_defaults(command='compile')
    compile_parser.add_argument(
        '--path',
        type=lambda p: convert_path_to_locales_folder(p), 
        default= _DEFAULT_LOCALES_PATH,
        help=f'Path to the locales folder (default: {_DEFAULT_LOCALES_PATH.as_posix()})'
    )

    ####### Init/interative parser
    iter_parser = subparsers.add_parser(
        'iter',
        aliases=['iterate', 'iterative', 'init', 'initialize', 'ini'],
        usage='%(prog)s init',
        description=textwrap.dedent("""
            Enters interactive mode.
            An infinite loop that accepts an indeterminate number of inputs, 
            eliminating the need to run the application multiple times from the command line.
        """),
        help="Enters interactive mode.",
        formatter_class=rich_argparse.RawDescriptionRichHelpFormatter
    )
    iter_parser.set_defaults(command='iter')

    return parser