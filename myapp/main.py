from wbiz import get_wbiz_pages_by_category
import csv

wbiz_pages = get_wbiz_pages_by_category()
filepath =""
csvfile = open(filepath, "w", newline="")
csvwriter = csv.writer(csvfile)

for page in wbiz_pages:
    for data in page:
        csvwriter.writerow(data)

csvfile.close()