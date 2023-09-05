import os
import pandas as pd
import csv

def getExistingCSV():
    
    folder_path = os.getcwd()

    # Get the list of files in the folder
    file_list = os.listdir(folder_path)
    print(1)
    # Filter the files with the ".csv" extension
    csv_files = [file for file in file_list if file.endswith(".csv")]
    num_csv = len(csv_files)
    total_row_count=0
    # Print the list of CSV files
    for csv_file in csv_files:
        print(csv_file)
        with open(csv_file, 'r') as file:
            csv_reader = csv.reader(file)
            row_count = sum(1 for row in csv_reader)-1
            print(f"File: {csv_file}, Number of rows: {row_count}")
            total_row_count += row_count
    data = {"num_csv" : num_csv, "total_row_count" : total_row_count}
    print(data)
    return data

def main():
    getExistingCSV()

if __name__ == '__main__':
    main()
