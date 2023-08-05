import argparse
from os.path import exists as path_exists
from aqua_cli.cli import check_intake
from aqua_cli.cli.arguments import (setup, change_amount, get, about)
from aqua_cli.utils.files_location import db_file

def main():
    args = setup_args()
    if not(path_exists(db_file)):
        print('ERROR: setup the application with --setup <age> <weight>, then try to run the application again.')
        return

    implement_arguments(args)
    check_intake.check_intake()

def setup_args():
    parser = argparse.ArgumentParser(
        prog='aqua',
        description='A simple water tracking CLI. Track your water intake, live better :)'
    )

    parser.add_argument(
        '--setup',
        '-s',
        nargs=2,
        type=int,
        metavar=('<age>', '<weight>'),
        help='setup the application'
    )

    parser.add_argument(
        '--add',
        '-a',
        nargs=1,
        type=int,
        metavar='<amount>',
        help='add the specified amount'
    )

    parser.add_argument(
        '--remove',
        '-r',
        nargs=1,
        type=int,
        metavar='<amount>',
        help='remove the specified amount'
    )

    parser.add_argument(
        '--get',
        '-g',
        action='store_true',
        help='get your intake'
    )

    parser.add_argument(
        '--get-all',
        '-l',
        action='store_true',
        help='show your intake history'
    )

    parser.add_argument(
        '--about',
        '-t',
        action='store_true',
        help='check updates and show the application version'
    )

    args = parser.parse_args()
    return args

def implement_arguments(args):
    if args.setup:
        setup.setup(age=args.setup[0], weight=args.setup[1])
        return
    
    if args.add:
        change_amount.change_amount(target='add', amount=args.add[0])
    elif args.remove:
        change_amount.change_amount(target='remove', amount=args.remove[0])
    elif args.get:
        get.get(target='get')
    elif args.get_all:
        get.get(target='get-all')
    elif args.about:
        about.about()

if __name__ == '__main__':
    main()