# Sequence of Returns Risk Analysis
## Historical Analysis of S&P 500 Returns (1988-2024)

---

## Executive Summary

**Worst time to retire**: **March 2004**
- 5-year total return: **-29.05%**
- Annualized return: **-6.63%**

**Best time to retire**: **January 1995**
- 5-year total return: **+251.11%**
- Annualized return: **+28.56%**

**Difference**: **280.17 percentage points**

This massive difference perfectly illustrates **sequence of returns risk** - the critical importance of WHEN you retire, not just what your average returns are over time.

---

## Top 10 Worst 5-Year Periods to Retire

| Rank | Start Date | End Date | Total Return | Annualized | Context |
|------|------------|----------|--------------|------------|---------|
| 1 | March 2004 | Feb 2009 | -29.05% | -6.63% | 2008 Financial Crisis |
| 2 | April 2004 | Mar 2009 | -21.66% | -4.76% | 2008 Financial Crisis |
| 3 | Feb 2004 | Jan 2009 | -19.50% | -4.24% | 2008 Financial Crisis |
| 4 | April 1998 | Mar 2003 | -17.47% | -3.77% | Dot-com bubble burst |
| 5 | April 2000 | Mar 2005 | -14.84% | -3.16% | Dot-com bubble burst |
| 6 | March 1998 | Feb 2003 | -14.08% | -2.99% | Dot-com bubble burst |
| 7 | May 2000 | Apr 2005 | -13.86% | -2.94% | Dot-com bubble burst |
| 8 | Sept 2000 | Aug 2005 | -12.83% | -2.71% | Dot-com bubble burst |
| 9 | May 2004 | Apr 2009 | -12.79% | -2.70% | 2008 Financial Crisis |
| 10 | May 1998 | Apr 2003 | -11.56% | -2.43% | Dot-com bubble burst |

**Key Pattern**: All worst periods involve either:
- The 2008 Financial Crisis (Great Recession)
- The 2000-2002 Dot-com bubble burst

---

## Detailed Case Study: March 2004 Retiree

### Scenario
- **Retirement date**: March 2004
- **Starting portfolio**: $1,000,000
- **Allocation**: 100% S&P 500
- **Withdrawal rate**: 4% annually ($3,333/month)
- **Inflation adjustment**: None (for simplicity)

### Year-by-Year Results

| Year | Annual Return | Portfolio Value (End of Year) |
|------|---------------|-------------------------------|
| 2004 | +7.39% | $1,037,984 |
| 2005 | +4.91% | $1,047,238 |
| 2006 | +15.79% | $1,169,157 |
| 2007 | +5.49% | $1,193,258 |
| **2008** | **-37.00%** | **$720,934** |
| 2009 (Jan-Feb) | -18.18% | **$583,562** |

### The Devastating Impact

**After 5 years**:
- Starting portfolio: $1,000,000
- Ending portfolio: **$583,562**
- **Total loss: $416,438 (-41.6%)**
- Total withdrawals: $200,000

**Worst month**: October 2008 (-16.80% single month)
- Portfolio dropped from $936,195 to $775,627 in one month
- This is AFTER already being down significantly

### Why This Was So Devastating

1. **Early losses compound**: The portfolio was already weakened before the crisis
2. **Withdrawals during declines**: Taking out $3,333/month while losing money
3. **No time to recover**: Only 5 years into retirement when crisis hit
4. **Sequence matters**: -37% in year 5 is much worse than -37% in year 20

---

## Comparison: Best Case Scenario (January 1995 Retiree)

### Same Scenario, Different Timing
- **Retirement date**: January 1995
- **Starting portfolio**: $1,000,000
- **Same allocation**: 100% S&P 500
- **Same withdrawal**: 4% annually ($3,333/month)

### Results After 5 Years
- Starting portfolio: $1,000,000
- Ending portfolio: **$3,131,627**
- **Total gain: $2,131,627 (+213.2%)**
- Total withdrawals: $200,000

### The Staggering Difference

| Metric | March 2004 Retiree | January 1995 Retiree | Difference |
|--------|-------------------|----------------------|------------|
| Ending Portfolio | $583,562 | $3,131,627 | **$2,548,065** |
| 5-Year Return | -29.05% | +251.11% | **280.17 pp** |
| Financial Security | Severely impaired | Excellent | - |

**Same withdrawal rate. Same allocation. Different timing. Completely different outcomes.**

---

## Key Insights for Retirement Planning

### 1. **Sequence of Returns Risk is Real**
The ORDER of returns matters more than the average, especially early in retirement.

### 2. **First 5-10 Years Are Critical**
Early losses combined with withdrawals can permanently impair a portfolio's ability to recover.

### 3. **2008 Financial Crisis Was Brutal**
- S&P 500 dropped -37% in 2008 alone
- Followed by another -18% in early 2009
- Total peak-to-trough decline: ~57%

### 4. **Asset Allocation Matters**
- Our analysis shows 100% stocks for illustration
- Real retirees should diversify (stocks + bonds)
- Bonds provide stability during stock market crashes

### 5. **Dynamic Withdrawal Strategies Help**
- Fixed 4% during crisis = depleting portfolio
- Flexible withdrawals can preserve capital
- Consider reducing spending during bear markets

---

## Application to Monte Carlo Simulations

### Why We Use Historical Bootstrap
1. **Captures real market behavior**: Includes actual crashes like 2008
2. **Preserves correlations**: Stocks, bonds, and inflation move together realistically
3. **Shows realistic risk**: Not just theoretical standard deviations

### Why We Test Multiple Allocations
- 100% stocks: High returns, high sequence risk (as shown above)
- Balanced allocations: Trade some upside for stability
- Our tool finds the optimal allocation for YOUR specific parameters

### Why 1,000 Simulations Matter
- Each simulation randomly samples from history
- Some get lucky (retire in 1995)
- Some get unlucky (retire in 2004)
- 1,000 iterations show the full range of possibilities

---

## Historical Context

### 2008 Financial Crisis (The Great Recession)
- **Trigger**: Subprime mortgage crisis, Lehman Brothers collapse
- **Duration**: Dec 2007 - June 2009 (18 months)
- **S&P 500 decline**: -57% peak-to-trough
- **Recovery**: Took until March 2013 to reach pre-crisis levels

### Dot-com Bubble Burst (2000-2002)
- **Trigger**: Internet stock overvaluation
- **Duration**: March 2000 - October 2002 (30 months)
- **NASDAQ decline**: -78% peak-to-trough
- **S&P 500 decline**: -49% peak-to-trough
- **Recovery**: Took until 2007 to reach pre-crash levels

---

## Conclusion

**The evidence is clear**: When you retire matters enormously.

Someone who retired in March 2004 with $1 million would have seen their portfolio cut nearly in half within 5 years, despite:
- Following the "4% rule"
- Having experienced positive returns in 3 of the 5 years
- Making no mistakes

Someone who retired just 9 years earlier (January 1995) would have **tripled** their money in the same timeframe, with the same strategy.

This is why:
1. **Asset allocation is critical** - diversification reduces sequence risk
2. **Flexibility matters** - be prepared to adjust spending in down markets
3. **Testing multiple scenarios** - our Monte Carlo tool simulates thousands of possible market sequences
4. **Planning is essential** - understand the risks before you retire

---

## Data Source
- **S&P 500 Total Returns**: Monthly data from February 1988 to December 2024
- **Source**: Historical market data, including dividends reinvested
- **Adjustments**: None - raw historical returns used

---

*Generated by Claude Code for Longevity Planning retirement calculator*
*Analysis date: October 7, 2025*
