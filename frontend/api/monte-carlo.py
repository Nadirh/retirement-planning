"""
Monte Carlo Retirement Simulation API
Vercel Python Serverless Function

Uses historical bootstrap sampling from 1988-2024 market data.
"""

from http.server import BaseHTTPRequestHandler
import json
import pandas as pd
import numpy as np
from pathlib import Path

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        """Handle POST request for Monte Carlo simulation"""
        try:
            # Read request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            request_data = json.loads(post_data.decode('utf-8'))

            # Extract parameters
            years = request_data.get('years', 25)
            withdrawal_rate = request_data.get('withdrawalRate', 5.0) / 100  # Convert to decimal
            inflation_input = request_data.get('inflation')  # None or number
            run_allocation_sweep = request_data.get('allocationSweep', False)
            run_stress_test = request_data.get('historicalStressTest', False)

            # Run historical stress test, allocation sweep, or single simulation
            if run_stress_test:
                stock_allocation = request_data.get('stockAllocation', 70) / 100
                bond_allocation = request_data.get('bondAllocation', 30) / 100
                result = run_historical_stress_test(
                    years=years,
                    withdrawal_rate=withdrawal_rate,
                    stock_allocation=stock_allocation,
                    bond_allocation=bond_allocation
                )
            elif run_allocation_sweep:
                result = run_allocation_sweep_analysis(
                    years=years,
                    withdrawal_rate=withdrawal_rate,
                    inflation_input=inflation_input
                )
            else:
                stock_allocation = request_data.get('stockAllocation', 70) / 100
                bond_allocation = request_data.get('bondAllocation', 30) / 100
                result = run_monte_carlo(
                    years=years,
                    withdrawal_rate=withdrawal_rate,
                    inflation_input=inflation_input,
                    stock_allocation=stock_allocation,
                    bond_allocation=bond_allocation
                )

            # Send response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode('utf-8'))

        except Exception as e:
            # Error response
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            error_response = {
                'error': str(e),
                'message': 'Monte Carlo simulation failed'
            }
            self.wfile.write(json.dumps(error_response).encode('utf-8'))

    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()


def load_historical_data():
    """Load historical market returns from CSV"""
    # Find the CSV file (works both locally and on Vercel)
    csv_path = Path(__file__).parent.parent / 'data' / 'monthly_returns.csv'

    if not csv_path.exists():
        raise FileNotFoundError(f"Historical data not found at {csv_path}")

    df = pd.read_csv(csv_path)

    # Convert percentages to decimals
    df['SP500_Return'] = df['SP500_Total_Return'] / 100
    df['Bond_Return'] = df['Treasury_5Y_Total_Return'] / 100
    df['Inflation'] = df['Inflation_Monthly'] / 100

    return df[['SP500_Return', 'Bond_Return', 'Inflation']].values


def run_monte_carlo(years, withdrawal_rate, inflation_input, stock_allocation, bond_allocation, num_simulations=1000):
    """
    Run Monte Carlo simulation using historical bootstrap

    Parameters:
    - years: Number of years in retirement
    - withdrawal_rate: Initial withdrawal as % of portfolio (decimal, e.g., 0.05)
    - inflation_input: Fixed annual inflation rate (decimal) or None for bootstrap
    - stock_allocation: % in stocks (decimal, e.g., 0.70)
    - bond_allocation: % in bonds (decimal, e.g., 0.30)
    - num_simulations: Number of Monte Carlo iterations (default 100)

    Returns:
    - Dictionary with success rate and statistics
    """

    # Load historical data
    historical_data = load_historical_data()
    num_months = len(historical_data)

    # Convert annual inflation to monthly if provided
    if inflation_input is not None:
        monthly_inflation_fixed = (1 + inflation_input / 100) ** (1/12) - 1
        use_bootstrap_inflation = False
    else:
        monthly_inflation_fixed = 0
        use_bootstrap_inflation = True

    # Initialize results
    successes = 0
    failures = 0
    final_portfolios = []
    years_to_failure = []

    # Initial portfolio value (arbitrary - math is scale-invariant)
    initial_portfolio = 1_000_000

    # Monthly simulation
    total_months = years * 12

    # Run simulations
    for sim in range(num_simulations):
        portfolio = initial_portfolio
        monthly_withdrawal = initial_portfolio * withdrawal_rate / 12

        failed = False
        failure_month = None
        annual_inflation_multiplier = 1.0  # Track compounded inflation over the year

        for month in range(total_months):
            # Randomly select a historical month (bootstrap)
            random_month_idx = np.random.randint(0, num_months)
            stock_return, bond_return, historical_inflation = historical_data[random_month_idx]

            # Choose inflation source
            if use_bootstrap_inflation:
                inflation = historical_inflation
            else:
                inflation = monthly_inflation_fixed

            # Accumulate inflation throughout the year
            if use_bootstrap_inflation:
                annual_inflation_multiplier *= (1 + inflation)

            # Apply returns to portfolio
            stock_value = portfolio * stock_allocation * (1 + stock_return)
            bond_value = portfolio * bond_allocation * (1 + bond_return)
            portfolio = stock_value + bond_value

            # Withdraw (inflation-adjusted)
            portfolio -= monthly_withdrawal

            # Adjust withdrawal for inflation (annually)
            if (month + 1) % 12 == 0:
                # Calculate annual inflation from past 12 months
                if use_bootstrap_inflation:
                    # Use compounded inflation from bootstrapped data over the past 12 months
                    monthly_withdrawal *= annual_inflation_multiplier
                    annual_inflation_multiplier = 1.0  # Reset for next year
                else:
                    # Use fixed annual inflation rate
                    monthly_withdrawal *= (1 + inflation_input / 100)

            # Check for failure
            if portfolio <= 0:
                failed = True
                failure_month = month
                break

        # Record results
        if failed:
            failures += 1
            years_to_failure.append(failure_month / 12)
        else:
            successes += 1
            final_portfolios.append(portfolio)

    # Calculate statistics
    success_rate = (successes / num_simulations) * 100

    avg_final_portfolio = np.mean(final_portfolios) if final_portfolios else 0
    median_years_to_failure = np.median(years_to_failure) if years_to_failure else None

    return {
        'successRate': round(success_rate, 1),
        'totalSimulations': num_simulations,
        'successes': successes,
        'failures': failures,
        'details': {
            'avgFinalPortfolio': round(avg_final_portfolio, 0),
            'medianYearsToFailure': round(median_years_to_failure, 1) if median_years_to_failure else None,
            'usedBootstrap': use_bootstrap_inflation
        }
    }


def run_historical_stress_test(years, withdrawal_rate, stock_allocation, bond_allocation):
    """
    Run a deterministic historical simulation starting March 2000

    This simulates retiring at the dot-com bubble peak (March 24, 2000 was the
    historical S&P 500 peak) using actual historical data from March 2000 through
    December 2024.

    March 2000 - March 2010 saw only +2.81% total return (+0.28% annualized),
    including both the dot-com crash (2000-2002) and the financial crisis (2008-2009).

    Parameters:
    - years: Number of years in retirement (if ≤24, stop at Mar 2024; if ≥25, stop at Dec 2024)
    - withdrawal_rate: Annual withdrawal as % of portfolio (decimal)
    - stock_allocation: % in stocks (decimal)
    - bond_allocation: % in bonds (decimal)

    Returns:
    - Dictionary with year-by-year portfolio values
    """

    # Load historical data
    historical_data = load_historical_data()
    df = pd.read_csv(Path(__file__).parent.parent / 'data' / 'monthly_returns.csv')
    df['Date'] = pd.to_datetime(df['Date'])

    # Stress test configuration: March 2000 (dot-com bubble peak)
    start_year = 2000
    start_month = 3  # March
    start_day = 31
    anniversary_month = 3  # Record values every March

    start_date = pd.to_datetime(f'{start_year}-{start_month:02d}-{start_day}')
    historical_subset = df[df['Date'] >= start_date].reset_index(drop=True)

    # Determine end date based on years (24 years from March 2000 = March 2024)
    years_from_start = 2024 - start_year  # 24 years available
    if years <= years_from_start:
        # Stop at anniversary month in final year
        max_months = years * 12
        end_year = start_year + years
        end_month = anniversary_month
    else:
        # Stop at December 2024
        max_months = min(years * 12, len(historical_subset))
        end_year = 2024
        end_month = 12

    # Initial portfolio
    initial_portfolio = 1_000_000
    portfolio = initial_portfolio
    monthly_withdrawal = initial_portfolio * withdrawal_rate / 12

    # Track results by year (October to October, then final Dec 2024)
    yearly_results = []
    failed = False
    failure_year = None

    # Add starting value
    start_date_str = start_date.strftime('%B %Y')
    yearly_results.append({
        'date': start_date_str,
        'portfolioValue': initial_portfolio,
        'year': start_year
    })

    # Run simulation month by month
    for month_idx in range(min(max_months, len(historical_subset))):
        row = historical_subset.iloc[month_idx]

        # Get returns (convert percentages to decimals)
        stock_return = row['SP500_Total_Return'] / 100
        bond_return = row['Treasury_5Y_Total_Return'] / 100
        monthly_inflation = row['Inflation_Monthly'] / 100

        # Apply returns to portfolio
        stock_value = portfolio * stock_allocation * (1 + stock_return)
        bond_value = portfolio * bond_allocation * (1 + bond_return)
        portfolio = stock_value + bond_value

        # Withdraw
        portfolio -= monthly_withdrawal

        # Adjust withdrawal for inflation (annually)
        if (month_idx + 1) % 12 == 0:
            # Compound the inflation over the past 12 months
            annual_inflation = 1.0
            for i in range(12):
                past_month = historical_subset.iloc[month_idx - 11 + i]
                annual_inflation *= (1 + past_month['Inflation_Monthly'] / 100)
            monthly_withdrawal *= annual_inflation

        # Check for failure
        if portfolio <= 0:
            failed = True
            failure_year = row['Date'].year
            break

        # Record anniversary month values each year (skip the starting year)
        current_date = row['Date']
        if current_date.month == anniversary_month and current_date.year > start_year:
            yearly_results.append({
                'date': f"{current_date.strftime('%B')} {current_date.year}",
                'portfolioValue': portfolio,
                'year': current_date.year
            })

    # Add final December 2024 value if portfolio still exists and years exceed available history
    if not failed and years > years_from_start:
        # Continue to December 2024
        dec_2024_data = historical_subset[historical_subset['Date'] <= '2024-12-31']
        remaining_months = len(dec_2024_data) - max_months

        for month_idx in range(max_months, len(dec_2024_data)):
            row = historical_subset.iloc[month_idx]

            stock_return = row['SP500_Total_Return'] / 100
            bond_return = row['Treasury_5Y_Total_Return'] / 100

            stock_value = portfolio * stock_allocation * (1 + stock_return)
            bond_value = portfolio * bond_allocation * (1 + bond_return)
            portfolio = stock_value + bond_value
            portfolio -= monthly_withdrawal

            if (month_idx + 1) % 12 == 0:
                annual_inflation = 1.0
                for i in range(12):
                    past_month = historical_subset.iloc[month_idx - 11 + i]
                    annual_inflation *= (1 + past_month['Inflation_Monthly'] / 100)
                monthly_withdrawal *= annual_inflation

            if portfolio <= 0:
                failed = True
                failure_year = row['Date'].year
                break

        if not failed:
            yearly_results.append({
                'date': 'December 2024',
                'portfolioValue': portfolio,
                'year': 2024
            })

    return {
        'type': 'historicalStressTest',
        'startDate': start_date_str,
        'yearsSimulated': years,
        'initialPortfolio': initial_portfolio,
        'stockAllocation': stock_allocation * 100,
        'bondAllocation': bond_allocation * 100,
        'withdrawalRate': withdrawal_rate * 100,
        'failed': failed,
        'failureYear': failure_year,
        'yearlyResults': yearly_results
    }


def run_allocation_sweep_analysis(years, withdrawal_rate, inflation_input, num_simulations=1000):
    """
    Run Monte Carlo simulations across different stock/bond allocations

    Tests allocations from 0% stocks to 100% stocks in 10% increments
    (11 total combinations: 0/100, 10/90, 20/80, ... 100/0)

    Returns:
    - Array of results for each allocation
    - Best allocation recommendation
    """

    allocations = []
    results = []

    # Test allocations from 0% to 100% stocks in 10% increments
    for stock_pct in range(0, 101, 10):
        stock_allocation = stock_pct / 100
        bond_allocation = (100 - stock_pct) / 100

        # Run Monte Carlo for this allocation
        result = run_monte_carlo(
            years=years,
            withdrawal_rate=withdrawal_rate,
            inflation_input=inflation_input,
            stock_allocation=stock_allocation,
            bond_allocation=bond_allocation,
            num_simulations=num_simulations
        )

        allocations.append({
            'stockPercent': stock_pct,
            'bondPercent': 100 - stock_pct,
            'successRate': result['successRate'],
            'successes': result['successes'],
            'failures': result['failures'],
            'avgFinalPortfolio': result['details']['avgFinalPortfolio'],
            'medianYearsToFailure': result['details']['medianYearsToFailure']
        })

        results.append(result['successRate'])

    # Find best allocation (highest success rate)
    best_idx = results.index(max(results))
    best_allocation = allocations[best_idx]

    return {
        'type': 'allocationSweep',
        'allocations': allocations,
        'bestAllocation': {
            'stockPercent': best_allocation['stockPercent'],
            'bondPercent': best_allocation['bondPercent'],
            'successRate': best_allocation['successRate']
        },
        'totalCombinations': len(allocations),
        'simulationsPerCombination': num_simulations,
        'totalSimulations': len(allocations) * num_simulations
    }
