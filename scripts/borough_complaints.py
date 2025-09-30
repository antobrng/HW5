import argparse
import csv
import sys
from datetime import datetime

def parse_args():
    parser = argparse.ArgumentParser(
        description='Process 311 complaint data by borough and date range.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        '-i', '--input',
        required=True,
        help='Path to the input CSV file'
    )
    parser.add_argument(
        '-s', '--start_date',
        required=True,
        help='Start date in MM/DD/YYYY format'
    )
    parser.add_argument(
        '-e', '--end_date',
        required=True,
        help='End date in MM/DD/YYYY format'
    )
    parser.add_argument(
        '-o', '--output',
        help='Path to the output CSV file (optional; if not provided, prints to stdout)'
    )
    return parser.parse_args()

def main():
    args = parse_args()
    start_date = datetime.strptime(args.start_date, '%m/%d/%Y').date()
    end_date = datetime.strptime(args.end_date, '%m/%d/%Y').date()

    csv.field_size_limit(sys.maxsize) 

    complaint_counts = {}

    with open(args.input, 'r') as input_file:
        reader = csv.DictReader(input_file)
        for row in reader:
            try:
                created_date_str = row['Created Date']
                created_date = datetime.strptime(created_date_str.split()[0], '%m/%d/%Y').date()
            except (ValueError, KeyError):
                continue  

            if start_date <= created_date <= end_date:
                borough = row.get('Borough', '').strip()
                complaint_type = row.get('Complaint Type', '').strip()
                if borough and complaint_type:
                    key = (complaint_type, borough)
                    complaint_counts[key] = complaint_counts.get(key, 0) + 1

    output_data = [
        ['Complaint Type', 'Borough', 'Count']
    ]
    for (complaint_type, borough), count in sorted(complaint_counts.items()):
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
