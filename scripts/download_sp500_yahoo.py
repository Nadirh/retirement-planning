#!/usr/bin/env python3
"""
Download S&P 500 Total Return data from Yahoo Finance
Fills in the gap for 1965-2024 monthly data
"""

import pandas as pd
import requests
import time
from datetime import datetime

print("=" * 80)
print("DOWNLOADING S&P 500 DATA FROM YAHOO FINANCE")
print("=" * 80)

# Yahoo Finance uses Unix timestamps
# January 1, 1965 = -157766400
# December 31, 2024 = 1735689600

start_timestamp = -157766400  # Jan 1, 1965
end_timestamp = int(datetime(2024, 12, 31).timestamp())

# Try S&P 500 Total Return Index first
ticker = "^SP500TR"
print(f"\n[1/2] Trying {ticker} (S&P 500 Total Return Index)...")

url = f"https://query1.finance.yahoo.com/v7/finance/download/{ticker}"
params = {
    'period1': start_timestamp,
    'period2': end_timestamp,
    'interval': '1mo',
    'events': 'history',
    'includeAdjustedClose': 'true'
}

try:
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()

    # Parse CSV
    from io import StringIO
    df = pd.read_csv(StringIO(response.text))

    print(f"✓ Downloaded {len(df)} months of data")
    print(f"  Date range: {df['Date'].min()} to {df['Date'].max()}")
    print(f"  Columns: {list(df.columns)}")

    # Convert to monthly returns
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date')

    # Calculate monthly returns using adjusted close
    df['SP500_Return'] = df['Close'].pct_change()

    # Keep only Date and Return
    sp500_data = df[['Date', 'SP500_Return']].copy()
    sp500_data = sp500_data.dropna()

    print(f"\n✓ Calculated monthly returns")
    print(f"  Average monthly return: {sp500_data['SP500_Return'].mean():.4%}")
    print(f"  Annualized return: {(1 + sp500_data['SP500_Return'].mean())**12 - 1:.2%}")

    # Save to CSV
    sp500_data.to_csv('data/sp500_yahoo_finance.csv', index=False, float_format='%.6f')
    print(f"\n✓ Saved to data/sp500_yahoo_finance.csv")

except Exception as e:
    print(f"✗ Error with {ticker}: {e}")
    print("\nTrying fallback: ^GSPC (S&P 500 Price Index)...")

    # Fallback to regular S&P 500 (price only, not total return)
    ticker = "^GSPC"
    url = f"https://query1.finance.yahoo.com/v7/finance/download/{ticker}"

    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()

        df = pd.read_csv(StringIO(response.text))

        print(f"✓ Downloaded {len(df)} months of S&P 500 price data")
        print(f"  Date range: {df['Date'].min()} to {df['Date'].max()}")
        print(f"  ⚠️  Note: This is PRICE ONLY (no dividends)")

        df['Date'] = pd.to_datetime(df['Date'])
        df = df.sort_values('Date')
        df['SP500_Price_Return'] = df['Close'].pct_change()

        sp500_data = df[['Date', 'SP500_Price_Return']].copy()
        sp500_data = sp500_data.dropna()

        sp500_data.to_csv('data/sp500_yahoo_finance_price_only.csv', index=False, float_format='%.6f')
        print(f"\n✓ Saved to data/sp500_yahoo_finance_price_only.csv")
        print(f"  ⚠️  You'll need to add dividends separately for total return")

    except Exception as e2:
        print(f"✗ Both attempts failed: {e2}")
        print("\n" + "=" * 80)
        print("MANUAL DOWNLOAD REQUIRED")
        print("=" * 80)
        print("\nPlease download manually from:")
        print("1. Yahoo Finance: https://finance.yahoo.com/quote/%5ESP500TR/history")
        print("2. Or use your paid Yahoo Finance account")
        print("3. Download as CSV for date range 1965-01-01 to 2024-12-31")
        print("4. Save to: data/sp500_manual.csv")

print("\n" + "=" * 80)
print("COMPLETE")
print("=" * 80)
