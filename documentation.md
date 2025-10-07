# Retirement Planning Application - Development Documentation

## Project Overview

**Name:** Longevity Planning
**Domain:** LongevityPlanning.ai (owned on GoDaddy, not yet connected)
**Current Deployment:** https://retirement-planning-blush.vercel.app/
**Repository:** https://github.com/Nadirh/retirement-planning

### Purpose
DIY retirement planning tool with Monte Carlo simulations. Helps users optimize portfolio allocation and withdrawal strategy to maximize odds of not running out of money in retirement.

### Target Audience
Retirees and pre-retirees (60+ years old) who need accessible, easy-to-use financial planning tools.

---

## Current Status

### What's Built (Phase 1 - MVP Input Form)
✅ **Accessible 3-question retirement planning form**
- Years in retirement (1-60 range)
- Year 1 withdrawal rate as % of portfolio (0.1-20% range)
- Inflation rate with 3% default (0-10% range)

✅ **Accessibility Features (WCAG 2.1 AA Compliant)**
- Large, clear fonts (18px+ body, 24px+ inputs/headings)
- High contrast colors (4.5:1 for normal text, 3:1 for large text)
- Text-to-speech with **female voice** (reads questions aloud)
- **Speech-to-text input** (users can speak answers)
- Full keyboard navigation support
- Screen reader optimization with ARIA labels
- Skip-to-content link
- Large touch targets (44x44px minimum)
- High-visibility focus indicators

✅ **User Experience**
- Clean, uncluttered layout
- Real-time form validation with helpful error messages
- Visual feedback for voice features (pulsing microphone when listening)
- Helpful instructions and placeholder text

### What's NOT Built Yet
❌ Monte Carlo simulation engine
❌ Results visualization (charts/graphs)
❌ Additional input fields (age, retirement age, portfolio size, Social Security)
❌ Data persistence (Supabase integration)
❌ Custom domain connection (LongevityPlanning.ai)
❌ Backend optimizer API (Python)

---

## Technology Stack

### Frontend
- **Next.js 15.5.4** (App Router with Turbopack)
- **React 19.1.0**
- **TypeScript 5**
- **Tailwind CSS 4** (with PostCSS)
- **Web Speech API** (built-in browser API for text-to-speech and speech recognition)

### Development Environment
- **GitHub Codespaces** (Node.js 20, Python 3.11)
- **VS Code** with ESLint, Prettier extensions

### Deployment
- **Vercel** (auto-deploys from GitHub main branch)
- **Production URL:** https://retirement-planning-blush.vercel.app/

### Planned (Not Yet Implemented)
- **Supabase** (PostgreSQL database for persistence)
- **Python 3.11** (optimizer API)
- **NumPy/SciPy** (Monte Carlo simulations)

---

## Project Structure

```
retirement-planning/
├── .devcontainer/
│   └── devcontainer.json          # GitHub Codespaces configuration
├── frontend/
│   ├── app/
│   │   ├── layout.tsx             # Root layout with metadata and skip-to-content
│   │   ├── page.tsx               # Main form component (308 lines)
│   │   └── globals.css            # Accessibility-first theme
│   ├── public/                    # Static assets
│   ├── package.json               # Dependencies
│   ├── tsconfig.json              # TypeScript config
│   ├── tailwind.config.ts         # Tailwind setup
│   ├── next.config.ts             # Next.js config
│   └── eslint.config.mjs          # ESLint rules
├── optimizer-api/                 # (Not yet implemented)
├── ARCHITECTURE.md                # Technical architecture and roadmap
├── prd.md                         # Product requirements document
├── claude.md                      # Development workflow guide
├── todo.md                        # Development tracking and deep thinking
└── documentation.md               # This file
```

---

## Key Features Implementation

### 1. Text-to-Speech (Female Voice)

**Location:** `/frontend/app/page.tsx` lines 21-54

**How it works:**
- Uses browser's `speechSynthesis` API
- Searches for female voices across platforms:
  - macOS: Samantha, Victoria
  - Windows: Zira, Microsoft Zira
  - Chrome: Google US English Female
- Slower speech rate (0.9) for clarity
- Blue speaker icons next to each question
- Visual indicator when speaking (button changes color)

**Browser support:** Chrome, Edge, Safari, Firefox

### 2. Speech-to-Text (Voice Input)

**Location:** `/frontend/app/page.tsx` lines 56-102

**How it works:**
- Uses `webkitSpeechRecognition` or `SpeechRecognition` API
- Green microphone button next to each input field
- Button turns red and pulses when listening
- Extracts numbers from spoken text using regex `/\d+(\.\d+)?/`
- Automatically fills input field with recognized number
- Error handling with helpful messages

**Browser support:** Chrome, Edge, Safari (not Firefox)

### 3. Form Validation

**Location:** `/frontend/app/page.tsx` lines 114-165

**Validation rules:**
- **Years in retirement:** Must be whole number between 1-60
- **Withdrawal rate:** Must be decimal between 0.1-20
- **Inflation rate:** Must be decimal between 0-10

**User experience:**
- Errors display in red below each field
- Errors clear automatically when user starts typing
- All errors shown on submit attempt
- Helpful, accessible error messages

### 4. Accessibility Features

**Location:** `/frontend/app/globals.css` and `/frontend/app/layout.tsx`

**Implementation:**
- CSS custom properties for consistent theming
- `:focus-visible` for keyboard navigation indicators
- ARIA labels on all interactive elements
- Semantic HTML5 structure
- Skip-to-content link (hidden until focused)
- Large touch targets enforced via CSS

---

## Development Workflow

### Local Development

1. **Start development server:**
   ```bash
   cd frontend
   npm run dev
   ```
   Runs at http://localhost:3000 with hot reload

2. **Build for production:**
   ```bash
   npm run build
   ```
   Verifies TypeScript types and runs ESLint

3. **Run linter:**
   ```bash
   npm run lint
   ```

### Git Workflow

1. Make changes to code
2. Test locally with `npm run dev`
3. Verify build succeeds with `npm run build`
4. Commit changes:
   ```bash
   git add .
   git commit -m "descriptive message"
   ```
5. Push to GitHub:
   ```bash
   git push
   ```
6. Vercel auto-deploys from main branch (takes ~1-2 minutes)

### Deployment

- **Automatic:** Every push to `main` branch triggers Vercel deployment
- **Manual:** Can deploy from Vercel dashboard
- **Preview:** Each commit gets unique preview URL
- **Production:** https://retirement-planning-blush.vercel.app/ (stable URL)

---

## Code Quality Standards

### TypeScript
- Strict mode enabled
- ESLint enforces type safety
- `any` types only allowed with `eslint-disable` comments (used for Web Speech API due to incomplete browser typings)

### Accessibility
- WCAG 2.1 AA compliance
- All interactive elements keyboard accessible
- ARIA labels on all form controls
- Color contrast ratios verified:
  - Normal text: 4.5:1 minimum
  - Large text: 3:1 minimum

### File Organization
- **Single Responsibility:** Each component has one clear purpose
- **No over-engineering:** Use built-in browser APIs over external libraries
- **Progressive enhancement:** Core functionality works without JavaScript

---

## Known Issues & Limitations

### Browser Compatibility
- **Text-to-speech:** Works in all modern browsers (Chrome, Edge, Safari, Firefox)
- **Speech-to-text:** Only works in Chrome, Edge, Safari (not Firefox)
- Graceful fallback messages shown for unsupported browsers

### TypeScript Limitations
- Web Speech API requires `any` types with ESLint disable comments
- Browser APIs have incomplete TypeScript definitions

### Current Limitations
- Form data only stored in browser state (lost on page refresh)
- No backend API yet
- No data persistence
- No Monte Carlo simulation yet
- No results visualization

---

## Testing Checklist

### Manual Testing (Before Each Release)

**Visual Inspection:**
- [ ] Large, readable fonts throughout
- [ ] High contrast colors
- [ ] Clean, uncluttered layout
- [ ] Responsive on mobile and desktop

**Keyboard Navigation:**
- [ ] Tab through all form fields
- [ ] Focus indicators highly visible
- [ ] Enter key submits form
- [ ] Skip-to-content link works

**Text-to-Speech:**
- [ ] Click speaker icons to hear questions
- [ ] Female voice used (platform-dependent)
- [ ] Visual indicator shows when speaking
- [ ] Speech rate is clear and understandable

**Speech-to-Text:**
- [ ] Click microphone buttons
- [ ] Button turns red and pulses when listening
- [ ] Spoken numbers fill input fields correctly
- [ ] Error messages helpful for non-numeric speech
- [ ] Works in Chrome, Edge, Safari

**Form Validation:**
- [ ] Empty form shows all error messages
- [ ] Invalid values show specific errors
- [ ] Valid values submit successfully
- [ ] Errors clear when typing
- [ ] Console logs form data on submit

**Screen Reader (if available):**
- [ ] NVDA/JAWS/VoiceOver reads all content
- [ ] Skip-to-content link announced
- [ ] Error messages announced
- [ ] Form labels correctly associated

---

## Next Steps (Roadmap)

### Phase 2: Monte Carlo Simulation (Next Priority)
1. Add Monte Carlo simulation engine (client-side JavaScript)
2. Display results with basic statistics
3. Add simple chart/visualization
4. Show probability of success percentage

### Phase 3: Enhanced Inputs
1. Add age and retirement age fields
2. Add current portfolio size field
3. Add Social Security benefits (optional)
4. Add asset allocation (stocks/bonds split)

### Phase 4: Data Persistence
1. Set up Supabase project
2. Add user authentication
3. Save simulation results to database
4. Allow users to compare scenarios

### Phase 5: Advanced Optimization
1. Build Python optimizer API
2. Deploy as serverless function
3. Connect frontend to optimizer
4. Show optimized withdrawal strategies

### Phase 6: Production Launch
1. Connect LongevityPlanning.ai domain to Vercel
2. Add analytics (privacy-focused)
3. Add error tracking (Sentry or similar)
4. Performance optimization
5. SEO optimization

---

## Architecture Principles

From `ARCHITECTURE.md`:

1. **Simplicity First:** Avoid over-engineering, use standard solutions
2. **Single Responsibility:** Each component has one clear job
3. **Progressive Enhancement:** Core features work without JavaScript
4. **Accessibility:** WCAG 2.1 AA minimum, optimize for 60+ users
5. **Separation of Concerns:** Frontend (Next.js) separate from backend (Python)
6. **Incremental Development:** Ship small, working features frequently

---

## Development Guidelines

From `claude.md`:

1. **Deep Thinking:** Analyze requirements thoroughly before coding
2. **Plan in todo.md:** Document approach, dependencies, edge cases
3. **Wait for Approval:** Get user sign-off before implementation
4. **Incremental Commits:** Small, working changes committed frequently
5. **Test Locally:** Verify builds before pushing
6. **Update Documentation:** Keep todo.md and documentation.md current

---

## Useful Commands

### Frontend Development
```bash
cd frontend
npm run dev          # Start dev server (localhost:3000)
npm run build        # Production build with type checking
npm run lint         # Run ESLint
npm run start        # Start production server
```

### Git Operations
```bash
git status           # Check current changes
git add .            # Stage all changes
git commit -m "msg"  # Commit with message
git push             # Push to GitHub (triggers Vercel deploy)
git log --oneline    # View commit history
```

### Vercel
```bash
# Vercel auto-deploys from GitHub
# No manual commands needed
# Check status at https://vercel.com/
```

---

## Contact & Resources

- **GitHub Repository:** https://github.com/Nadirh/retirement-planning
- **Production URL:** https://retirement-planning-blush.vercel.app/
- **Vercel Dashboard:** https://vercel.com/ (requires login)
- **Next.js Docs:** https://nextjs.org/docs
- **Tailwind CSS Docs:** https://tailwindcss.com/docs
- **WCAG Guidelines:** https://www.w3.org/WAI/WCAG21/quickref/

---

## Change Log

### 2025-10-07 - Voice Features & TypeScript Fixes
- ✅ Added female voice text-to-speech
- ✅ Added speech-to-text input for all fields
- ✅ Fixed TypeScript build errors with ESLint disable comments
- ✅ Deployed to Vercel successfully

### 2025-10-07 - Initial Form Implementation
- ✅ Initialized Next.js 14 with TypeScript and Tailwind
- ✅ Created accessibility-first theme
- ✅ Built 3-question form component
- ✅ Added text-to-speech (initial version)
- ✅ Added form validation
- ✅ Added keyboard navigation support
- ✅ Deployed to Vercel

### 2025-10-07 - Project Setup
- ✅ Created GitHub repository
- ✅ Set up GitHub Codespaces
- ✅ Created ARCHITECTURE.md
- ✅ Created prd.md
- ✅ Created claude.md workflow guide

---

**Last Updated:** October 7, 2025
**Current Version:** 0.1.0 (MVP Input Form)
**Status:** ✅ Phase 1 Complete - Ready for user testing
