# %% [markdown]
# # 01 - Data Cleaning: Online Retail Dataset
#
# Goal: produce a clean, transaction-level dataset that is safe to aggregate
# into RFM metrics. Every filtering decision below is documented with the
# business reason behind it (this becomes the "Action" section of the README
# later).

# %%
import pandas as pd
import numpy as np

pd.set_option("display.max_columns", None)

RAW_PATH = "../data/raw/data.csv"
PROCESSED_PATH = "../data/processed/online_retail_clean.csv"

# %% [markdown]
# ## 1. Load & first look
#
# Source: Kaggle "carrie1/ecommerce-data" (a re-hosted copy of the UCI
# Online Retail dataset). It needs `encoding="ISO-8859-1"` — the file
# contains special characters (e.g. in Description) that aren't valid UTF-8.

# %%
df = pd.read_csv(RAW_PATH, encoding="ISO-8859-1")

print("Shape:", df.shape)
df.head()

# %%
df.info()

# %%
# Quick data quality snapshot before touching anything
quality_report = pd.DataFrame({
    "n_missing": df.isnull().sum(),
    "pct_missing": (df.isnull().mean() * 100).round(2),
    "dtype": df.dtypes,
})
quality_report

# %% [markdown]
# ## 2. Handle missing `CustomerID`
#
# **Business context:** rows without a `CustomerID` are transactions we can't
# tie to a person (guest checkout, POS sale without loyalty card, data entry
# gap). Since RFM is a *customer-level* analysis, these rows carry zero
# information for segmentation — keeping them would silently inflate revenue
# totals without attaching them to any actionable customer. The standard,
# defensible move is to drop them, but we report the % lost so the business
# knows the coverage of the analysis.

# %%
n_before = len(df)
missing_custid_pct = df["CustomerID"].isnull().mean() * 100
print(f"Rows with missing CustomerID: {missing_custid_pct:.2f}%")

df = df.dropna(subset=["CustomerID"])
df["CustomerID"] = df["CustomerID"].astype(int).astype(str)

print(f"Rows dropped: {n_before - len(df)} ({(n_before - len(df)) / n_before * 100:.2f}%)")

# %% [markdown]
# ## 3. Remove duplicate rows
#
# Exact duplicate rows (same invoice, product, quantity, timestamp) are almost
# always double-counted scans/imports, not separate purchases. We do this
# early so later percentage calculations aren't skewed by dupes.

# %%
n_before = len(df)
df = df.drop_duplicates()
print(f"Duplicate rows removed: {n_before - len(df)}")

# %% [markdown]
# ## 4. Treat cancelled / returned transactions
#
# **Business context:** negative `Quantity` almost always corresponds to
# **returns / cancellations** (their `InvoiceNo` starts with the letter `C`).
# These are real business events, but they distort *purchase-behavior* RFM —
# a return isn't a purchase. We isolate them for a separate check (any
# negative quantity NOT flagged as a cancellation is a data-error candidate
# worth knowing about), then exclude all of it from the core RFM table.

# %%
cancellations = df[df["InvoiceNo"].astype(str).str.startswith("C")]
print(f"Cancellation invoices: {cancellations.shape[0]} rows "
      f"({cancellations.shape[0] / len(df) * 100:.2f}%)")

negative_qty_not_cancel = df[(df["Quantity"] < 0) & (~df["InvoiceNo"].astype(str).str.startswith("C"))]
print(f"Negative Quantity NOT flagged as cancellation (data error candidates): {negative_qty_not_cancel.shape[0]}")

# %%
n_before = len(df)
df = df[df["Quantity"] > 0]
print(f"Rows removed as returns/cancellations: {n_before - len(df)} "
      f"({(n_before - len(df)) / n_before * 100:.2f}%)")

# %% [markdown]
# ## 5. Correct `StockCode` anomalies
#
# **Business context:** genuine product codes in this dataset follow a
# consistent format (mostly 5 numeric digits). Codes like `POST`, `M`,
# `BANK CHARGES`, `DOT` are **not products** — they're postage, manual
# adjustments, bank fees, etc. Left in, they'd pollute Monetary value with
# non-product revenue and show up as fake "top products". Instead of
# hardcoding a guessed list of codes, we detect them data-drivenly: count how
# many digits each unique `StockCode` contains, and flag the codes that
# deviate from the dominant pattern.

# %%
unique_codes = df["StockCode"].astype(str).unique()
digit_counts = pd.Series(unique_codes).apply(lambda x: sum(c.isdigit() for c in x))
print("Distribution of numeric-digit counts across unique StockCodes:")
print(digit_counts.value_counts().sort_index())

# %%
# Codes with 0 or 1 numeric digits deviate from the standard ~5-digit format
anomalous_codes = [code for code, n_digits in zip(unique_codes, digit_counts) if n_digits <= 1]
print(f"Anomalous stock codes found ({len(anomalous_codes)}):")
for code in anomalous_codes:
    print(" -", code)

pct_anomalous = df["StockCode"].isin(anomalous_codes).mean() * 100
print(f"\n% of rows affected: {pct_anomalous:.2f}%")

# %%
n_before = len(df)
df = df[~df["StockCode"].isin(anomalous_codes)]
print(f"Rows removed for anomalous StockCode: {n_before - len(df)}")

# %% [markdown]
# ## 6. Clean `Description`
#
# **Business context:** descriptions are standardized to uppercase in this
# dataset — entries with lowercase text tend to be service notes (e.g.
# "Next Day Carriage", "High Resolution Image") rather than actual products,
# similarly to the StockCode anomalies above. We inspect them explicitly
# rather than assume, then drop rows that are service notes and standardize
# casing on what remains so identical products aren't split into duplicate
# labels by case differences.

# %%
lowercase_descriptions = [
    d for d in df["Description"].dropna().unique()
    if any(c.islower() for c in d)
]
print(f"Descriptions containing lowercase characters ({len(lowercase_descriptions)}):")
for d in lowercase_descriptions:
    print(" -", d)

# %%
# Inspect the list above for your specific data pull; on the standard UCI
# Online Retail extract these two are known service notes, not products.
service_related_descriptions = ["Next Day Carriage", "High Resolution Image"]
service_related_descriptions = [d for d in service_related_descriptions if d in lowercase_descriptions]

pct_service = df["Description"].isin(service_related_descriptions).mean() * 100
print(f"% of rows with service-related descriptions: {pct_service:.2f}%")

n_before = len(df)
df = df[~df["Description"].isin(service_related_descriptions)]
df["Description"] = df["Description"].str.upper()
print(f"Rows removed as service-related descriptions: {n_before - len(df)}")

# %% [markdown]
# ## 7. Treat zero / negative `UnitPrice`
#
# **Business context:** `UnitPrice <= 0` usually means data errors or free
# items given away (promo, damaged-goods write-off). These aren't genuine
# sales and would distort Monetary value if kept.

# %%
non_positive_price = df[df["UnitPrice"] <= 0]
print(f"Rows with UnitPrice <= 0: {non_positive_price.shape[0]} "
      f"({non_positive_price.shape[0] / len(df) * 100:.2f}%)")

n_before = len(df)
df = df[df["UnitPrice"] > 0]
print(f"Rows removed for non-positive UnitPrice: {n_before - len(df)}")

# %% [markdown]
# ## 8. Fix data types

# %%
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
df["InvoiceNo"] = df["InvoiceNo"].astype(str)
df["StockCode"] = df["StockCode"].astype(str)

# Derived column we'll need for Monetary in the next notebook
df["TotalPrice"] = df["Quantity"] * df["UnitPrice"]

df.dtypes

# %% [markdown]
# ## 9. Sanity check & export

# %%
df.reset_index(drop=True, inplace=True)

print("Final shape:", df.shape)
print("Date range:", df["InvoiceDate"].min(), "->", df["InvoiceDate"].max())
print("Unique customers:", df["CustomerID"].nunique())
print("Unique invoices:", df["InvoiceNo"].nunique())
assert df["CustomerID"].isnull().sum() == 0
assert (df["Quantity"] > 0).all()
assert (df["UnitPrice"] > 0).all()

df.to_csv(PROCESSED_PATH, index=False)
print(f"Saved cleaned dataset to {PROCESSED_PATH}")
