import csv
import os

import numpy as np


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TABLES_DIR = os.path.join(BASE_DIR, 'tables')


def to_int(val):
    return int(val.replace(',', ''))


def parse_2014():
    filename = os.path.join(TABLES_DIR, '2014_Table_3.csv')
    with open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile)
        sheet = np.array(list(reader))

    if sheet.shape != (69, 24):
        raise ValueError('Unexpected data shape.')

    # Check header row.
    headers = [
        ['Detailed Years of School', 'ALL RACES', ''],
        ['', 'Number', 'Percent'],
    ]
    if not np.all(sheet[4:6, :3] == headers):
        raise ValueError('Unexpected row headers.')

    schooling_types = sheet[6:, 0]
    schooling_numbers = sheet[6:, 1]

    if schooling_types[0] != '':
        raise ValueError('Unexpected name for "total"')

    total_people = to_int(schooling_numbers[0])
    schooling_types = schooling_types[1:]
    schooling_numbers = schooling_numbers[1:]

    # Remove blank rows.
    blank_names = np.where(schooling_types == '')
    if not np.all(schooling_numbers[blank_names] == ''):
        raise ValueError('Values are in empty rows are non-empty')

    nonblank_names = np.where(schooling_types != '')
    schooling_types = schooling_types[nonblank_names]
    schooling_numbers = schooling_numbers[nonblank_names]

    # Remove footnotes
    if not np.all(schooling_numbers[-3:] == ''):
        raise ValueError('Expected footer rows')
    schooling_numbers = schooling_numbers[:-3]
    schooling_types = schooling_types[:-3]

    # NOTE: We ignore (but could use if we chose) the categories
    #       given by schooling_types.
    # blank_numbers = np.where(schooling_numbers == '')
    # categories = schooling_types[blank_numbers]
    non_blank_numbers = np.where(schooling_numbers != '')
    schooling_numbers = schooling_numbers[non_blank_numbers]
    schooling_types = schooling_types[non_blank_numbers]

    schooling_numbers = np.vectorize(to_int)(schooling_numbers)

    result = dict(zip(schooling_types, schooling_numbers))
    if sum(result.values()) != total_people:
        raise ValueError('Total does not match observed.')
    return total_people, result


def analyze_2014():
    total_people, result = parse_2014()
