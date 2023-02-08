import csv
import shutil
import os

def change_type(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        headers = next(reader)
        
        if "Type" not in headers or "Description" not in headers or "Product" not in headers:
            print("Warning: Some of the required headers (Type, Description, and Product) are missing. Skipping change_type function.")
            return
        
        type_index = headers.index("Type")
        desc_index = headers.index("Description")
        prod_index = headers.index("Product")
        
        rows = [row for row in reader]
        
        for i, row in enumerate(rows):
            if row[desc_index] == "Exchanged to KEEP":
                rows[i][type_index] = "buy"
            elif row[type_index] == "TRANSFER" and row[prod_index] == "Savings":
                rows[i][type_index] = "sell"
            elif row[type_index] == "TRANSFER" and row[prod_index] == "Current":
                rows[i][type_index] = "buy"    
            elif row[type_index] == 'EXCHANGE' and row[prod_index] == 'Current' and 'GBP' in row[desc_index]:
                row[type_index] = 'sell'
            elif row[type_index] == 'EXCHANGE' and row[prod_index] == 'Current' and 'GBP' not in row[desc_index]:
                row[type_index] = 'buy' 

                     
                
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

def delete_column_by_header(filename, headers_to_delete):
    shutil.copy2(filename, f"{filename}.bak")

    with open(filename, 'r') as f_in:
        reader = csv.reader(f_in)
        headers = next(reader)
        column_indices = []
        for header in headers_to_delete:
            try:
                column_index = headers.index(header)
                column_indices.append(column_index)
            except ValueError:
                print(f"Error: Header '{header}' not found in file.")
        data = [row for row in reader]

    with open(filename, 'w', newline='') as f_out:
        writer = csv.writer(f_out)
        writer.writerow([h for i, h in enumerate(headers) if i not in column_indices])
        for row in data:
            writer.writerow([cell for i, cell in enumerate(row) if i not in column_indices])

def add_empty_columns(filename, new_headers):
    with open(filename, 'r') as f_in:
        reader = csv.reader(f_in)
        headers = next(reader)
        for header in new_headers:
            if header not in headers:
                headers.extend(new_headers)
                break
        data = [row for row in reader]

    with open(filename, 'w', newline='') as f_out:
        writer = csv.writer(f_out)
        writer.writerow(headers)
        for row in data:
            if len(row) < len(headers):
                row.extend(["", ""] * len(new_headers))
            writer.writerow(row)

def rearrange_columns(filename, header_order):
    with open(filename, 'r') as f_in:
        reader = csv.reader(f_in)
        headers = next(reader)
        data = [row for row in reader]

    if header_order[0] in headers:
        new_headers = header_order
        new_data = [[row[headers.index(header)] for header in new_headers] for row in data]

        with open(filename, 'w', newline='') as f_out:
            writer = csv.writer(f_out)
            writer.writerow(new_headers)
            for row in new_data:
                writer.writerow(row)
    else:
        print(f"{header_order[0]} not found in header row.")


def rename_headers(filename, header_order):
    with open(filename, 'r') as f_in:
        reader = csv.reader(f_in)
        headers = next(reader)
        header_map = {headers[i]: header for i, header in enumerate(header_order)}
        data = [row for row in reader]

    with open(filename, 'w', newline='') as f_out:
        writer = csv.writer(f_out)
        new_headers = [header_map.get(header, header) for header in headers]
        writer.writerow(new_headers)
        for row in data:
            writer.writerow(row)            

def change_fee_values(filename):
    with open(filename, 'r') as f_in:
        reader = csv.reader(f_in)
        headers = next(reader)
        type_index = headers.index("Type")
        fee_currency_index = headers.index("Fee Currency")
        fee_amount_index = headers.index("Fee Amount")
        data = [row for row in reader]

    with open(filename, 'w', newline='') as f_out:
        writer = csv.writer(f_out)
        writer.writerow(headers)
        for row in data:
            if row[type_index] == "EXCHANGE" :
            # if row[type_index] == "EXCHANGE" and  row[fee_amount_index] == "":
                row[fee_currency_index] = "GBP"
                # row[fee_amount_index] = "0.00"
            writer.writerow(row)

def convert_string(filename, original_string, new_string):
    with open(filename, 'r') as f_in:
        reader = csv.reader(f_in)
        headers = next(reader)
        data = [row for row in reader]

    if "Type" in headers:
        index = headers.index("Type")
        new_data = [[new_string if cell == original_string else cell for cell in row] for row in data]

        with open(filename, 'w', newline='') as f_out:
            writer = csv.writer(f_out)
            writer.writerow(headers)
            for row in new_data:
                writer.writerow(row)
    else:
        print("Type not found in header row.")

def delete_rows(filename, type_value):
    with open(filename, 'r') as f_in:
        reader = csv.reader(f_in)
        headers = next(reader)
        data = [row for row in reader]

    if "Type" in headers:
        index = headers.index("Type")
        new_data = [row for row in data if row[index] != type_value]

        with open(filename, 'w', newline='') as f_out:
            writer = csv.writer(f_out)
            writer.writerow(headers)
            for row in new_data:
                writer.writerow(row)
    else:
        print("Type not found in header row.")

def swap_values(filename, type_value, received_currency_value):
    temp_file = filename + "_temp.csv"
    with open(filename, "r") as csvfile, open(temp_file, "w", newline="") as tempfile:
        reader = csv.DictReader(csvfile)
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(tempfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in reader:
            if row["Type"].lower() == type_value.lower() and row["Received Currency"] != received_currency_value:
                row["Received Currency"], row["Sent Currency"] = row["Sent Currency"], row["Received Currency"]
                row["Received Amount"], row["Sent Amount"] = row["Sent Amount"], row["Received Amount"]
            writer.writerow(row)
    with open(temp_file, "r") as tempfile:
        with open(filename, "w", newline="") as csvfile:
            csvfile.write(tempfile.read())

def fill_fee_info(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        headers = next(reader)
        
        if "Fee Currency" not in headers or "Fee Amount" not in headers:
            return
        
        fee_currency_index = headers.index("Fee Currency")
        fee_amount_index = headers.index("Fee Amount")
        received_amount_index = headers.index("Received Amount")
        data = [row for row in reader]

    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        
        for row in data:
            if row[fee_currency_index] == '':
                row[fee_currency_index] = 'GBP'
                
            if row[fee_amount_index] == '':
                row[fee_amount_index] = '0.00'

            if row[received_amount_index] == '':
                row[received_amount_index] = '0.00'
                
            writer.writerow(row)

def remove_negative(filename):
    with open(filename, "r") as file:
        reader = csv.reader(file)
        header = next(reader)
        rows = [row for row in reader]
    
    if "Received Amount" not in header or "Sent Amount" not in header or "Fee Amount" not in header:
        print("Error: One of the required columns not found.")
        return

    received_amount_index = header.index("Received Amount")
    sent_amount_index = header.index("Sent Amount")
    fee_amount_index = header.index("Fee Amount")

    for row in rows:
        if row[received_amount_index].strip() != '' and row[received_amount_index][0] == "-":
            row[received_amount_index] = row[received_amount_index][1:]
        if row[sent_amount_index].strip() != '' and row[sent_amount_index][0] == "-":
            row[sent_amount_index] = row[sent_amount_index][1:]
        if row[fee_amount_index].strip() != '' and row[fee_amount_index][0] == "-":
            row[fee_amount_index] = row[fee_amount_index][1:]
    
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(rows)                

change_type('example.csv')
headers_to_delete = ['Product', 'Started Date', 'State', 'Balance', 'Description']
delete_column_by_header('example.csv', headers_to_delete)
add_empty_columns('example.csv', ['Received Net Worth', 'Sent Net Worth', 'Fee Currency', 'Fee Net Worth'])


rearrange_columns('example.csv', [
    'Completed Date',
    'Type',
    'Currency',
    'Amount',
    'Received Net Worth',
    'Base currency',
    'Fiat amount',
    'Sent Net Worth',
    'Fee Currency',
    'Fee',
    'Fee Net Worth'
])

rename_headers('example.csv', [
    'Date',
    'Type',
    'Received Currency',
    'Received Amount',
    'Received Net Worth',
    'Sent Currency',
    'Sent Amount',
    'Sent Net Worth',
    'Fee Currency',
    'Fee Amount',
    'Fee Net Worth'
])

# change_fee_values('example.csv')
convert_string('example.csv', "EXCHANGE", "buy")
# delete_rows('example.csv', "TRANSFER")
swap_values('example.csv', "sell", "GBP")
fill_fee_info('example.csv')
remove_negative("example.csv")







# Now can we make code that rearranges the order of columns into based on this header order "Complete Date, Type, Currency, Amount, 
