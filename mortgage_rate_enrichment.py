import pandas as pd

sold = pd.read_csv("sold_filtered.csv", low_memory=False)
listings = pd.read_csv("listing.csv", low_memory=False)

url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=MORTGAGE30US"
mortgage = pd.read_csv(url, parse_dates=['observation_date'])

mortgage.columns = ['date', 'rate_30yr_fixed']
mortgage['year_month'] = mortgage['date'].dt.to_period('M')
mortgage_monthly = (mortgage.groupby('year_month')['rate_30yr_fixed'].mean().reset_index())

sold['year_month'] = pd.to_datetime(sold['CloseDate']).dt.to_period('M')

listings['year_month'] = pd.to_datetime(listings['ListingContractDate']).dt.to_period('M')

sold_with_rates = sold.merge(mortgage_monthly, on='year_month', how='left')
listings_with_rates = listings.merge(mortgage_monthly, on='year_month', how='left')

sold_with_rates.to_csv("sold_with_mortage_rates.csv", index=False)
listings_with_rates.to_csv("listings_with_mortage_rates.csv", index=False)
