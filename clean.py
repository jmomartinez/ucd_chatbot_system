import csv
import string

with open('data.csv', encoding="utf8", newline='') as file:
    reader = csv.reader(file)
    with open('cleanData.csv', 'w', newline='') as newfile:
        writer = csv.writer(newfile, delimiter=',', quotechar='"')
        for row in reader:
            for i in range(len(row)):
                row[i] = "".join(c for c in row[i] if c.isalnum() or c in string.punctuation or c == ' ')
            writer.writerow(row)
        newfile.close()
    file.close()
