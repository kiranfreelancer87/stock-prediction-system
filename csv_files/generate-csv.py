import csv
import json

tabs_data = json.loads(open('tabs_data.json').read())

for td in tabs_data:
    with open(f'../data/{td['name']}.json', 'r') as f:
        data = json.loads(f.read())['data']
        columns = td['columns']
    csv_data = []
    for item in data:
        row = item["d"]
        row[5] = ",".join(row[5])
        csv_data.append(row)

    output_file = f"{td['name']}.csv"

    # Write to CSV
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(columns)  # Write the header
        writer.writerows(csv_data)  # Write the data

    print(f"Data has been written to {output_file}")
