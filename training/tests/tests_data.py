import csv

"""
 pytest tests/tests_data.py --datafile="wrong_data"
 pytest tests/tests_data.py --datafile="SalaryData1"
"""

def test_empty_fields(datafile):
    no_blank_cells = True
    filename = "data/%s.csv" % datafile
    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        for row in csvreader:
            print(row)
            if row[0] in (None, ""):
                no_blank_cells = False
    assert no_blank_cells

