import csv
import numpy as np
from pathlib import Path

# Loads and returns tables A2 and A3, combines them and creates a overall header and table
def getTablesSaturatedWater():
    # Read tables and load into variables
    file_A2 = open(Path('tables/A-2.csv'))
    file_A3 = open(Path('tables/A-3.csv'))

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
    return header_A2, A_23

def getTablesSuperheatedVapour():
    # Read tables and load into variables
    file_A4 = open(Path('tables/A-4.csv'))

    csvreader = csv.reader(file_A4)

    header = next(csvreader)

    rows = []

    for row in csvreader:
        row = [float(i) for i in row]
        rows.append(row)

    file_A4.close()

    return header, np.array(rows)

# Returns a row from combined table A_23 interpolated (if needed) to the value of 1 chosen variable
def interpolateRow(inVar, inVal, header, table):
    inVarCol = header.index(inVar)

    outRow = np.empty(len(table[0, :]))

    for i in range(len(table[0, :])):
        outRow[i] = np.interp(inVal, table[:, inVarCol], table[:, i], left=-1, right=-1)

    return outRow

headerSaturatedWater, tableSaturatedWater = getTablesSaturatedWater()

print(headerSaturatedWater)
print(interpolateRow('h_f', 341.1111111, headerSaturatedWater, tableSaturatedWater))

# Returns a table for a given pressure
def interpolateTable(pressure, table):
    # If the pressure is an exact match for a table (at least one pressure match exists in the table):
    if np.any(np.where(table[:,0] == pressure)):
        return table[np.where(table[:,0] == pressure),:]

    # If the pressure is within the range of the tables find closest pressure below given value
    elif table[0,0] < pressure < table[-1,0]:
        # Contains all rows where pressure is less than the input
        lowerrows = table[np.where(pressure - table[:, 0] > 0)]
        higherrows = table[np.where(table[:, 0] - pressure > 0)]

        # Takes the rows from lowerrows where pressure is closest to the input pressure
        closest_below = table[np.where(table[:,0] == lowerrows[:,0].max())]
        closest_above = table[np.where(table[:,0] == higherrows[:,0].min())]

        return closest_below + (closest_above - closest_below) * (pressure - closest_below[0,0]) / (closest_above[0,0] - closest_below[0,0])

headerSuperheatedVapour, tableSuperheatedVapour = getTablesSuperheatedVapour()

print(headerSuperheatedVapour)
print(interpolateTable(table=tableSuperheatedVapour, pressure=11.2))