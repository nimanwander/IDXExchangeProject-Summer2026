import pandas as pd

sold = pd.read_csv("sold_week6_market_metrics.csv", low_memory=False)
numeric_columns = ["ClosePrice", "LivingArea", "DaysOnMarket"]

for col in numeric_columns:
    Q1 = sold[col].quantile(0.25)
    Q3 = sold[col].quantile(0.75)
    IQR = Q3-Q1 
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    sold[f"{col}_outlier_flag"] = ((sold[col] < lower) | (sold[col] > upper))

    print(f"\n{col}")
    print("Q1:", Q1)
    print("Q3:", Q3)
    print("IQR:", IQR)
    print("Lower bound:", lower)
    print("Upper bound:", upper)
    print("Number of outliers:", sold[f"{col}_outlier_flag"].sum())

outlier_flags = ["ClosePrice_outlier_flag", "LivingArea_outlier_flag", "DaysOnMarket_outlier_flag"]
sold_filtered = sold.loc[~sold[outlier_flags].any(axis=1)].copy()

print("\nDataset size before filtering:", len(sold))
print("Dataset size after filtering:", len(sold_filtered))
print("Rows removed:", len(sold) - len(sold_filtered))
print("\nMedians before filtering:")
print(sold[numeric_columns].median())
print("\nMedians after filtering:")
print(sold_filtered[numeric_columns].median())

sold.to_csv("sold_week7_flagged.csv", index=False)
sold_filtered.to_csv("sold_week7_filtered.csv", index=False)