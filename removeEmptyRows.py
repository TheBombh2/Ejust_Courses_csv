import csv

def remove_empty_lines(filename):
    with open(filename, 'r', newline='') as file:
        reader = csv.reader(file)
        rows = [row for row in reader if any(row)]

    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)

# Example usage
csv_filename = 'final.csv'

remove_empty_lines(csv_filename)
