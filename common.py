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
