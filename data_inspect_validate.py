import pandas as pd

sold = pd.read_csv("sold.csv", low_memory=False)
listings = pd.read_csv("listing.csv", low_memory=False)

print(f'Sold Columns: {sold.columns}')
print(f'Sold Head: {sold.head()}')

print(sold['PropertyType'].unique())
print(f'Sold Shape: {sold.shape}')
print(sold.dtypes)
print(sold.isnull().sum())

missing_values = sold.isnull().sum()
dropped_columns = missing_values[missing_values > 0.9 * len(sold)].index

print('Columns with more than 90% missing values:')
print(dropped_columns)

sold = sold.drop(columns = dropped_columns)

print(f'Sold shape after dropping columns: {sold.shape}')

columns_to_summarize = ["ClosePrice", "LivingArea", "DaysOnMarket"]
for column in columns_to_summarize:
    print(f"\n{column}")
    print("Min", sold[column].min())
    print("Max", sold[column].max())
    print("Mean", sold[column].mean())
    print("Median", sold[column].median())
    print("25th Percentile:", sold[column].quantile(0.25))
    print("50th Percentile:", sold[column].quantile(0.50))
    print("75th Percentile:", sold[column].quantile(0.75))

# 67 rows have a $0 Close Price
# 131 rows have 0 listed as Living Area

print(f'Number of rows with negative values in DaysOnMarket column: {(sold["DaysOnMarket"] < 0).sum()}')

sold.to_csv("sold_filtered.csv", index=False)
