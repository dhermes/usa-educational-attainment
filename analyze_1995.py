import csv
import os

import numpy as np

from common import TABLES_DIR
from common import analyze_generic
from common import to_int


def parse_1995():
    filename = os.path.join(TABLES_DIR, '1995_Table_1_By_Hand.csv')
    with open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile)
        sheet = np.array(list(reader))
    if sheet.shape != (16, 17):
        raise ValueError('Unexpected data shape.')

    row_names = sheet[1:, 0]
    column_names = sheet[0, 1:]
    cohort_data = np.vectorize(to_int)(sheet[1:, 1:])

    if column_names[0] != 'Total':
        raise ValueError('Expected total first')
    column_names = column_names[1:]
    row_totals = cohort_data[:, 0]
    cohort_data = cohort_data[:, 1:]

    if np.any(np.abs(np.sum(cohort_data, axis=1) - row_totals) > 5):
        raise ValueError('Row totals do not match observed.')

    if row_names.shape + column_names.shape != cohort_data.shape:
        raise ValueError('Expected row/col names to match data.')

    return row_names, column_names, cohort_data


def analyze_1995():
    return analyze_generic(parse_1995)
