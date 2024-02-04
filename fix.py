import csv
import re

#This script was made to fix some rows that wasn't properly written

pattern = re.compile(r'(?P<code>\w+).-(?P<title>.*?)\s\((?P<credit_hours>\d+)\sCH\)')

with open('final.csv', 'r') as file:
    reader = csv.reader(file)
    rows = list(reader)

for row in rows:
    if row[2] == "None":
        match = pattern.match(row[1])

        print(row[1])
        # Export Information
        Ccode = match.group('code') if match is not None else None
        Ctile = match.group('title') if match is not None else None
        Cch = match.group('credit_hours') if match is not None else None
        if Ccode is not None and Ctile is not None and Cch is not None:
            row[1] = Ccode
            row[2] = Ctile
            row[3] = Cch
            print(Ccode, Ctile, Cch)

# Remove rows with all values as None
rows = [row for row in rows if any(val != "None" for val in row)]

with open('final.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(rows)
