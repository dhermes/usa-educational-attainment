import os

import numpy as np

from common import CohortData
from common import TABLES_DIR
from common import _get_all_ages
from common import _get_25_to_34
from common import _get_35_to_54
from common import _get_55_and_older
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


def analyze_2005():
    sheet = load_2005()
    row_names, column_names, cohort_data = parse_2005(sheet)

    result = []
    # ALL AGES
    data = _get_all_ages(row_names, column_names, cohort_data)
    result.append(data)

    # 25-34
    data = _get_25_to_34(row_names, column_names, cohort_data)
    result.append(data)

    # 35-54
    data = _get_35_to_54(row_names, column_names, cohort_data)
    result.append(data)

    # 55 YEARS OLD AND OVER
    data = _get_55_and_older(row_names, column_names, cohort_data)
    result.append(data)

    return result
