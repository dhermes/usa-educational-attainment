import csv
import os

import numpy as np

from common import TABLES_DIR
from common import to_int


def _parse_2010_or_2014(sheet, num_col, num_col_name,
                        total_name, num_footers):
    # Check header row.
    headers = [
        ['Detailed Years of School', num_col_name],
        ['', 'Number'],
    ]
    type_col = 0
    if not np.all(sheet[4:6, [type_col, num_col]] == headers):
        raise ValueError('Unexpected row headers.')

    schooling_types = sheet[6:, type_col]
    schooling_numbers = sheet[6:, num_col]

    if schooling_types[0] != total_name:
        raise ValueError('Unexpected name for "total"')

    total_people = to_int(schooling_numbers[0])
    schooling_types = schooling_types[1:]
    schooling_numbers = schooling_numbers[1:]

    # Remove footnotes, intentionally leave a blank row.
    if not np.all(schooling_numbers[-num_footers:] == ''):
        raise ValueError('Expected footer rows')
    schooling_numbers = schooling_numbers[:-num_footers]
    schooling_types = schooling_types[:-num_footers]

    result = []

    separator_rows, = np.where(schooling_types == '')
    num_sections = len(separator_rows) - 1
    for section in xrange(num_sections):
        begin_index = separator_rows[section] + 1
        end_index = separator_rows[section + 1] - 1

        # Determine if the section has a category.
        category = None
        if schooling_numbers[begin_index] == '':
            category = schooling_types[begin_index]
            begin_index += 1

        for index in xrange(begin_index, end_index + 1):
            result.append((
                schooling_types[index],
                category,
                to_int(schooling_numbers[index]),
            ))

    if np.abs(sum([val[-1] for val in result]) - total_people) > 5:
        raise ValueError('Total does not match observed.')
    return total_people, result


def load_2010():
    filename = os.path.join(TABLES_DIR, '2010_Table_3.csv')
    with open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile)
        sheet = np.array(list(reader))
    if sheet.shape != (70, 23):
        raise ValueError('Unexpected data shape.')
    return sheet


def load_2014():
    filename = os.path.join(TABLES_DIR, '2014_Table_3.csv')
    with open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile)
        sheet = np.array(list(reader))
    if sheet.shape != (69, 24):
        raise ValueError('Unexpected data shape.')

    return sheet


def _analyze_2010_or_2014(sheet, year, total_name='', num_footers=4):
    options = [
        (1, 'ALL RACES'),
        (7, '25 TO 34  YEARS OLD'),
        (9, '35 TO 54  YEARS OLD'),
        (11, '55 YEARS OLD AND OVER'),
    ]
    result = []
    for num_col, num_col_name in options:
        pretty_name = ' '.join(num_col_name.split())
        if pretty_name == 'ALL RACES':
            pretty_name = 'ALL AGES'
        print '%d; %25s:' % (year, pretty_name),
        total_people, result = _parse_2010_or_2014(
            sheet, num_col, num_col_name, total_name=total_name,
            num_footers=num_footers)

        # Assumes the data is in order of educational attainment from
        # least (i.e. Less than 1st grade) to most (i.e. PhD)

        # We expect exactly one match for each type.
        begin_of_hs, = [row for row, value in enumerate(result)
                        if value[0] == 'High school diploma']
        begin_of_bachelors, = [row for row, value in enumerate(result)
                               if value[0] == 'Bachelors degree only']

        hs_tot = sum([value[-1] for value in result[begin_of_hs:]])
        bachelors_tot = sum([
            value[-1] for value in result[begin_of_bachelors:]])

        total_people = float(total_people)
        hs_percent = hs_tot / total_people
        bachelors_percent = bachelors_tot / total_people

        print 'HS -> %4.1f and BA/BS -> %4.1f' % (
            100 * hs_percent, 100 * bachelors_percent)
        result.append((num_col_name, hs_percent, bachelors_percent))

    return result


def analyze_2010():
    sheet = load_2010()
    return _analyze_2010_or_2014(sheet, 2010, total_name='Total',
                                 num_footers=5)


def analyze_2014():
    sheet = load_2014()
    return _analyze_2010_or_2014(sheet, 2014)
