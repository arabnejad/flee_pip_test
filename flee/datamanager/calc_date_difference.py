from flee import flee
from flee.datamanager import handle_refugee_data
from flee.datamanager import DataTable
import numpy as np
import flee.postprocessing.analysis as a
import sys

"""
calc_date_difference.py
Calculates the number of days between two dates.

Usage python3 calc_date_difference.py <YYYY-MM-DD earlier date> <YYYY-MM-DD later date>

"""


if __name__ == "__main__":
    print(DataTable.subtract_dates(sys.argv[2], sys.argv[1]))
