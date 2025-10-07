#!/usr/bin/env python3
"""Test script for allocation sweep"""

import sys
import os
from pathlib import Path

# Change to frontend directory
os.chdir('/workspaces/retirement-planning/frontend')

# Load the module directly
import importlib.util
spec = importlib.util.spec_from_file_location("monte_carlo", "/workspaces/retirement-planning/frontend/api/monte-carlo.py")
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)

import json

# Run allocation sweep
print("Running allocation sweep with 100 Monte Carlo iterations per allocation...")
print("Testing 11 allocations from 0% stocks to 100% stocks...")
print()

result = mc.run_allocation_sweep_analysis(
    years=25,
    withdrawal_rate=0.05,
    inflation_input=3.0,
    num_simulations=100
)

print(f"Total simulations: {result['totalSimulations']}")
print(f"Best allocation: {result['bestAllocation']['stockPercent']}% stocks / {result['bestAllocation']['bondPercent']}% bonds")
print(f"Best success rate: {result['bestAllocation']['successRate']}%")
print()
print("=" * 60)
print("All Allocations:")
print("=" * 60)
print(f"{'Stocks':>6} {'Bonds':>6} {'Success Rate':>12} {'Successes':>10} {'Failures':>8}")
print("-" * 60)
for alloc in result['allocations']:
    print(f"{alloc['stockPercent']:>6}% {alloc['bondPercent']:>6}% {alloc['successRate']:>11.1f}% {alloc['successes']:>10} {alloc['failures']:>8}")
