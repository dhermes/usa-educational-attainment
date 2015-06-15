#!/usr/bin/env python

import argparse

from analyze_2005 import analyze_2005
from analyze_2010_and_2014 import analyze_2010
from analyze_2010_and_2014 import analyze_2014


def main():
    year_choices = {
        2005: analyze_2005,
        2010: analyze_2010,
        2014: analyze_2014,
    }
    parser = argparse.ArgumentParser(
        description='Run analysis on educational attainment census data')
    subparsers = parser.add_subparsers(help='Subcommands to choose',
                                       dest='chosen_parser')

    text_display_parser = subparsers.add_parser(
        'text', description='View numbers as text for a chosen year')
    text_display_parser.add_argument(
        '--year', dest='year', type=int,
        choices=tuple(year_choices.keys()), required=True,
        help='Year of data to analyze.')

    args = parser.parse_args()
    if args.chosen_parser == 'text':
        method = year_choices[args.year]
        for data in method():
            data.display(args.year)


if __name__ == '__main__':
    main()
