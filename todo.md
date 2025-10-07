# Feature: Initial Input Form (3 Questions)

## Deep Thinking Analysis

### Problem Understanding
Create the first user-facing feature: a simple web form collecting 3 critical retirement planning inputs:
1. Years in retirement (planning horizon)
2. Year 1 withdrawal rate as % of portfolio
3. Inflation rate (default 3%)

This is the foundation for the Monte Carlo simulator. Must be clean, simple, and functional.

**Critical UX Requirements:**
- Target audience: 60+ years old (retirees and pre-retirees)
- Must be absolutely wonderful, easy, and pleasing to the eye
- Excellent accessibility (WCAG 2.1 AA minimum)
- Large, clear fonts with high contrast
- Text-to-speech capability for visually impaired users
- Keyboard navigation support
- Screen reader optimized

### Why This Approach
- Start with absolute minimum viable input to prove concept
- These 3 inputs are sufficient to run a basic Monte Carlo simulation
- User sees form immediately (instant engagement)
- Follows PRD "2-minute intake → instant baseline result"
- No backend/database needed yet - pure frontend
- Aligns with ARCHITECTURE.md Phase 1: "Input forms"

### Decomposition
1. Initialize Next.js 14+ with TypeScript (App Router)
2. Set up Tailwind CSS for styling with accessibility-first theme
3. Create home page with 3-question form component
4. Implement beautiful, senior-friendly UI design
5. Add comprehensive accessibility features (ARIA labels, semantic HTML, keyboard nav)
6. Integrate text-to-speech for form questions and instructions
7. Add form validation (client-side) with clear error messages
8. Handle form submission (console.log for now)
9. Test with screen readers and keyboard-only navigation

### Dependencies Analysis

**Files to create:**
- `frontend/package.json` (full Next.js + dependencies)
- `frontend/tsconfig.json` (TypeScript configuration)
- `frontend/next.config.js` (Next.js config)
- `frontend/tailwind.config.ts` (Tailwind setup)
- `frontend/postcss.config.js` (for Tailwind)
- `frontend/app/layout.tsx` (root layout)
- `frontend/app/page.tsx` (home page with form)
- `frontend/app/globals.css` (Tailwind imports)

**Files to modify:**
- None (all new files)

**Potential conflicts:**
- None (greenfield frontend)

### Edge Cases Identified
- **Years in retirement**: Must be positive integer (validate 1-60 range)
- **Withdrawal rate**: Must be positive decimal (validate 0.1%-20% range)
- **Inflation rate**: Can be 0 or positive (validate 0%-10% range)
- **Empty inputs**: Require all fields before submission
- **Invalid numbers**: Handle non-numeric gracefully
- **Negative numbers**: Reject negative values
- **Extreme values**: Warn if values seem unrealistic
- **Accessibility**:
  - Screen reader users must understand all form elements
  - Keyboard-only users must be able to navigate and submit
  - Error messages must be announced by screen readers
  - Focus indicators must be highly visible
  - Text-to-speech button must be easily discoverable
  - Color contrast must meet WCAG AA (4.5:1 for normal text, 3:1 for large text)

### Simplicity Check
✓ Only 3 input fields - nothing more
✓ No backend API calls yet
✓ No database - values stay in browser
✓ Clean Tailwind styling with accessibility-first approach
✓ Use Next.js 14 App Router (modern, simpler)
✓ Single page component - no routing yet
✓ Use browser's Web Speech API for text-to-speech (built-in, no external dependencies)
✓ Semantic HTML for screen readers
✗ NOT adding Monte Carlo simulation yet (next step)
✗ NOT adding charts/visualizations yet
✗ NOT adding Social Security, age, portfolio size yet
✗ NOT adding navigation or multiple pages
✗ NOT over-complicating accessibility (use standard patterns)

### Architecture Alignment
✓ Matches ARCHITECTURE.md Phase 1: "Next.js application with TypeScript"
✓ Follows "Input forms" requirement
✓ Single Responsibility: Form component only collects input
✓ Matches PRD section 5.1 "Required inputs"
✓ Follows PRD section 9 "Quick Setup"
✓ Uses recommended tech stack: Next.js, TypeScript, Tailwind

## Todo Items

- [ ] Initialize Next.js 14 with TypeScript and Tailwind CSS (Medium)
- [ ] Create root layout with accessibility-first theme (fonts, colors, contrast) (Simple)
- [ ] Build home page with 3-question form component using semantic HTML (Medium)
- [ ] Implement beautiful, senior-friendly UI design with large fonts and high contrast (Medium)
- [ ] Add text-to-speech functionality for questions and help text (Medium)
- [ ] Add comprehensive ARIA labels and keyboard navigation (Simple)
- [ ] Add form validation with clear, accessible error messages (Simple)
- [ ] Test with keyboard navigation and verify focus indicators (Simple)
- [ ] Test form submission and console output (Simple)

## Risks

- **Risk**: Next.js setup might have dependency conflicts
  - **Mitigation**: Use latest stable Next.js 14, follow official docs

- **Risk**: Form validation might be too strict/lenient
  - **Mitigation**: Start with reasonable ranges, iterate based on feedback

- **Risk**: User might not understand what inputs mean
  - **Mitigation**: Add clear labels, help text, and tooltips with simple explanations

- **Risk**: Text-to-speech might not work in all browsers
  - **Mitigation**: Use Web Speech API with graceful fallback message; works in Chrome, Edge, Safari

- **Risk**: Accessibility might not meet all WCAG 2.1 AA criteria
  - **Mitigation**: Follow standard patterns, test with screen readers (NVDA/JAWS), use Lighthouse audit

- **Risk**: Design might be too complex for seniors
  - **Mitigation**: Keep UI minimal, use large touch targets (min 44x44px), clear visual hierarchy

## Dependencies

- Node.js 20 (already in devcontainer)
- npm or yarn for package management

---

**Awaiting approval before proceeding with implementation.**
