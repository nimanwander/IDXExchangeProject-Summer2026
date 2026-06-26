import pandas as pd

sold1 = pd.read_csv('CRMLSSold202601.csv')    #num of rows: 16487
sold2 = pd.read_csv('CRMLSSold202602.csv')    #num of rows: 19010
sold3 = pd.read_csv('CRMLSSold202603.csv')    #num of rows: 23372
sold4 = pd.read_csv('CRMLSSold202604.csv')    #num of rows: 24261
sold = pd.concat([sold1, sold2, sold3, sold4])
#sold number of rows before filtering is 83130
#sold number of rows after filtering is 54592

listing1 = pd.read_csv('CRMLSListing202601.csv')    #num of rows: 35302
listing2 = pd.read_csv('CRMLSListing202602.csv')    #num of rows: 32884
listing3 = pd.read_csv('CRMLSListing202603.csv')    #num of rows: 39153
listing4 = pd.read_csv('CRMLSListing202604.csv')    #num of rows: 39020
listing = pd.concat([listing1, listing2, listing3, listing4])
#listing number of rows before filtering is 146359
#listing number of rows after filtering is 95035

sold_filtered = sold[sold['PropertyType'] == 'Residential']
listing_filtered = listing[listing['PropertyType'] == 'Residential']

sold_filtered.to_csv('Sold2026.csv', index=False)
listing_filtered.to_csv('Listing2026.csv', index=False)