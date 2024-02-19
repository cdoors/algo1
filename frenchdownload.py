import requests
import zipfile
import os
import pandas as pd

# URL of the Ken French data ZIP file
url = 'https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_Factors_CSV.zip'

# Download the ZIP file
response = requests.get(url)
zip_filename = 'F-F_Research_Data_Factors_CSV.zip'

# Ensure the response is successful
if response.status_code == 200:
    # Save the ZIP file locally
    with open(zip_filename, 'wb') as file:
        file.write(response.content)
    
    # Extract the ZIP file
    with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
        zip_ref.extractall('.')  # Extract to the current directory
    
    print(f"Extracted files: {zip_ref.namelist()}")  # Print the names of the extracted files
    
    # Assuming you know the name of the CSV file or it's the only CSV file extracted
    csv_filename = [name for name in zip_ref.namelist() if name.endswith('.csv')][0]
    
    # Load the CSV file into a pandas DataFrame
    french_data = pd.read_csv(csv_filename)
    
    print(french_data.head())  # Display the first few rows of the dataset
    
    # Cleanup: Remove the ZIP file after extraction (optional)
    os.remove(zip_filename)
else:
    print("Failed to download the file")

# Note: Adjust the script as necessary based on the exact content and format of the Ken French data.
