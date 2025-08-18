from datetime import datetime

from .cli import create_parser
from .runner import DefaultRunner


def main():
    parser = create_parser()
    args = parser.parse_args()
    runner = DefaultRunner()

    if args.command == 'calc':
        
        result = getattr(runner, 'sum')(args.date, args.interval)

        print(f"Resulting date: {result}")

    elif args.command == 'diff':
        days = runner.diff(args.start, args.end)
        print(f"Difference in days: {days}")

    elif args.command in ['iter', 'initialize', 'init', 'iterative', 'ini']:
        runner.enter_interactive_mode()
    elif args.command in ['gui', 'interface', 'ui']:
        runner.launch_gui()
