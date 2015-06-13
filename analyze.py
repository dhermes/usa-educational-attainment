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

    # Remove footnotes, intentionally leave a blank row.
    if not np.all(schooling_numbers[-4:] == ''):
        raise ValueError('Expected footer rows')
    schooling_numbers = schooling_numbers[:-4]
    schooling_types = schooling_types[:-4]

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

    if sum([val[-1] for val in result]) != total_people:
        raise ValueError('Total does not match observed.')
    return total_people, result


def analyze_2014():
    total_people, result = parse_2014()

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

    print '2014: HS -> %4.1f and BA/BS -> %4.1f' % (
        100 * hs_percent, 100 * bachelors_percent)
    return hs_percent, bachelors_percent
