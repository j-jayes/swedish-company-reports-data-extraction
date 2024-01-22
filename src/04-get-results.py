# Adjusting the script to process the newly uploaded file (1976) and save the results to an Excel sheet
import re
import pandas as pd
import os

def is_number(string):
    # Regular expression for a valid number (integer or decimal)
    return re.match(r"\\d", string) is not None

def extract_financial_data_general(file_path):
    # Read the file content
    with open(file_path, 'r') as file:
        file_content = file.read()

    # extract year from file_path by looking for a number of 4 digits after data/companies/Electrolux/extracted_data/
    year_match = re.search(r"data/companies/Electrolux/extracted_data/(\d{4})", file_path)
    year = year_match.group(1) if year_match is not None else None
    year = int(year)


    # Extract the JSON-like string
    start = file_content.find('```json\n') + len('```json\n')
    end = file_content.find('\n```', start)
    json_string = file_content[start:end]

    # Use regular expressions to extract the key-value pairs
    sales_total_match = re.search(r'"sales_total": "([^"]+)"', json_string)
    taxes_match = re.search(r'"taxes": "([^"]+)"', json_string)
    net_profit_match = re.search(r'"net_profit": "([^"]+)"', json_string)

    # Extract the values from the matches, if match is not None
    sales_total = sales_total_match.group(1) if sales_total_match is not None else None
    taxes = taxes_match.group(1) if taxes_match is not None else None
    net_profit = net_profit_match.group(1) if net_profit_match is not None else None


    return {"year": year, "sales_total": sales_total, "taxes": taxes, "net_profit": net_profit}


# folder path at "data/companies/Electrolux/extracted_data"
folder_path = 'data/companies/Electrolux/extracted_data'

# list of files in the folder
files = os.listdir(folder_path)

# create an empty list to store the results
results = []

# loop through the files
for file in files:
    # extract the financial data
    financial_data = extract_financial_data_general(os.path.join(folder_path, file))

    # append the results to the list
    results.append(financial_data)

# convert the list to a DataFrame
results_df = pd.DataFrame(results)

# arrange results_df by year
results_df = results_df.sort_values("year")

# save the DataFrame to an Excel file
results_df.to_excel("data/companies/Electrolux/extracted_data/extracted_data.xlsx", index=False)
