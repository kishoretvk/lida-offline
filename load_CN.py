import pandas as pd
import zipfile
import os

# Path to the zip file
zip_file_path = "../DATA/202309_fixed_postcode_coverage_r01/postcode_files.zip"


# Path to the directory containing the extracted CSV files
# directory_path = "..//DATA//combined_postcode_data.csv"

# Initialising an empty DataFrame to store the combined data
combined_data = pd.DataFrame()

# Open the zip file
with zipfile.ZipFile(zip_file_path, 'r') as z:
    # Looping through each file in the directory and processing the data
    for filename in z.namelist():
        # Check if the file is a CSV file
        if filename.endswith('.csv'):
            # Open each file
            with z.open(filename) as f:
                # Read the CSV data
                try:
                    # Reading the data from each file
                    data = pd.read_csv(f)
                    
                    # Selecting the required columns and renaming them as specified
                    selected_data = data[['postcode_space', 'Gigabit availability (% premises)', 
                                          '% of premises with NGA',
                                          '% of premises below the USO', 
                                          '% of premises unable to receive 30Mbit/s']]
                    

                    # print the fillename and the number of rows in the selected data
                    print(filename, ":", selected_data.shape[0])

                    # Appending the selected data to the combined DataFrame
                    # print(type(combined_data))
                    # print(selected_data)
                    # print(type(selected_data))
                    # combined_data = combined_data.append(selected_data, ignore_index=True)
                    combined_data = pd.concat([combined_data, selected_data], ignore_index=True)

                except Exception as e:
                    # In case of any error, we'll skip the file and continue with the next
                    print("Error processing file: ", filename)
                    print("Exception: ", str(e))
                    continue

# Renaming the columns in the combined data
combined_data.rename(columns={'postcode_space': 'Postcode',
                            'Gigabit availability (% premises)': 'Gigabit',
                            '% of premises with NGA': 'Superfast',
                            '% of premises below the USO': 'Sub_USO',
                            '% of premises unable to receive 30Mbit/s': 'Sub_superfast'}, inplace=True)


# Subtract the Gigabit from the SFBB to get the Superfast and round to 1 decimal place
combined_data['Superfast'] = round(combined_data['Superfast'] - combined_data['Gigabit'])

# Subtract the Sub_USO from the Sub_superfast to get the Sub_superfast above USO and round to 1 decimal place
combined_data['Sub_superfast'] = round(combined_data['Sub_superfast'] - combined_data['Sub_USO'])

# Add a new 'Total' column that is the sum of the other columns
combined_data['Total'] = combined_data['Gigabit'] + combined_data['Superfast'] + combined_data['Sub_USO'] + combined_data['Sub_superfast']

# Saving the combined data to a new CSV file
output_file_path = "../DATA/202309_fixed_postcode_coverage_r01/combined_postcode.csv"
combined_data.to_csv(output_file_path, index=False)


# print the output_file_path and the number of rows in the combined data
print(output_file_path, ":", combined_data.shape[0])
print(combined_data.head())

