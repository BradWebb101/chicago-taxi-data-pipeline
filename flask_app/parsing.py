import io
import csv

def to_csv(data):
    output = io.StringIO()
    writer = csv.writer(output)
    for row in data:
        writer.writerow(row)
    return output.getvalue()






