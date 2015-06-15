#!/usr/bin/env python

import argparse

from analyze_2010_and_2014 import analyze_2010
from analyze_2010_and_2014 import analyze_2014


def main():
    year_choices = {
        2010: analyze_2010,
        2014: analyze_2014,
    }
    parser = argparse.ArgumentParser(
        description='Run analysis on educational attainment census data')
    parser.add_argument('--year', dest='year', type=int,
                        choices=tuple(year_choices.keys()), default=2014,
                        help='Year of data to analyze.')
    args = parser.parse_args()
    method = year_choices[args.year]
    method()


if __name__ == '__main__':
    main()
