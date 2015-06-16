import cStringIO
import csv
import os

import numpy as np

from common import TABLES_DIR
from common import analyze_generic
from common import to_int


def load_csv_pipe_delimiter(lines):
    mock_file = cStringIO.StringIO()
    mock_file.write('\n'.join(lines))
    mock_file.seek(0)
    reader = csv.reader(mock_file, delimiter='|')
    return np.array(list(reader))


def join_separated_phrase(phrase_parts):
    actual_parts = []
    hyphen_found = False
    for part in phrase_parts:
        to_add = part.strip()
        if not hyphen_found:
            to_add = ' ' + to_add

        # Intentionally using `part`, not `to_add` here.
        if part.endswith('-'):
            hyphen_found = True
            to_add = to_add[:-1]
        else:
            hyphen_found = False

        actual_parts.append(to_add)
    return ''.join(actual_parts).strip()


def parse_2000():
    filename = os.path.join(TABLES_DIR, '2000_Table_1.txt')
    with open(filename, 'rU') as fh:
        file_lines = fh.read().split('\n')

    begin_line = 16
    end_line = 76
    if not (set(file_lines[begin_line]) == set('-') and
            file_lines[begin_line] == file_lines[end_line]):
        raise ValueError('')

    # Get all the lines in between the '---' lines.
    table = file_lines[begin_line + 1:end_line]
    # Remove blank lines, should be every other.
    if set(table[::2]) != set(['']):
        raise ValueError('Expected blank lines between.')

    table = table[1::2]
    if not (table[0].startswith('|All Races') and
            table[1].startswith('|AND Both Sexes')):
        raise ValueError('Wrong table.')

    header_sep_line = 7
    if set(table[header_sep_line]) != set('+-|'):
        raise ValueError('Separator not where expected.')

    # Headers start after table[1]
    header_lines = table[2:header_sep_line]
    column_names = load_csv_pipe_delimiter(header_lines)
    column_names = np.array([join_separated_phrase(row)
                             for row in column_names.T])

    just_data = table[header_sep_line + 1:]
    sheet = load_csv_pipe_delimiter(just_data)

    if sheet.shape != (21, 19):
        raise ValueError('Expected 2D data.')

    if not np.all(sheet[:, [0, -1]] == ''):
        raise ValueError('Bad first and last column')

    row_names = np.array([val.strip() for val in sheet[:, 1]])
    cohort_data = np.vectorize(to_int)(sheet[:, 2:-1])
    column_names = column_names[2:-1]

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


def analyze_2000():
    return analyze_generic(parse_2000)
