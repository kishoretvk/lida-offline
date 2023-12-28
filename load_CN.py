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
                                          'SFBB availability (% premises)',
                                          '% of premises below the USO', 
                                          '% of premises unable to receive 30Mbit/s']]
                    selected_data.rename(columns={'postcode_space': 'Postcode',
                                                'Gigabit availability (% premises)': 'Gigabit',
                                                'SFBB availability (% premises)': 'Superfast',
                                                '% of premises below the USO': 'Sub_USO',
                                                '% of premises unable to receive 30Mbit/s': 'Sub_superfast'}, inplace=True)
                    
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

# Saving the combined data to a new CSV file
output_file_path = "../DATA/202309_fixed_postcode_coverage_r01/combined_postcode.csv"
combined_data.to_csv(output_file_path, index=False)

output_file_path
