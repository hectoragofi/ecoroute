import pandas as pd

# Read the CSV file
df = pd.read_csv('portsdirty.csv')

# Select only the required columns
selected_columns = ['World Port Index Number', 'Latitude', 'Longitude', 'Main Port Name']
cleaned_df = df[selected_columns]

# Write the cleaned data to a new CSV file
cleaned_df.to_csv('ports.csv', index=False)
