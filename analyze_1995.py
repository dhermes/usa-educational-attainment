import csv
import os

import numpy as np

from common import CohortData
from common import TABLES_DIR
from common import _get_all_ages
from common import _get_25_to_34
from common import _get_35_to_54
from common import _get_55_and_older
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
    row_names, column_names, cohort_data = parse_1995()

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
