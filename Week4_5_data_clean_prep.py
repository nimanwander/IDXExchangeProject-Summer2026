import pandas as pd
sold = pd.read_csv("sold_with_mortage_rates.csv", low_memory=False)
listings = pd.read_csv("listings_with_mortage_rates.csv", low_memory=False)

sold_before = len(sold)
listings_before = len(listings)
sold["CloseDate"] = pd.to_datetime(sold["CloseDate"])
sold["PurchaseContractDate"] = pd.to_datetime(sold["PurchaseContractDate"])
sold["ListingContractDate"] = pd.to_datetime(sold["ListingContractDate"])
sold["ContractStatusChangeDate"] = pd.to_datetime(sold["ContractStatusChangeDate"])

listings["ListingContractDate"] = pd.to_datetime(listings["ListingContractDate"])
listings["ContractStatusChangeDate"] = pd.to_datetime(listings["ContractStatusChangeDate"])
listings["CloseDate"] = pd.to_datetime(listings["CloseDate"])
listings["PurchaseContractDate"] = pd.to_datetime(listings["PurchaseContractDate"])

sold = sold.drop(columns=["ListingKey", "ListingKeyNumeric", "ListingId", "ListAgentEmail",'ListAgentFirstName','ListAgentLastName','ListAgentFullName',"CoListAgentLastName",'CoListAgentFirstName','BuyerAgentFirstName','BuyerAgentLastName','BuyerAgentMlsId','ElementarySchool','MiddleOrJuniorSchool','HighSchool', 'HighSchoolDistrict','ViewYN','BuyerAgencyCompensation','BuyerAgencyCompensationType','OriginatingSystemSubName','OriginatingSystemName','CoListOfficeName','SubdivisionName','AssociationFeeFrequency','MainLevelBedrooms','Flooring','AssociationFee','BuyerAgentAOR','BuyerOfficeAOR'])
listings = listings.drop(columns=["PropertyType.1", "ListAgentFirstName.1", "ListAgentLastName.1","DaysOnMarket.1", "ListPrice.1", "CloseDate.1", "BuyerOfficeName.1", "UnparsedAddress.1",'MiddleOrJuniorSchoolDistrict','ElementarySchoolDistrict',"AboveGradeFinishedArea","FireplacesTotal","TaxYear","BusinessType","CoveredSpaces",'TaxAnnualAmount','BelowGradeFinishedArea','CoBuyerAgentFirstName','BuilderName','LotSizeDimensions','BuildingAreaTotal','ElementarySchool','MiddleOrJuniorSchool','HighSchool','BuyerOfficeName','BuyerOfficeAOR','BuyerAgentFirstName','BuyerAgentLastName','BuyerAgentMlsId','BuyerAgentLastName','HighSchoolDistrict','BuyerAgencyCompensation','BuyerAgencyCompensationType','CoListAgentFirstName','CoListAgentLastName','CoListOfficeName','SubdivisionName','AssociationFeeFrequency'])
sold = sold.dropna(subset=["ClosePrice", "CloseDate", "ListingContractDate"])
listings = listings.dropna(subset=["BedroomsTotal", "BathroomsTotalInteger","LivingArea", "PostalCode"])

#print(sold.isnull().sum()[sold.isnull().sum() > 0].sort_values(ascending=False))
#print(listings.isnull().sum()[listings.isnull().sum() > 0].sort_values(ascending=False))

sold = sold[sold["DaysOnMarket"] >= 0]
listings = listings[listings["DaysOnMarket"] >= 0]
sold = sold[(sold["ClosePrice"] > 0) & (sold["LivingArea"] > 0)]
listings = listings[listings["LivingArea"] > 0]

numeric_columns = ["DaysOnMarket","BedroomsTotal","BathroomsTotalInteger"]
for col in numeric_columns:
    if col in sold.columns:
        print(f"{col}: {(sold[col] < 0).sum()} negative values")
    if col in listings.columns:
        print(f"{col}: {(listings[col] < 0).sum()} negative values")

check_zero_columns = ["ClosePrice", "LivingArea"]
for col in check_zero_columns:
    if col in sold.columns:
        print(f"Sold {col}: {(sold[col] == 0).sum()} zero values")
    if col in listings.columns:
        print(f"Listings {col}: {(listings[col] == 0).sum()} zero values")

sold_missing_pct = sold.isnull().mean() * 100
listings_missing_pct = listings.isnull().mean() * 100

print("SOLD >90% MISSING")
print(sold_missing_pct[sold_missing_pct > 90])

print("\nLISTINGS >90% MISSING")
print(listings_missing_pct[listings_missing_pct > 90])

sold["listing_after_close_flag"] = (sold["ListingContractDate"] > sold['CloseDate'])
sold['purchase_after_close_flag'] = (sold["PurchaseContractDate"] > sold['CloseDate'])
sold["negative_timeline_flag"] = (sold["PurchaseContractDate"] < sold["ListingContractDate"])

print("Listing after close:", sold["listing_after_close_flag"].sum())
print("Purchase after close:", sold["purchase_after_close_flag"].sum())
print("Negative timeline:", sold["negative_timeline_flag"].sum())

sold["missing_coordinates_flag"] = (sold["Latitude"].isna() | sold["Longitude"].isna())
sold["zero_coordinates_flag"] = ((sold["Latitude"] == 0) | (sold["Longitude"] == 0))
sold["positive_longitude_flag"] = (sold["Longitude"] > 0)
sold["implausible_coordinates_flag"] = ((sold["Latitude"] < -90) | (sold["Latitude"] > 90) | (sold["Longitude"] < -180) | (sold["Longitude"] > 180))

listings["missing_coordinates_flag"] = (listings["Latitude"].isna() | listings["Longitude"].isna())
listings["zero_coordinates_flag"] = ((listings["Latitude"] == 0) | (listings["Longitude"] == 0))
listings["positive_longitude_flag"] = (listings["Longitude"] > 0)
listings["implausible_coordinates_flag"] = ((listings["Latitude"] < -90) | (listings["Latitude"] > 90) | (listings["Longitude"] < -180) | (listings["Longitude"] > 180))

#print(sold["StateOrProvince"].value_counts(dropna=False))
#print(listings["StateOrProvince"].value_counts(dropna=False))

print("\nSOLD GEOGRAPHIC CHECKS")
print("Missing coordinates:", sold["missing_coordinates_flag"].sum())
print("Zero coordinates:", sold["zero_coordinates_flag"].sum())
print("Positive longitude:", sold["positive_longitude_flag"].sum())
print("Implausible coordinates:", sold["implausible_coordinates_flag"].sum())

print("\nLISTINGS GEOGRAPHIC CHECKS")
print("Missing coordinates:", listings["missing_coordinates_flag"].sum())
print("Zero coordinates:", listings["zero_coordinates_flag"].sum())
print("Positive longitude:", listings["positive_longitude_flag"].sum())
print("Implausible coordinates:", listings["implausible_coordinates_flag"].sum())

print("\nROW COUNTS")
print("Sold before:", sold_before)
print("Sold after:", len(sold))
print("Listings before:", listings_before)
print("Listings after:", len(listings))

print("\nSOLD DATE TYPES")
print(sold[
    [
        "CloseDate",
        "PurchaseContractDate",
        "ListingContractDate",
        "ContractStatusChangeDate"
    ]
].dtypes)

print("\nLISTINGS DATE TYPES")
print(listings[["CloseDate", "PurchaseContractDate", "ListingContractDate", "ContractStatusChangeDate"]].dtypes)


sold.to_csv("sold_cleaned.csv", index=False)
listings.to_csv("listings_cleaned.csv", index=False)
