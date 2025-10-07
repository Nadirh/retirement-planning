#!/usr/bin/env python3
"""
Download Historical Market Data for Monte Carlo Retirement Simulations

This script downloads 60 years (1965-2024) of monthly data for:
1. S&P 500 Total Returns (from Robert Shiller)
2. 5-Year Treasury Yields (from FRED)
3. 10-Year Treasury Yields (from FRED)
4. CPI Inflation (from FRED)

And calculates Treasury total returns using modified duration approximation.

Author: Claude Code
Date: October 7, 2025
"""

import pandas as pd
import numpy as np
import requests
from datetime import datetime
import io

# Configuration
START_DATE = '1965-01-01'
END_DATE = '2024-12-31'
DURATION_5Y = 4.25  # Modified duration for 5-year Treasury
DURATION_10Y = 8.5  # Modified duration for 10-year Treasury

# Output file
OUTPUT_CSV = 'data/historical_returns_1965_2024.csv'
METADATA_FILE = 'data/historical_returns_metadata.txt'

print("=" * 80)
print("DOWNLOADING HISTORICAL MARKET DATA (1965-2024)")
print("=" * 80)

# ============================================================================
# 1. Download S&P 500 Total Return Data from Robert Shiller
# ============================================================================
print("\n[1/4] Downloading S&P 500 Total Return data from Robert Shiller...")

shiller_url = 'http://www.econ.yale.edu/~shiller/data/ie_data.xls'

try:
    response = requests.get(shiller_url, timeout=30)
    response.raise_for_status()

    # Read Excel file (Shiller's data starts at row 7)
    # Try xlrd engine first for .xls format
    try:
        shiller_df = pd.read_excel(io.BytesIO(response.content), sheet_name='Data', engine='xlrd', skiprows=7, nrows=2000)
    except:
        # Fallback to openpyxl for .xlsx
        shiller_df = pd.read_excel(io.BytesIO(response.content), engine='openpyxl', skiprows=7, nrows=2000)

    # Get actual column names from first row
    print(f"  Shiller columns ({len(shiller_df.columns)}): {list(shiller_df.columns[:5])}...")

    # Use the actual column names (first 3 columns are Date, Price, Dividend)
    date_col = shiller_df.columns[0]
    price_col = shiller_df.columns[1]
    dividend_col = shiller_df.columns[2]

    # Keep only necessary columns
    shiller_df = shiller_df[[date_col, price_col, dividend_col]].copy()
    shiller_df.columns = ['Date', 'SP500_Price', 'Dividend']

    # Convert Date to datetime (format: YYYY.MM)
    shiller_df['Date'] = pd.to_datetime(shiller_df['Date'].astype(str).str.replace('.', '-'), format='%Y-%m', errors='coerce')

    # Filter to our date range
    shiller_df = shiller_df[(shiller_df['Date'] >= START_DATE) & (shiller_df['Date'] <= END_DATE)]

    # Calculate monthly returns from price and dividend data
    # Total Return = (Price[t] + Dividend[t]) / Price[t-1] - 1
    shiller_df = shiller_df.sort_values('Date')
    shiller_df['SP500_Monthly_Return'] = (
        (shiller_df['SP500_Price'] + shiller_df['Dividend']) /
        shiller_df['SP500_Price'].shift(1) - 1
    )

    # Keep only Date and Return
    sp500_data = shiller_df[['Date', 'SP500_Monthly_Return']].copy()
    sp500_data = sp500_data.dropna()

    print(f"✓ Downloaded {len(sp500_data)} months of S&P 500 data")
    print(f"  Date range: {sp500_data['Date'].min()} to {sp500_data['Date'].max()}")

except Exception as e:
    print(f"✗ Error downloading Shiller data: {e}")
    print("  Please download manually from http://www.econ.yale.edu/~shiller/data.htm")
    sp500_data = None

# ============================================================================
# 2. Download 5-Year Treasury Yield from FRED
# ============================================================================
print("\n[2/4] Downloading 5-Year Treasury yield data from FRED...")

fred_5y_url = 'https://fred.stlouisfed.org/graph/fredgraph.csv?id=DGS5'

try:
    response = requests.get(fred_5y_url, timeout=30)
    response.raise_for_status()

    treasury_5y_df = pd.read_csv(io.StringIO(response.text))
    treasury_5y_df.columns = ['Date', 'DGS5']
    treasury_5y_df['Date'] = pd.to_datetime(treasury_5y_df['Date'])

    # Convert to numeric, handle missing values
    treasury_5y_df['DGS5'] = pd.to_numeric(treasury_5y_df['DGS5'], errors='coerce')

    # Get end-of-month values
    treasury_5y_df = treasury_5y_df.set_index('Date')
    treasury_5y_monthly = treasury_5y_df.resample('ME').last()

    # Forward fill missing values (holidays/weekends)
    treasury_5y_monthly['DGS5'] = treasury_5y_monthly['DGS5'].ffill()

    # Filter to date range
    treasury_5y_monthly = treasury_5y_monthly[
        (treasury_5y_monthly.index >= START_DATE) &
        (treasury_5y_monthly.index <= END_DATE)
    ]

    print(f"✓ Downloaded {len(treasury_5y_monthly)} months of 5-Year Treasury yield data")
    print(f"  Date range: {treasury_5y_monthly.index.min()} to {treasury_5y_monthly.index.max()}")

except Exception as e:
    print(f"✗ Error downloading 5-Year Treasury data: {e}")
    treasury_5y_monthly = None

# ============================================================================
# 3. Download 10-Year Treasury Yield from FRED
# ============================================================================
print("\n[3/4] Downloading 10-Year Treasury yield data from FRED...")

fred_10y_url = 'https://fred.stlouisfed.org/graph/fredgraph.csv?id=DGS10'

try:
    response = requests.get(fred_10y_url, timeout=30)
    response.raise_for_status()

    treasury_10y_df = pd.read_csv(io.StringIO(response.text))
    treasury_10y_df.columns = ['Date', 'DGS10']
    treasury_10y_df['Date'] = pd.to_datetime(treasury_10y_df['Date'])

    # Convert to numeric, handle missing values
    treasury_10y_df['DGS10'] = pd.to_numeric(treasury_10y_df['DGS10'], errors='coerce')

    # Get end-of-month values
    treasury_10y_df = treasury_10y_df.set_index('Date')
    treasury_10y_monthly = treasury_10y_df.resample('ME').last()

    # Forward fill missing values
    treasury_10y_monthly['DGS10'] = treasury_10y_monthly['DGS10'].ffill()

    # Filter to date range
    treasury_10y_monthly = treasury_10y_monthly[
        (treasury_10y_monthly.index >= START_DATE) &
        (treasury_10y_monthly.index <= END_DATE)
    ]

    print(f"✓ Downloaded {len(treasury_10y_monthly)} months of 10-Year Treasury yield data")
    print(f"  Date range: {treasury_10y_monthly.index.min()} to {treasury_10y_monthly.index.max()}")

except Exception as e:
    print(f"✗ Error downloading 10-Year Treasury data: {e}")
    treasury_10y_monthly = None

# ============================================================================
# 4. Download CPI Inflation from FRED
# ============================================================================
print("\n[4/4] Downloading CPI inflation data from FRED...")

fred_cpi_url = 'https://fred.stlouisfed.org/graph/fredgraph.csv?id=CPIAUCSL'

try:
    response = requests.get(fred_cpi_url, timeout=30)
    response.raise_for_status()

    cpi_df = pd.read_csv(io.StringIO(response.text))
    cpi_df.columns = ['Date', 'CPI']
    cpi_df['Date'] = pd.to_datetime(cpi_df['Date'])
    cpi_df = cpi_df.set_index('Date')

    # Convert to numeric
    cpi_df['CPI'] = pd.to_numeric(cpi_df['CPI'], errors='coerce')

    # Calculate month-over-month inflation
    cpi_df['CPI_Monthly_Inflation'] = cpi_df['CPI'].pct_change()

    # Calculate 12-month (annual) inflation
    cpi_df['CPI_Annual_Inflation'] = cpi_df['CPI'].pct_change(periods=12)

    # Filter to date range
    cpi_df = cpi_df[
        (cpi_df.index >= START_DATE) &
        (cpi_df.index <= END_DATE)
    ]

    print(f"✓ Downloaded {len(cpi_df)} months of CPI data")
    print(f"  Date range: {cpi_df.index.min()} to {cpi_df.index.max()}")

except Exception as e:
    print(f"✗ Error downloading CPI data: {e}")
    cpi_df = None

# ============================================================================
# 5. Calculate Treasury Total Returns
# ============================================================================
print("\n" + "=" * 80)
print("CALCULATING TREASURY TOTAL RETURNS USING DURATION APPROXIMATION")
print("=" * 80)

if treasury_5y_monthly is not None:
    print("\n[5/6] Calculating 5-Year Treasury total returns...")

    # Convert yields from percentage to decimal
    treasury_5y_monthly['Yield_Decimal'] = treasury_5y_monthly['DGS5'] / 100

    # Calculate yield change
    treasury_5y_monthly['Yield_Change'] = treasury_5y_monthly['Yield_Decimal'].diff()

    # Calculate total return using duration approximation
    # Total Return = (Yield / 12) - (Duration × Yield_Change)
    treasury_5y_monthly['Treasury_5Y_Return'] = (
        (treasury_5y_monthly['Yield_Decimal'] / 12) -
        (DURATION_5Y * treasury_5y_monthly['Yield_Change'])
    )

    print(f"✓ Calculated 5-Year Treasury total returns")
    print(f"  Duration used: {DURATION_5Y} years")
    print(f"  Average monthly return: {treasury_5y_monthly['Treasury_5Y_Return'].mean():.4%}")
    print(f"  Annualized return: {(1 + treasury_5y_monthly['Treasury_5Y_Return'].mean())**12 - 1:.2%}")

if treasury_10y_monthly is not None:
    print("\n[6/6] Calculating 10-Year Treasury total returns...")

    # Convert yields from percentage to decimal
    treasury_10y_monthly['Yield_Decimal'] = treasury_10y_monthly['DGS10'] / 100

    # Calculate yield change
    treasury_10y_monthly['Yield_Change'] = treasury_10y_monthly['Yield_Decimal'].diff()

    # Calculate total return using duration approximation
    treasury_10y_monthly['Treasury_10Y_Return'] = (
        (treasury_10y_monthly['Yield_Decimal'] / 12) -
        (DURATION_10Y * treasury_10y_monthly['Yield_Change'])
    )

    print(f"✓ Calculated 10-Year Treasury total returns")
    print(f"  Duration used: {DURATION_10Y} years")
    print(f"  Average monthly return: {treasury_10y_monthly['Treasury_10Y_Return'].mean():.4%}")
    print(f"  Annualized return: {(1 + treasury_10y_monthly['Treasury_10Y_Return'].mean())**12 - 1:.2%}")

# ============================================================================
# 6. Merge All Data and Create CSV
# ============================================================================
print("\n" + "=" * 80)
print("MERGING DATA AND CREATING CSV FILE")
print("=" * 80)

# Merge all dataframes
if sp500_data is not None:
    sp500_data = sp500_data.set_index('Date')

# Combine all data
combined_df = pd.DataFrame(index=pd.date_range(start=START_DATE, end=END_DATE, freq='ME'))

if sp500_data is not None:
    combined_df = combined_df.join(sp500_data[['SP500_Monthly_Return']], how='left')

if treasury_5y_monthly is not None:
    combined_df = combined_df.join(treasury_5y_monthly[['Treasury_5Y_Return']], how='left')

if treasury_10y_monthly is not None:
    combined_df = combined_df.join(treasury_10y_monthly[['Treasury_10Y_Return']], how='left')

if cpi_df is not None:
    combined_df = combined_df.join(cpi_df[['CPI_Monthly_Inflation', 'CPI_Annual_Inflation']], how='left')

# Reset index to make Date a column
combined_df = combined_df.reset_index()

# Rename columns properly
rename_dict = {
    'index': 'Date',
    'SP500_Monthly_Return': 'SP500_Return',
    'CPI_Monthly_Inflation': 'CPI_Monthly',
    'CPI_Annual_Inflation': 'CPI_Annual'
}
combined_df = combined_df.rename(columns=rename_dict)

# Remove any rows with all NaN values
subset_cols = [col for col in ['SP500_Return', 'Treasury_5Y_Return', 'Treasury_10Y_Return', 'CPI_Monthly']
               if col in combined_df.columns]
if subset_cols:
    combined_df = combined_df.dropna(how='all', subset=subset_cols)

# Save to CSV
import os
os.makedirs('data', exist_ok=True)

combined_df.to_csv(OUTPUT_CSV, index=False, float_format='%.6f')

print(f"\n✓ Created CSV file: {OUTPUT_CSV}")
print(f"  Total months: {len(combined_df)}")
print(f"  Date range: {combined_df['Date'].min()} to {combined_df['Date'].max()}")
print(f"  Columns: {', '.join(combined_df.columns)}")

# ============================================================================
# 7. Create Metadata File
# ============================================================================
print(f"\n✓ Creating metadata file: {METADATA_FILE}")

metadata = f"""Historical Market Data - Metadata
{'=' * 80}

Data Sources:
-------------
1. S&P 500 Total Returns
   - Source: Robert Shiller, Yale University
   - URL: http://www.econ.yale.edu/~shiller/data.htm
   - Calculation: (Price[t] + Dividend[t]) / Price[t-1] - 1
   - Coverage: {sp500_data.index.min() if sp500_data is not None else 'N/A'} to {sp500_data.index.max() if sp500_data is not None else 'N/A'}

2. 5-Year Treasury Total Returns
   - Source: FRED (Federal Reserve Economic Data)
   - URL: https://fred.stlouisfed.org/series/DGS5
   - Series: DGS5 (5-Year Treasury Constant Maturity Rate)
   - Calculation Method: Modified Duration Approximation
   - Modified Duration: {DURATION_5Y} years
   - Formula: Total Return = (Yield/12) - (Duration × ΔYield)
   - Coverage: {treasury_5y_monthly.index.min() if treasury_5y_monthly is not None else 'N/A'} to {treasury_5y_monthly.index.max() if treasury_5y_monthly is not None else 'N/A'}

3. 10-Year Treasury Total Returns
   - Source: FRED (Federal Reserve Economic Data)
   - URL: https://fred.stlouisfed.org/series/DGS10
   - Series: DGS10 (10-Year Treasury Constant Maturity Rate)
   - Calculation Method: Modified Duration Approximation
   - Modified Duration: {DURATION_10Y} years
   - Formula: Total Return = (Yield/12) - (Duration × ΔYield)
   - Coverage: {treasury_10y_monthly.index.min() if treasury_10y_monthly is not None else 'N/A'} to {treasury_10y_monthly.index.max() if treasury_10y_monthly is not None else 'N/A'}

4. CPI Inflation
   - Source: FRED (Federal Reserve Economic Data)
   - URL: https://fred.stlouisfed.org/series/CPIAUCSL
   - Series: CPIAUCSL (Consumer Price Index for All Urban Consumers)
   - CPI_Monthly: Month-over-month inflation rate
   - CPI_Annual: 12-month (year-over-year) inflation rate
   - Coverage: {cpi_df.index.min() if cpi_df is not None else 'N/A'} to {cpi_df.index.max() if cpi_df is not None else 'N/A'}

Bond Math Methodology:
----------------------
Treasury yields are converted to total returns using the modified duration approximation:

Total Return = Coupon Income + Capital Gain/Loss
             = (Yield / 12) - (Modified Duration × Change in Yield)

This is the industry-standard approach when actual bond prices are unavailable.

Duration Values Used:
- 5-Year Treasury: {DURATION_5Y} years (based on CME Group data and academic research)
- 10-Year Treasury: {DURATION_10Y} years (based on CME Group data and academic research)

Validation:
-----------
10-Year Treasury returns will be cross-validated against Aswath Damodaran's annual data:
- Source: https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/histretSP.html
- Acceptable variance: ±0.2% annually

Data Quality Notes:
-------------------
- Missing values in FRED data are forward-filled from previous valid observation
- End-of-month values are used for all monthly calculations
- First month of each series may be NaN due to diff() calculations

Output File Format:
-------------------
Filename: {OUTPUT_CSV}
Columns:
  - Date: End of month date (YYYY-MM-DD)
  - SP500_Return: Monthly total return (decimal, e.g., 0.05 = 5%)
  - Treasury_5Y_Return: Monthly total return (decimal)
  - Treasury_10Y_Return: Monthly total return (decimal)
  - CPI_Monthly: Month-over-month inflation (decimal)
  - CPI_Annual: 12-month inflation rate (decimal)

Date Range: {START_DATE} to {END_DATE}
Total Months: {len(combined_df)}

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Script: download_historical_data.py
"""

with open(METADATA_FILE, 'w') as f:
    f.write(metadata)

print("\n" + "=" * 80)
print("DOWNLOAD COMPLETE!")
print("=" * 80)
print(f"\nFiles created:")
print(f"  1. {OUTPUT_CSV}")
print(f"  2. {METADATA_FILE}")
print(f"\nNext steps:")
print(f"  1. Review the CSV file for data quality")
print(f"  2. Run validation checks against Damodaran data")
print(f"  3. Perform sanity checks on historical events")
print("=" * 80)
