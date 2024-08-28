"""
1. File Handling and Array Operations
"""

import os
import csv
import logging
import numpy as np
import pydicom

# Configure logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')


def list_folder_contents(path):
    """List the contents of a folder and count the number of elements
    inside."""
    try:
        items = os.listdir(path)
        print(f"Total items in '{path}': {len(items)}")
        for item in items:
            print(item)
    except Exception as e:
        logging.error(f"Error accessing folder {path}: {e}")


def read_csv_file(path, filename):
    """Read a CSV file, print columns, number of rows, and calculate
    statistics for numeric columns."""
    try:
        filepath = os.path.join(path, filename)
        if not os.path.isfile(filepath):
            raise FileNotFoundError(f"The file '{filename}' does not exist.")

        with open(filepath, mode='r') as file:
            reader = csv.reader(file)
            header = next(reader)
            rows = list(reader)

        print(f"Columns: {header}")
        print(f"Number of rows: {len(rows)}")

        # Convert to numpy array for processing numeric data
        data = np.array(rows)
        for i, col_name in enumerate(header):
            try:
                col_data = data[:, i].astype(float)
                avg = np.mean(col_data)
                std_dev = np.std(col_data)
                print(f"Column '{col_name}': Average = {avg}, Standard Deviation = {std_dev}")
            except ValueError:
                print(f"Column '{col_name}' is not numeric, skipping statistical analysis.")

    except Exception as e:
        logging.error(f"Error processing CSV file '{filename}': {e}")


def read_dicom_file(path, filename, *tags):
    """Read a DICOM file and print basic information and optional tags."""
    try:
        filepath = os.path.join(path, filename)
        if not os.path.isfile(filepath):
            raise FileNotFoundError(f"The file '{filename}' does not exist.")

        dicom_data = pydicom.dcmread(filepath)

        print(f"Patient's Name: {dicom_data.PatientName}")
        print(f"Study Date: {dicom_data.StudyDate}")
        print(f"Modality: {dicom_data.Modality}")

        for tag in tags:
            try:
                tag_value = dicom_data[tag].value
                print(f"Tag {hex(tag)}: {tag_value}")
            except KeyError:
                print(f"Tag {hex(tag)} not found in the DICOM file.")

    except Exception as e:
        logging.error(f"Error processing DICOM file '{filename}': {e}")


# Example usage
if __name__ == '__main__':
    print("--- List Folder Contents ---")
    list_folder_contents('/Users/cristianpinzon/Downloads/prueba_python')
    print("--- Read CSV File ---")
    read_csv_file('/Users/cristianpinzon/Downloads/prueba_python', 'sample-01-csv.csv')
    print("--- Read DICOM File ---")
    read_dicom_file('/Users/cristianpinzon/Downloads/prueba_python', 'sample-01-dicom.dcm', 0x0008, 0x0010)
