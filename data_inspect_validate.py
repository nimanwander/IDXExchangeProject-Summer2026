import pandas as pd

sold = pd.read_csv("sold.csv", low_memory=False)
listings = pd.read_csv("listing.csv", low_memory=False)

print(sold.columns)
print(sold.head())

print(sold['PropertyType'].unique())
print(sold.shape)
print(sold.dtypes)
print(sold.isnull().sum())
