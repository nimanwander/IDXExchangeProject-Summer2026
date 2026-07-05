import pandas as pd
import os

sold_dfs = []
listing_dfs= []

for year in range (2024,2027):
    for month in range (1,13):
        sold_file = f"CRMLSSold{year}{month:02d}.csv"
        listing_file = f"CRMLSListing{year}{month:02d}.csv"
    
        if os.path.exists(sold_file):
            sold_dfs.append(pd.read_csv(sold_file, low_memory=False))
        if os.path.exists(listing_file):
            listing_dfs.append(pd.read_csv(listing_file, low_memory=False))

sold = pd.concat(sold_dfs, ignore_index=True)
listing = pd.concat(listing_dfs,ignore_index=True)

print(f'Number of rows in concated sold file before filtering: {len(sold)}')
print(f'Number of rows in concated listing file before filtering: {len(listing)}')

sold_filtered = sold[sold['PropertyType'] == 'Residential']
listing_filtered = listing[listing['PropertyType'] == 'Residential']

print(f'Number of rows in filtered concated sold file: {len(sold_filtered)}')
print(f'Number of rows in filtered concated listing file: {len(listing_filtered)}')

sold_filtered.to_csv('Sold.csv', index=False)
listing_filtered.to_csv('Listing.csv', index=False)
