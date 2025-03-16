import pandas as pd

# Load the three CSV files into pandas DataFrames
df1 = pd.read_csv('restaurant_data.csv')
df2 = pd.read_csv('robot_restaurant_data.csv')
df3 = pd.read_csv('qr_code_restaurant_data.csv')

# Concatenate the DataFrames into one
combined_df = pd.concat([df1, df2, df3], ignore_index=True)

# Write the combined DataFrame to a new CSV file
combined_df.to_csv('mathuria_restauraunt_data.csv', index=False)

print("CSV files have been successfully combined and saved as 'mathuria_restauraunt_data.csv'")

output_table = combined_df
