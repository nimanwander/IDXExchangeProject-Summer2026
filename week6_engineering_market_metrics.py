import geopandas as gpd 
import pandas as pd

sold = pd.read_csv('sold_cleaned.csv', low_memory=False)
listings = pd.read_csv('listings_cleaned.csv', low_memory=False)
districts = gpd.read_file("DistrictAreas2526_-276418018002580880.geojson")

sold["CloseDate"] = pd.to_datetime(sold["CloseDate"])
sold["PurchaseContractDate"] = pd.to_datetime(sold["PurchaseContractDate"])
sold["ListingContractDate"] = pd.to_datetime(sold["ListingContractDate"])

districts = districts[districts["DistrictType"] == "Unified"]
districts = districts.to_crs("EPSG:4326")
sold_geo = gpd.GeoDataFrame(sold, geometry=gpd.points_from_xy(sold["Longitude"], sold["Latitude"]), crs="EPSG:4326")
listings_geo = gpd.GeoDataFrame(listings, geometry=gpd.points_from_xy(listings["Longitude"], listings["Latitude"]), crs="EPSG:4326")

sold_geo = gpd.sjoin(sold_geo, districts[["DistrictName", "geometry"]], how="left", predicate="within")
listings_geo = gpd.sjoin(listings_geo, districts[["DistrictName", "geometry"]], how="left", predicate="within")

sold["DistrictName"] = sold_geo["DistrictName"].values
listings["DistrictName"] = listings_geo["DistrictName"].values

sold["PriceRatio"] = sold["ClosePrice"] / sold ["OriginalListPrice"].replace(0,pd.NA)
sold["PriceRatioFlag"] = (sold["PriceRatio"] < 0.5) | (sold["PriceRatio"] > 2.0)
sold.loc[sold["PriceRatioFlag"], "PriceRatio"] = pd.NA
sold["PricePerSqFt"] = sold["ClosePrice"] / sold ["LivingArea"]
sold["Year"] = sold["CloseDate"].dt.year
sold["Month"] = sold["CloseDate"].dt.month
sold["YrMo"] = sold["CloseDate"].dt.to_period("M").astype(str)

sold['CloseToOriginalListRatio'] = sold["ClosePrice"] / sold["OriginalListPrice"].replace(0,pd.NA)
sold['ListingToContractDays'] = (sold["PurchaseContractDate"] - sold["ListingContractDate"]).dt.days
sold['ContractToCloseDays'] = (sold["CloseDate"] - sold["PurchaseContractDate"]).dt.days

metric_columns = ["ClosePrice", "OriginalListPrice", "LivingArea", "PriceRatio", "PricePerSqFt", "DaysOnMarket", "Year", "Month", "YrMo", "CloseToOriginalListRatio", "ListingToContractDays", "ContractToCloseDays"]

#print(sold[metric_columns].head())
#print(sold[["ListingContractDate", "PurchaseContractDate", "CloseDate", "ListingToContractDays", "ContractToCloseDays"]].head(10))

sold["ContractToCloseFlag"] = sold["ContractToCloseDays"] < 0
#print("Negative ContractToCloseDays:", sold["ContractToCloseFlag"].sum())

sold["ListingToContractFlag"] = sold["ListingToContractDays"] < 0
#print("Negative ListingToContractDays:", sold["ListingToContractFlag"].sum())

property_type_summary = sold.groupby("PropertyType").agg(SalesCount = ("ClosePrice", "count"), AverageClosePrice = ("ClosePrice", "mean"), AveragePricePerSqFt = ("PricePerSqFt", "mean"), AverageDaysOnMarket = ("DaysOnMarket", "mean"), AveragePriceRatio = ("PriceRatio", "mean")).reset_index()
print(property_type_summary)

property_subtype_summary = sold.groupby("PropertySubType").agg(SalesCount = ("ClosePrice", "count"), AverageClosePrice = ("ClosePrice", "mean"), AveragePricePerSqFt = ("PricePerSqFt", "mean"), AverageDaysOnMarket = ("DaysOnMarket", "mean"), AveragePriceRatio = ("PriceRatio", "mean")).reset_index()
print(property_subtype_summary)

county_or_parish_summary = sold.groupby("CountyOrParish").agg(SalesCount = ("ClosePrice", "count"), AverageClosePrice = ("ClosePrice", "mean"), AveragePricePerSqFt = ("PricePerSqFt", "mean"), AverageDaysOnMarket = ("DaysOnMarket", "mean"), AveragePriceRatio = ("PriceRatio", "mean")).reset_index()
print(county_or_parish_summary)

mls_area_summary = sold.groupby("MLSAreaMajor").agg(SalesCount = ("ClosePrice", "count"), AverageClosePrice = ("ClosePrice", "mean"), AveragePricePerSqFt = ("PricePerSqFt", "mean"), AverageDaysOnMarket = ("DaysOnMarket", "mean"), AveragePriceRatio = ("PriceRatio", "mean")).reset_index()
print(mls_area_summary)

list_office_name_summary = sold.groupby("ListOfficeName").agg(SalesCount = ("ClosePrice", "count"), AverageClosePrice = ("ClosePrice", "mean"), AveragePricePerSqFt = ("PricePerSqFt", "mean"), AverageDaysOnMarket = ("DaysOnMarket", "mean"), AveragePriceRatio = ("PriceRatio", "mean")).reset_index()
print(list_office_name_summary)

buyer_office_summary = sold.groupby("BuyerOfficeName").agg(SalesCount = ("ClosePrice", "count"), AverageClosePrice = ("ClosePrice", "mean"), AveragePricePerSqFt = ("PricePerSqFt", "mean"), AverageDaysOnMarket = ("DaysOnMarket", "mean"), AveragePriceRatio = ("PriceRatio", "mean")).reset_index()
print(buyer_office_summary)

sold.to_csv("sold_week6_market_metrics.csv", index=False)
listings.to_csv("listings_week6_market_metrics.csv", index=False)

property_type_summary.to_csv("property_type_summary.csv", index=False)
property_subtype_summary.to_csv("property_subtype_summary.csv", index=False)
county_or_parish_summary.to_csv("county_or_parish_summary.csv", index=False)
mls_area_summary.to_csv("mls_area_summary.csv", index=False)
list_office_name_summary.to_csv("list_office_name_summary.csv", index=False)
buyer_office_summary.to_csv("buyer_office_summary.csv", index=False)