import csv
import os

import numpy as np


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TABLES_DIR = os.path.join(BASE_DIR, 'tables')


class CohortData(object):

    def __init__(self, name, total, hs_total, bachelors_total):
        self.name = name
        self.total = total
        self.hs_total = hs_total
        self.bachelors_total = bachelors_total

    @property
    def hs_percent(self):
        return (self.hs_total * 100.0) / self.total

    @property
    def bachelors_percent(self):
        return (self.bachelors_total * 100.0) / self.total

    def display(self, year):
        print '%d; %25s: HS -> %4.1f and BA/BS -> %4.1f' % (
            year, self.name, self.hs_percent, self.bachelors_percent)


def to_int(val):
    # See footnote (in 2005, 2010, and 2014):
    # A dash (-) represents zero or rounds to zero.
    if val.strip() == '-':
        return 0
    return int(val.replace(',', ''))


def load_non_rectangular(filename):
    """Loads a CSV with an unequal number of columns per row."""
    with open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile)
        sheet = list(reader)

    # Each entry in sheet is a list, which is mutable.
    num_cols = max(map(len, sheet))
    for row_val in sheet:
        row_deficit = num_cols - len(row_val)
        row_val.extend([''] * row_deficit)

    return np.array(sheet)


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
    return CohortData(None, actual_total, min_hs_total,
                      min_bachelors_total)


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
    data = _get_total(curr_rows, curr_row_names, row_names,
                      column_names, cohort_data)
    data.name = 'ALL AGES'
    return data


def _get_25_to_34(row_names, column_names, cohort_data):
    curr_rows = [4, 5]
    curr_row_names = ['25 to 29 years', '30 to 34 years']
    data = _get_total(curr_rows, curr_row_names, row_names,
                      column_names, cohort_data)
    data.name = '25 TO 34 YEARS OLD'
    return data


def _get_35_to_54(row_names, column_names, cohort_data):
    curr_rows = [6, 7, 8, 9]
    curr_row_names = [
        '35 to 39 years',
        '40 to 44 years',
        '45 to 49 years',
        '50 to 54 years',
    ]
    data = _get_total(curr_rows, curr_row_names, row_names,
                      column_names, cohort_data)
    data.name = '35 TO 54 YEARS OLD'
    return data


def _get_55_and_older(row_names, column_names, cohort_data):
    curr_rows = [10, 11, 12, 13, 14]
    curr_row_names = [
        '55 to 59 years',
        '60 to 64 years',
        '65 to 69 years',
        '70 to 74 years',
        '75 years and over',
    ]
    data = _get_total(curr_rows, curr_row_names, row_names,
                      column_names, cohort_data)
    data.name = '55 YEARS OLD AND OVER'
    return data
