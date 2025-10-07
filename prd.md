DIY Retirement Planner — Business‑Only PRD (Overview for Vibe Coding AI)
Purpose: Provide a clean, business‑only overview to guide vibe coding. Consolidates and de‑duplicates all inputs you provided. Technical implementation details are intentionally out of scope.

1) Product Summary
A web app for DIY pre‑retirees and retirees to plan decumulation, choose a stocks/bonds allocation, and select a withdrawal approach that maximizes the probability of not running out of money by a user‑defined horizon.
Core promise: "See (and improve) your odds of not running out."


Primary optimization surface: % in Stocks (1 − % in Bonds), and Year‑1 withdrawal rate (inflation‑adjusted thereafter).


Tone: Transparent, educational, practical; not advisory.



2) Users & Market Opportunity
Primary audience
DIY Investors with material savings (e.g., $200K–$2M+) seeking control and clarity.


Advisor skeptics / second‑opinion seekers who want to sanity‑check recommendations.


Tech‑savvy pre‑retirees (50–70) & retirees comfortable with digital tools.


Context & signals
DIY "success‑probability" calculators (Monte Carlo) are mainstream; many compare scenarios side‑by‑side. Our edge: retiree‑friendly UX, stock/bond focus first, plus guardrails/IRMAA/SS timing in one place.


Advisor capacity constraints (aging advisor base) imply more self‑directed planning and second opinions.


Pain points (what they struggle with)
Sequence‑of‑returns risk is poorly understood; early bad years can dominate outcomes.


Social Security timing (62 vs FRA vs 70) materially changes required withdrawals.


IRMAA blind spots: crossing Medicare income thresholds can add $1,000+/yr costs; most tools ignore this.


Tax‑inefficient withdrawals: order of accounts and Roth conversions during "gap years" before RMDs.



3) Problem / Jobs‑to‑Be‑Done (JTBD)
JTBD‑1: "Help me pick a stock/bond mix and year‑1 withdrawal rate that maximizes my survival probability to year N."


JTBD‑2: "Let me stress‑test against early bear markets, high inflation, and longevity risk."


JTBD‑3: "Show me how Social Security timing and healthcare/IRMAA change my odds and cash‑flows."


JTBD‑4: "Compare a few candidate plans and share a clear report with my spouse or advisor."



4) Value Proposition & Positioning
Core value proposition: "The retirement planning tool your financial advisor doesn't want you to have."
Three pillars
Transparency: show the math and assumptions; no black boxes.


Sophistication: portfolio‑survival probabilities with robust scenario analysis.


Practicality: actionable levers (allocation, withdrawal rate, SS timing, healthcare assumptions).


YES positioning as
Advisor sanity check (verify assumptions),


Scenario stress‑tester (sequence risk, inflation spikes),


Optimization engine (allocation & withdrawals),


Ongoing support (re‑run annually as conditions change).


Messaging examples
DIY: "Run the same style of simulations advisors use. Can your 60/40 truly support a 4% withdrawal?"


Advisor clients: "Your advisor suggests 70/30 @ 3.5%. Stress‑test: What if you retire into a bear market?"


Pre‑retirees: "Don't let early bad years derail retirement. Model sequence risk and optimize allocation."



5) Scope — Version 1 (Business Requirements)
5.1 Inputs
Required: Age, portfolio size, year‑1 withdrawal % (or dollar need), planning horizon (years), baseline inflation.


Asset assumptions: Expected returns/volatilities for Stocks and Bonds (pre‑set with editable historical ranges); option to run Monte Carlo and simple back‑tests.


Optional toggles: Social Security inclusion (simple estimator), Healthcare line item with IRMAA awareness.


5.2 Outputs
Primary metric: Probability of survival to year N for each (stocks %, withdrawal %) pair.


Recommendation: "Best‑fit" allocation and withdrawal combo with plain‑English rationale & downside caveats.


Sensitivity: quick cards to vary inflation (±1–2 pp), reduce returns, or simulate early‑bear sequence.


Plan comparison: save/compare up to 3 scenarios (e.g., 40/60 @ 3.5%, 50/50 @ 3.7%, 60/40 @ 4.0%).


Shareable report: 1‑page "Retirement Plan Snapshot" PDF.


5.3 Feature Epics (V1)
Setup & Quick Start


2‑minute intake → instant baseline result.


Clear display: Success Probability, Median Ending Balance, 10th percentile, Years to depletion (if any), distribution chart.


Allocation Optimizer


Goal: find stock/bond mix that maximizes survival probability for user's horizon & withdrawal.


Business constraints: min 20% Bonds, max 80% Stocks; optional user bounds.


Output copy: "Recommends 65/35; improves success from 82% → 89%; note worse‑case trade‑offs."


Stress‑Testing (Sequence & Macros)


Presets: Early Bear at retirement, Inflation spike, Longevity stretch.


Show delta to success rate and required spending cuts in tough scenarios; propose cash‑reserve heuristic.


Social Security (SS) Timing — What‑If


Compare claiming at 62 / FRA / 70; show portfolio withdrawal relief and success‑probability lift.


Simple breakeven insight ("Live past X → claiming later pays more").


Healthcare & IRMAA Awareness


IRMAA explainer: IRMAA = income‑based surcharges on Medicare Part B/D, using MAGI from two years prior; life‑change events can justify appeals.


Inputs: healthcare spend assumptions; IRMAA threshold banners when projected income crosses brackets.


Compare Plans & Reporting


Save up to 3 plans; side‑by‑side table for success %, median bequest, worst‑decile spend cuts.


Export 1‑page PDF for spouse/advisor.


Non‑Goals for V1
Detailed tax engine, advisor integrations, or more than 2 core asset classes.



6) V1.1 – V2 Enhancements
Tax‑Aware Withdrawals & Roth Conversions (⭐ High Value)


Account types: Taxable, Traditional (IRA/401k), Roth.


Withdrawal Order Optimizer with simple tax/IRMAA awareness; "gap years" Roth conversions before RMDs; bracket‑filling heuristics.


Before/after IRMAA effect and warnings.


"Blend with Guarantees" Track


Scenario compare: 100% market vs partial annuity floor (e.g., SPIA ladder) or TIPS ladder as bond alternative.


Trade‑offs: failure rate vs bequest; security vs upside.


Expanded Asset Classes (Phase 3)


3A Traditional: Cash/MM, International Stocks, REITs, Commodities/Gold.


3B Alternatives/Income: Annuities, Reverse Mortgages (as back‑stop), Real Estate, Crypto (advanced users).


Longevity Tools


SSA‑informed sliders, joint longevity for couples, and dynamic planning horizon that updates with age.


Alerts & Recommendations


IRMAA warning when projected MAGI crosses a bracket.


Tax optimization nudges (Roth conversions in low‑income years).


Rebalancing prompts when drift exceeds threshold.


Professional/Advisor Features


Multi‑household management, white‑label PDFs, export to Excel/CSV, (future) API access.



7) Unique Differentiators
Integrated IRMAA awareness, not just healthcare line items.


Sequence‑of‑returns visualization tightly coupled to allocation & withdrawal decisions.


Simple but powerful tax‑aware decumulation heuristics (upgrade path).


Clear, auditable methodology and explainers.



8) Pricing & Packaging
Free — "Basic Planning"
1,000 simulations; 2 asset classes; single scenario; basic SS; 1‑page PDF.


No optimizer, no IRMAA, no tax‑aware features; one saved scenario max.


Paid — "Advanced Planning" ($99/yr or $12/mo)
Everything in Free plus: 10,000 simulations; optimizer; 5 saved scenarios; IRMAA calculator & warnings; stress‑testing suite; tax‑aware withdrawal optimizer; Roth conversion calculator; sequence‑risk analysis; detailed PDFs; priority support.


Premium — "Professional" ($249/yr)
Everything in Advanced plus: multi‑household, white‑label reports, advanced assets (annuities, reverse mortgages, crypto, real estate), Excel export, phone/email support, (future) API.


Alternative: Lifetime Pro $299 one‑time (for subscription‑averse users).
Upgrade triggers (UX nudges)
After 3 free sims: "Unlock optimization to improve your success rate."


On IRMAA risk: "⚠️ See how to avoid surcharges — upgrade to Advanced."


When saving a second scenario: "Compare strategies side‑by‑side — upgrade."



9) User Flow (First‑Time)
Quick Setup: Age, retirement timing, savings, annual spend, current allocation.


Instant Results: e.g., "Success probability 84%; failures median depletion age 88; show distribution."


Optimize: Recommend allocation (e.g., 67/33 → success +5 pp); link to comparison.


Stress Test: Early bear and inflation spike; show spend‑cut implications; suggest cash reserve.


Social Security Prompt: Explore 62/FRA/70; show effect on withdrawals and success.


Key output metrics
Success probability; median ending balance; 10th percentile outcome; years until depletion.



10) Go‑to‑Market & Trust
Launch on Product Hunt / Hacker News; host free "Retirement Planning Workshop" webinar to capture emails.


Trust through transparency: methodology page, cited sources, clear trade‑offs.


Position as advisor sanity check / second opinion.



11) Compliance & Legal
Prominent disclaimer: Educational projections only; not financial/tax/legal advice; hypothetical results; no guarantees; consult a professional.


Terms of Service: estimates only; past ≠ future; no accuracy warranty; limitation of liability.


Insurance: E&O ($1M), cyber liability.



12) Success Metrics (Business)
Activation to first result (< 2 minutes) and completion rate.


Free→Paid conversion %, scenario‑save rate, stress‑test usage.


% of users who run SS timing and IRMAA checks.


NPS and refund rate.



13) Risks & Mitigations
Perceived complexity → Default simple flows; progressive disclosure.


Trust/credibility → Show assumptions, cite reputable sources, clear disclaimers.


Narrow scope (2 assets) → Roadmap for expanded assets (Phase 3).


Advisor/channel competition → Lean into second‑opinion positioning and unique IRMAA/tax features.



14) Open Questions / Decisions Needed
Final bounds for optimizer (default 20–80 stocks okay?).


Default inflation and return/volatility presets (historic vs user‑rollable ranges).


Minimum viable tax‑aware logic for V1.1 (how deep before CPA‑level complexity?).


Report length: 1‑page in V1; 10‑page detailed report in Advanced.


Prioritization between TIPS ladder vs Annuity floor in early roadmap.



15) Appendix — Key Concept Explainers (User‑Facing Copy Drafts)
Sequence‑of‑Returns Risk: Early negative returns increase depletion risk even if the long‑run average is the same. Our stress tests show impacts and how allocation/spending flexibility help.


Social Security Timing: Compare 62/FRA/70; later claiming generally reduces portfolio withdrawals and can raise survival odds; includes breakeven age view.


IRMAA (Medicare): Income‑related surcharges on Parts B/D based on MAGI from two years prior. Crossing a threshold by even $1 can raise premiums; certain life changes qualify for appeal. We flag thresholds and show potential impacts.


Tax‑Aware Withdrawals & Roth Conversions: Simple heuristics to improve after‑tax outcomes and sometimes avoid IRMAA brackets during "gap years."


"Blend with Guarantees": Compare a pure market approach to adding annuities or a TIPS ladder to lower failure rates at the cost of upside/bequest.


16) UX & Accessibility Requirements

Given our target demographic (pre-retirees and retirees 60+ years old), the application must prioritize accessibility and senior-friendly design:

**Visual Accessibility:**
- Large, clear fonts (minimum 18px body text, 24px+ headings)
- High contrast color schemes meeting WCAG 2.1 AA standards (4.5:1 for normal text, 3:1 for large text)
- Clean, uncluttered layouts with ample white space
- Large touch/click targets (minimum 44x44px)
- Clear visual hierarchy and focus indicators

**Assistive Technology Support:**
- Text-to-speech capability for all questions, instructions, and help text
- Full keyboard navigation support (no mouse required)
- Screen reader optimization with semantic HTML and ARIA labels
- High-visibility focus indicators for keyboard navigation
- Accessible error messages announced by screen readers

**Senior-Friendly UX:**
- Simple, clear language without jargon
- Minimal cognitive load - progressive disclosure of complexity
- Helpful tooltips and explanations
- Forgiving input validation with clear guidance
- Consistent, predictable interface patterns

**Testing & Compliance:**
- WCAG 2.1 Level AA compliance minimum
- Lighthouse accessibility audit scores 90+
- Tested with screen readers (NVDA, JAWS, VoiceOver)
- Keyboard-only navigation testing
- Color contrast verification tools

**Implementation Notes:**
- Use browser's native Web Speech API for text-to-speech (no external dependencies)
- Semantic HTML5 for proper document structure
- Tailwind CSS with custom accessibility-first theme
- Progressive enhancement approach (core functionality works without JavaScript)
