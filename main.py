import csv
from datetime import datetime

# File paths
file_path = 'PeopleTrainingDate.csv'
output_file_path = 'PeopleTrainingDateSorted.csv'
update_file_path = 'PeopleTrainingDateUpdate.csv'

def main():
    # Parse and print the initial table
    parse_and_print_table(file_path)
    
    # Parse, sort, and output the initial table to a new file
    parse_sort_and_output_table(file_path, output_file_path)

    # Read update data from a CSV file
    update_data = read_csv(update_file_path)
    
    # Rearrange the update data to match the desired format
    rearranged_update_data = rearrange_data(update_data)
    
    # Append the rearranged update data to the output file
    append_csv(rearranged_update_data, output_file_path)
    
    # Parse, sort, and output the updated table to the same file
    parse_sort_and_output_table(output_file_path, output_file_path)

def parse_and_print_table(file_path):
    # Open and read the CSV file
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        headers = reader.fieldnames
        data = list(reader)

    # Calculate column widths for pretty printing
    col_widths = {header: max(len(header), max(len(row[header]) for row in data)) for header in headers}

    # Print the header row
    header_row = ' | '.join(header.ljust(col_widths[header]) for header in headers)
    print(header_row)
    print('-' * len(header_row))

    # Print each data row
    for row in data:
        data_row = ' | '.join(row[header].ljust(col_widths[header]) for header in headers)
        print(data_row)

def parse_sort_and_output_table(file_path, output_file_path):
    # Open and read the CSV file
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        headers = reader.fieldnames
        data = list(reader)

    # Sort data by the 'Updated' column
    data.sort(key=lambda x: datetime.strptime(x['Updated'], '%d/%m/%Y'))
    
    # Reorder headers to have 'Updated' first
    reordered_headers = ['Updated'] + [header for header in headers if header != 'Updated']

    # Write sorted data to the output file
    with open(output_file_path, 'w', newline='') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=reordered_headers)
        writer.writeheader()
        writer.writerows(data)

def read_csv(file_path):
    # Read CSV file and return data as a list of rows
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        return list(reader)

def rearrange_data(data):
    # Rearrange data to match the desired format
    return [
        {
            'Updated': row[0],
            'Title': row[3],
            'Name': row[4],
            'ID': row[2],
            'Email': row[1],
            'Company': row[5]
        }
        for row in data
    ]

def append_csv(data, file_path):
    # Append data to the CSV file
    with open(file_path, 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writerows(data)

if __name__ == "__main__":
    main()
