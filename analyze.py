#!/usr/bin/env python

import argparse

from analyze_1995 import analyze_1995
from analyze_2000 import analyze_2000
from analyze_2005 import analyze_2005
from analyze_2010_and_2014 import analyze_2010
from analyze_2010_and_2014 import analyze_2014


def text_only(year_choices, args):
    method = year_choices[args.year]
    for data in method():
        data.display(args.year)


def add_plots(ax_hs, ax_bachelors, name, value_dict, all_years):
    # Intentionally delay imports to speed up other cases.
    import numpy as np
    years = []
    hs_values = []
    bachelors_values = []
    for year, cohort_data in value_dict.iteritems():
        all_years.add(year)  # Assume `all_years` is a set()
        years.append(year)
        hs_values.append(cohort_data.hs_percent)
        bachelors_values.append(cohort_data.bachelors_percent)

    years = np.array(years)
    hs_values = np.array(hs_values)
    bachelors_values = np.array(bachelors_values)

    to_sort = np.argsort(years)
    years = years[to_sort]
    hs_values = hs_values[to_sort]
    bachelors_values = bachelors_values[to_sort]

    ax_hs.plot(years, hs_values, label=name, marker='o')
    ax_bachelors.plot(years, bachelors_values,
                      label=name, marker='o')


def make_plot(year_choices):
    # Intentionally delay imports to speed up other cases.
    print 'Importing plotting utils...'
    from matplotlib import rcParams
    import matplotlib.pyplot as plt
    import seaborn
    seaborn.set_palette('husl')
    print 'Plotting imports complete'

    print 'Running analysis for each year...'
    by_name = {}
    for year, method in year_choices.iteritems():
        print year,
        curr_results = method()
        for data in curr_results:
            named_data = by_name.setdefault(data.name, {})
            if year in named_data:
                raise KeyError('Year %d already accounted for in '
                               'name %s' % (year, data.name))
            named_data[year] = data
    print '\nAnalysis complete'

    rows, cols = 1, 2
    width, height = rcParams['figure.figsize']
    fig, (ax_hs, ax_bachelors) = plt.subplots(
        rows, cols, figsize=(1.8 * width, height))

    all_years = set()
    for name in sorted(by_name.keys()):
        value_dict = by_name[name]
        add_plots(ax_hs, ax_bachelors, name, value_dict, all_years)

    all_years = sorted(all_years)
    ax_hs.set_xticks(all_years)
    ax_hs.set_xticklabels(map(str, all_years))
    ax_bachelors.set_xticks(all_years)
    ax_bachelors.set_xticklabels(map(str, all_years))

    ax_hs.set_xlabel('Year of Survey')
    ax_hs.set_ylabel('% Completed')
    ax_bachelors.set_xlabel('Year of Survey')

    ax_hs.legend(loc='lower right')
    ax_bachelors.legend(loc='lower right')

    ax_hs.set_title('High School', fontsize=20)
    ax_bachelors.set_title('Bachelors\'', fontsize=20)

    plt.show()


def main():
    year_choices = {
        1995: analyze_1995,
        2000: analyze_2000,
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

    plot_parser = subparsers.add_parser(
        'plot', description='Make plots of numbers over times')

    args = parser.parse_args()
    if args.chosen_parser == 'text':
        text_only(year_choices, args)
    elif args.chosen_parser == 'plot':
        make_plot(year_choices)


if __name__ == '__main__':
    main()
