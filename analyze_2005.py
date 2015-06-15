import os

import numpy as np

from common import TABLES_DIR
from common import load_non_rectangular
from common import to_int


def load_2005():
    filename = os.path.join(TABLES_DIR, '2005_Table_1.csv')
    sheet = load_non_rectangular(filename)
    if sheet.shape != (100, 18):
        raise ValueError('Unexpected data shape.')
    return sheet


def parse_2005(sheet):
    # Check header row.
    headers = [
        ['All Races\nand Both Sexes', 'Educational Attainment'],
        ['', 'Total'],
    ]
    if not np.all(sheet[4:6, 0:2] == headers):
        raise ValueError('Unexpected row headers.')
    if sheet[27, 0] != 'Footnotes:':
        raise ValueError('Expected footnotes to begin at 27.')

    data_rows = sheet[6:27, :]
    # Make sure the last column is bogus.
    if not (np.all(sheet[5, -2:] == ['Doctoral degree', '']) and
            np.all(data_rows[:, -1] == '')):
        raise ValueError('Expected bogus column.')
    data_rows = data_rows[:, :-1]
    column_names = sheet[5, 2:-1]

    row_names = data_rows[:, 0]
    row_totals = np.vectorize(to_int)(data_rows[:, 1])
    cohort_data = data_rows[:, 2:]

    if row_names.shape + column_names.shape != cohort_data.shape:
        raise ValueError('Expected row/col names to match data.')
    if np.any(cohort_data == ''):
        raise ValueError('Expected to empty cells in data.')
    # See footnote:
    #    A dash (-) represents zero or rounds to zero.
    cohort_data = np.vectorize(to_int)(cohort_data)

    if np.any(np.abs(np.sum(cohort_data, axis=1) - row_totals) > 5):
        raise ValueError('Row totals do not match observed.')

    return row_names, column_names, cohort_data


def _get_total(curr_rows, curr_row_names, row_names,
               column_names, cohort_data):
    if np.any(row_names[curr_rows] != curr_row_names):
        raise ValueError('Unexpected header rows')
    curr_cohort = cohort_data[curr_rows]
    combined_data = np.sum(curr_cohort, axis=0)

    min_hs = 7
    if column_names[min_hs] != 'High school graduate':
        raise ValueError('Unexpected min HS')
    min_hs_total = np.sum(combined_data[min_hs:])

    min_bachelors = 11
    if column_names[min_bachelors] != 'Bachelor\'s degree':
        raise ValueError('Unexpected min BA/BS')
    min_bachelors_total = np.sum(combined_data[min_bachelors:])

    actual_total = np.sum(combined_data)
    return min_hs_total, min_bachelors_total, actual_total


def _get_all_ages(row_names, column_names, cohort_data):
    curr_rows = range(4, 14 + 1)
    curr_row_names = [
        '25 to 29 years',
        '30 to 34 years',
        '35 to 39 years',
        '40 to 44 years',
        '45 to 49 years',
        '50 to 54 years',
        '55 to 59 years',
        '60 to 64 years',
        '65 to 69 years',
        '70 to 74 years',
        '75 years and over',
    ]
    return _get_total(curr_rows, curr_row_names, row_names,
                      column_names, cohort_data)


def _get_25_to_34(row_names, column_names, cohort_data):
    curr_rows = [4, 5]
    curr_row_names = ['25 to 29 years', '30 to 34 years']
    return _get_total(curr_rows, curr_row_names, row_names,
                      column_names, cohort_data)


def _get_35_to_54(row_names, column_names, cohort_data):
    curr_rows = [6, 7, 8, 9]
    curr_row_names = [
        '35 to 39 years',
        '40 to 44 years',
        '45 to 49 years',
        '50 to 54 years',
    ]
    return _get_total(curr_rows, curr_row_names, row_names,
                      column_names, cohort_data)


def _get_55_and_older(row_names, column_names, cohort_data):
    curr_rows = [10, 11, 12, 13, 14]
    curr_row_names = [
        '55 to 59 years',
        '60 to 64 years',
        '65 to 69 years',
        '70 to 74 years',
        '75 years and over',
    ]
    return _get_total(curr_rows, curr_row_names, row_names,
                      column_names, cohort_data)


def display_values(hs_total, bachelors_total, actual_total,
                   year, pretty_name):
    hs_percent = (hs_total * 100.0) / actual_total
    bachelors_percent = (bachelors_total * 100.0) / actual_total
    print '%d; %25s: HS -> %4.1f and BA/BS -> %4.1f' % (
        year, pretty_name, hs_percent, bachelors_percent)


def analyze_2005():
    sheet = load_2005()
    row_names, column_names, cohort_data = parse_2005(sheet)

    # ALL AGES
    args = (_get_all_ages(row_names, column_names, cohort_data) +
            (2005, 'ALL AGES'))
    display_values(*args)

    # 25-34
    args = (_get_25_to_34(row_names, column_names, cohort_data) +
            (2005, '25 TO 34 YEARS OLD'))
    display_values(*args)

    # 35-54
    args = (_get_35_to_54(row_names, column_names, cohort_data) +
            (2005, '35 TO 54 YEARS OLD'))
    display_values(*args)

    # 55 YEARS OLD AND OVER
    args = (_get_55_and_older(row_names, column_names, cohort_data) +
            (2005, '55 YEARS OLD AND OVER'))
    display_values(*args)
