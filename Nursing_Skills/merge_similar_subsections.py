import pandas as pd

# Load the data into a pandas DataFrame
df = pd.read_csv('extracted_data.csv')

# Initialize variables
merged_rows = []
current_row = df.loc[0]

# Iterate through each row in the DataFrame
for i in range(1, len(df)):
    # If the current row's subsection is the same as the next row's subsection
    if current_row['Subsection'] == df.loc[i, 'Subsection']:
        # Merge the two rows
        current_row['Text'] += '\n' + df.loc[i, 'Text']
    else:
        # Add the current row to the list of merged rows
        merged_rows.append(current_row)
        # Set the current row to the next row
        current_row = df.loc[i]

# Add the final row to the list of merged rows
merged_rows.append(current_row)

# Create a new DataFrame from the merged rows
merged_df = pd.DataFrame(merged_rows)

# Save the merged DataFrame to a new CSV file
merged_df.to_csv('merged_subsections_file.csv', index=False)
