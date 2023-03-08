import pandas as pd

# Load the CSV file into a Pandas DataFrame
df = pd.read_csv("Nursing_Fundamentals_Raw_Data.csv")

# Drop the rows where the third column is empty
df = df.dropna(subset=[df.columns[2]])

# Save the updated DataFrame to a new CSV file
df.to_csv("Nursing_Fundamentals_Removed_Empty_Rows.csv", index=False)
