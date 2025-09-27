import argparse
import csv
import sys
from datetime import datetime

def parse_args():
    parser = argparse.ArgumentParser(description='Process complaint data by borough and date range.')
    parser.add_argument('-i', '--input', required=True, help='Path to the input CSV file')
    parser.add_argument('-s', '--start_date', required=True, help='Start date in YYYY-MM-DD format')
    parser.add_argument('-e', '--end_date', required=True, help='End date in YYYY-MM-DD format')
    parser.add_argument('-o', '--output', help='Path to the output CSV file (optional)')
    return parser.parse_args()

def main():

    print("Starting borough complaints processing...")
    
    args = parse_args()
    start_date = datetime.strptime(args.start_date, '%Y-%m-%d').date()
    end_date = datetime.strptime(args.end_date, '%Y-%m-%d').date()

    with open(args.input, 'r') as input_file:
        reader = csv.DictReader(input_file)
        data = []
        for row in reader:
            try:
                created_date = datetime.strptime(row['created_date'], '%Y-%m-%dT%H:%M:%S.%f').date()
            except ValueError:
                continue
            if start_date <= created_date <= end_date:
                data.append(row)

    print(f"Total records within date range: {len(data)}")

    boroughs = set()
    complaint_types = set()
    for row in data:
        if row.get('borough'):
            boroughs.add(row['borough'].strip())
        if row.get('complaint_type'):
            complaint_types.add(row['complaint_type'].strip())

    output_data = [
        ['complaint_type', 'borough', 'count']
    ]

    for borough in sorted(boroughs):
        for complaint_type in sorted(complaint_types):
            count = sum(1 for row in data
                        if row.get('borough') and row.get('complaint_type') and 
                        row['borough'].strip() == borough and
                        row['complaint_type'].strip() == complaint_type)
            if count > 0:
                output_data.append([complaint_type, borough, count])

    if args.output:
        with open(args.output, 'w', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerows(output_data)
    else:
        writer = csv.writer(sys.stdout)
        writer.writerows(output_data)

if __name__ == '__main__':
    main()
