import shlex
import pytest

from argparse import ArgumentParser, Namespace
from datetime import datetime, timedelta

from src.cli import create_parser

@pytest.fixture(scope='module')
def parser() -> ArgumentParser:
    return create_parser()

def test_create_parser(parser: ArgumentParser):
    assert parser is not None
    assert parser.prog == 'dtcalc'
    assert parser.usage == '%(prog)s <command> [options]'

def test_arg_calc_parsing(parser: ArgumentParser):
    args: Namespace = parser.parse_args(shlex.split('calc 01-01-2020 5'))
    assert args.command == 'calc'
    assert args.date == datetime(2020, 1, 1)
    assert args.interval == timedelta(days=5)
    args = parser.parse_args(shlex.split('calc 01-01-2020 -5'))
    assert args.interval == timedelta(days=-5)

def test_arg_diff_parsing(parser: ArgumentParser):
    args: Namespace = parser.parse_args(shlex.split('diff 01-01-2020 10-01-2020'))
    assert args.command == 'diff'
    assert args.start == datetime(2020, 1, 1)
    assert args.end == datetime(2020, 1, 10)