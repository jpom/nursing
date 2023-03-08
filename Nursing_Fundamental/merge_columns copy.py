import pandas as pd

# Load the CSV file into a Pandas DataFrame
df = pd.read_csv("Nursing_Fundamentals_Removed_Empty_Rows.csv")

# Concatenate columns 1 and 2 into a single column
df["title"] = df.iloc[:,0].astype(str) + " " + df.iloc[:,1].astype(str)

# Concatenate columns 3 and 4 into a single column
df["heading"] = df.iloc[:,2].astype(str) + " " + df.iloc[:,3].astype(str)

# Concatenate columns 1, 2, 3, and 4 into a single column
df["content"] = df.iloc[:,0].astype(str) + " " + df.iloc[:,1].astype(str) + " " + df.iloc[:,2].astype(str) + " " + df.iloc[:,3].astype(str)

# Drop the first 4 columns
df.drop(df.columns[0:4], axis=1, inplace=True)

# Save the updated DataFrame to a new CSV file
df.to_csv("Nursing_Fundamentals_Merged_File.csv", index=False)
