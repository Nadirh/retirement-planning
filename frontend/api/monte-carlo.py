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

            # Run allocation sweep or single simulation
            if run_allocation_sweep:
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


def run_monte_carlo(years, withdrawal_rate, inflation_input, stock_allocation, bond_allocation, num_simulations=100):
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


def run_allocation_sweep_analysis(years, withdrawal_rate, inflation_input, num_simulations=100):
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
