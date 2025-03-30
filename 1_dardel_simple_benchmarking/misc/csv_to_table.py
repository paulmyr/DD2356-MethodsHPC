import pandas as pd
import argparse
from tabulate import tabulate

def read_csv_and_print_table(file_path):
    pd.set_option('display.max_columns', None)
    data = pd.read_csv(file_path, delimiter=';')
    
    print(tabulate(data, headers='keys', tablefmt='grid', showindex=False))


def main():
    parser = argparse.ArgumentParser(description='Read and display a CSV file with ";" delimiter.')
    parser.add_argument('file_path', type=str, help='Path to the CSV file')
    
    args = parser.parse_args()

    read_csv_and_print_table(args.file_path)

if __name__ == '__main__':
    main()