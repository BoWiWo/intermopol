import csv
import numpy as np

# Read tables and load into variables
file_A2 = open('tables\\A-2.csv')
file_A3 = open('tables\\A-3.csv')

csvreader_A2 = csv.reader(file_A2)
csvreader_A3 = csv.reader(file_A3)

header_A2 = next(csvreader_A2)
header_A3 = next(csvreader_A3)

header_A2.pop()
header_A3.pop()

rows_A2 = []
rows_A3 = []

for row in csvreader_A2:
    row.pop() # Remove last element from list, which is a repeat of pres/temp (whichever comes first)
    row = [float(i) for i in row]
    rows_A2.append(row)

for row in csvreader_A3:
    row.pop() # Remove last element from list, which is a repeat of pres/temp (whichever comes first)
    row[0], row[1] = row[1], row[0] # Swap first 2 columns to match pres/temp with table A-2
    row = [float(i) for i in row]
    rows_A3.append(row)

file_A2.close()
file_A3.close()

# Combined table for A-2 and A-3
A_23 = rows_A2

for row in rows_A3:
    A_23.append(row)

# Sort combined list by first element in row
A_23.sort(key = lambda x: x[0])

A_23 = np.array(A_23)

# Returns a row from combined table A_23 interpolated (if needed) to the value of 1 chosen variable
def interpolateRow(inVar, inVal, header, table):
    inVarCol = header.index(inVar)

    outRow = np.empty(len(table[0, :]))

    for i in range(len(table[0, :])):
        outRow[i] = np.interp(inVal, table[:, inVarCol], table[:, i], left=-1, right=-1)

    return outRow

print(np.array(header_A2))
print(interpolateRow('h_f', 341.1111111, header_A2, A_23))