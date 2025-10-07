# Retirement Planning App - Technical Architecture

## Project Overview

Web application for retirement planning using Monte Carlo simulations to help users optimize asset allocation and maximize probability of not running out of money.

**For development workflow and process, see `CLAUDE.md`**

---

## Technology Stack

### Frontend
- **Framework**: Next.js (React with TypeScript)
- **Purpose**:
  - User interface (forms, sliders, dashboards)
  - Client-side Monte Carlo simulations
  - Data visualizations and charts
- **Deployment**: Vercel
  - Zero-config deployment from GitHub
  - Automatic preview deployments for branches
  - Free tier available
  - Custom domains supported

### Database & Authentication
- **Platform**: Supabase
- **Features**:
  - PostgreSQL database
  - Built-in user authentication (login/signup)
  - Row-level security
  - Real-time subscriptions (optional)
  - Storage for user profiles, scenarios, historical runs
- **Deployment**: Supabase Cloud (managed service)
- **Cost**: Free tier (500MB database, 50K monthly active users)

### Backend Optimizer Service
- **Language**: Python 3.11+
- **Framework**: Flask or FastAPI
- **Purpose**: Portfolio optimization algorithms
- **Deployment**: Fly.io
  - Global edge deployment (low latency worldwide)
  - Deploy via CLI: `fly deploy`
  - ~$5-15/month
  - Free tier: 3 shared-cpu VMs
- **Libraries**:
  - **SciPy** (`scipy.optimize`) - Core optimization algorithms
  - **NumPy** - Numerical computing and array operations
  - **Pandas** (optional) - Data manipulation
  - Optional advanced: DEAP, PyGAD for genetic algorithms

### Development Environment
- **Platform**: GitHub Codespaces
- **Why**: Cloud-based development, no disk crash risk, work from anywhere
- **Configuration**: `.devcontainer/devcontainer.json` for automatic setup
- **Features**:
  - Pre-configured with Node.js and Python
  - Integrated VS Code in browser
  - Works with Claude Code via terminal
  - Auto-saves to GitHub
  - 60 hours/month free tier (2-core machine)
- **Cost**: Free for 60 hours/month, then ~$0.18/hour for 2-core machine

### Source Control
- **Platform**: GitHub
- **Structure**: Monorepo recommended
  ```
  retirement-planner/
  ├── .devcontainer/
  │   └── devcontainer.json    (Codespaces config)
  ├── frontend/
  │   ├── components/
  │   │   ├── ui/              (reusable UI components)
  │   │   ├── forms/           (input forms)
  │   │   └── charts/          (visualizations)
  │   ├── lib/
  │   │   ├── simulation/      (Monte Carlo logic)
  │   │   ├── calculations/    (financial calculations)
  │   │   └── api/             (API client for backend)
  │   ├── services/
  │   │   ├── database.ts      (data access layer)
  │   │   └── auth.ts          (authentication)
  │   ├── pages/
  │   │   └── api/             (Next.js API routes)
  │   └── types/               (TypeScript interfaces)
  ├── optimizer-api/
  │   ├── app/
  │   │   ├── optimizers/
  │   │   │   ├── base.py              (abstract base class)
  │   │   │   ├── gradient.py          (gradient descent)
  │   │   │   ├── evolutionary.py      (genetic algorithm)
  │   │   │   └── efficient_frontier.py
  │   │   ├── models/          (data models)
  │   │   ├── services/        (business logic)
  │   │   ├── repositories/    (data access)
  │   │   └── api/             (Flask/FastAPI routes)
  │   ├── tests/
  │   └── requirements.txt
  ├── CLAUDE.md                (Development workflow)
  ├── ARCHITECTURE.md          (This file)
  └── README.md
  ```

---

## System Architecture

### High-Level Data Flow

```
User Browser
    ↓
Next.js Frontend (Vercel)
├─ UI/UX (forms, charts, dashboards)
├─ Monte Carlo simulations (client-side for speed)
├─ Charts/visualizations (recharts)
└─ User input validation
    ↓
Supabase (Database & Auth)
├─ User accounts and authentication
├─ Saved retirement scenarios
├─ Historical simulation results
└─ User preferences
    ↓
Python Optimizer API (Fly.io)
├─ Portfolio optimization algorithms
├─ Gradient descent optimization
├─ Evolutionary/genetic algorithms
└─ Efficient frontier calculations
```

### Communication Flow

1. User inputs retirement data in Next.js UI
2. Frontend runs quick Monte Carlo simulations (1,000-10,000 runs)
3. Results saved to Supabase for user's account
4. For optimization, frontend calls Python API on Fly.io
5. Python API runs sophisticated optimization algorithms
6. Optimized portfolio returned to frontend
7. Frontend displays results with charts/visualizations

---

## Optimization Algorithms

### Excel Solver Equivalents in Python

The app replicates and exceeds Excel Solver functionality:

#### 1. **GRG Nonlinear** (Gradient-Based Optimization)
- **Python Implementation**: `scipy.optimize.minimize` with method='SLSQP'
- **Use Case**: Smooth nonlinear portfolio optimization
- **Characteristics**: Fast, finds local optimum, handles constraints
- **Best For**: Standard portfolio optimization with known objectives

#### 2. **Evolutionary/Genetic Algorithms**
- **Python Implementation**: `scipy.optimize.differential_evolution`
- **Use Case**: Global optimization, complex constraint scenarios
- **Characteristics**: Slower but more thorough, finds global optimum
- **Best For**: Complex retirement scenarios with multiple constraints

#### 3. **Linear Programming**
- **Python Implementation**: `scipy.optimize.linprog`
- **Use Case**: Linear constraint problems
- **Characteristics**: Fast, guaranteed optimal solution for linear problems
- **Best For**: Simple allocation problems with linear constraints

### Optimization Features to Implement

**Constraint Types:**
- Asset allocations must sum to 100%
- No short selling (each allocation ≥ 0%)
- Min/max allocation limits per asset class (e.g., stocks 40-80%)
- Target return or risk level
- Maximum drawdown limits
- Minimum probability of success threshold

**Optimization Modes:**
1. **Quick Optimization** (Gradient Descent/SLSQP)
   - ~1-5 seconds
   - Finds good local optimum
   - Suitable for most users

2. **Deep Optimization** (Evolutionary)
   - ~10-30 seconds
   - More thorough search
   - Better for complex scenarios

3. **Efficient Frontier** (Multiple optimizations)
   - Run optimization at different risk/return levels
   - Show curve of optimal portfolios
   - Helps users understand risk/return trade-offs

### Python Libraries for Optimization

**Core:**
- **SciPy** (`scipy.optimize`): Industry-standard optimization
- **NumPy**: Fast numerical computing
- **Pandas** (optional): Data manipulation

**Advanced (Phase 3+):**
- **DEAP**: Powerful genetic algorithms, highly customizable
- **PyGAD**: Simpler genetic algorithm library
- **Pymoo**: Multi-objective optimization (optimize multiple goals)
- **CVXPY**: For convex optimization problems

---

## Development Phases

### Phase 1: MVP (Frontend Only)
**Goal**: Working retirement calculator with Monte Carlo simulations

**Features:**
- Next.js application with TypeScript
- Input forms: age, retirement age, savings, contributions, expenses
- Asset allocation sliders (stocks/bonds/cash)
- Client-side Monte Carlo simulation engine (1,000-10,000 runs)
- Results visualization: success probability, wealth over time
- Basic charts with recharts
- Responsive design with Tailwind CSS

**No database yet** - calculations done in browser, results not saved

**Deliverables:**
- Functional retirement calculator
- Monte Carlo simulator (tested, accurate)
- Clean UI/UX
- ~2-3 weeks development time

**Success Criteria:**
- User can input data and get retirement projections
- Monte Carlo produces reasonable results
- UI is intuitive and responsive

---

### Phase 2: Add Persistence
**Goal**: Users can save scenarios and track results over time

**Features:**
- Supabase integration
- User authentication (signup/login)
- Save/load retirement scenarios
- Store simulation history
- Compare different scenarios
- User profile and preferences

**Database Schema:**
```sql
users (
  id uuid primary key,
  email text,
  created_at timestamp
)

scenarios (
  id uuid primary key,
  user_id uuid references users,
  name text,
  current_age integer,
  retirement_age integer,
  current_savings decimal,
  monthly_contribution decimal,
  retirement_expenses decimal,
  asset_allocation jsonb,
  created_at timestamp
)

simulation_results (
  id uuid primary key,
  scenario_id uuid references scenarios,
  success_rate decimal,
  results jsonb,
  run_at timestamp
)
```

**Deliverables:**
- Working authentication
- Scenario persistence
- Historical tracking
- ~1-2 weeks development time

**Success Criteria:**
- Users can create accounts
- Scenarios are saved and retrievable
- Data persists across sessions

---

### Phase 3: Advanced Optimization
**Goal**: Sophisticated portfolio optimization using Python backend

**Features:**
- Python Flask/FastAPI optimizer service
- Multiple optimization algorithms:
  - Gradient descent (SLSQP)
  - Evolutionary/genetic algorithms
  - Efficient frontier calculation
- User selects optimization method
- Constrained optimization (min/max allocations, target success rate)
- API endpoints for optimization requests
- Integration with Next.js frontend

**Python API Structure:**
```python
POST /api/optimize
{
  "scenario": {...},
  "constraints": {...},
  "method": "gradient" | "evolutionary" | "efficient_frontier"
}

Response:
{
  "optimized_allocation": {...},
  "expected_success_rate": 0.95,
  "computation_time": 2.3
}
```

**Deliverables:**
- Python optimizer service on Fly.io
- Multiple optimization algorithms
- API integration with frontend
- Visualization of efficient frontier
- ~2-3 weeks development time

**Success Criteria:**
- Optimization produces better allocations than user's initial guess
- Algorithms complete in reasonable time (<30 seconds)
- Results are accurate and reproducible

---

## Key Features to Build

### User Input Features
- Current age, retirement age
- Current savings amount
- Monthly contribution to savings
- Expected retirement expenses (monthly/annual)
- Social Security or pension income (optional)
- Asset allocation preferences (stocks/bonds/cash percentages)
- Risk tolerance selection
- Time horizon

### Monte Carlo Simulation Engine
**Algorithm:**
1. For each simulation (repeat N times):
   - Start with current savings
   - For each year until death:
     - Generate random returns based on asset allocation
     - Add contributions (if before retirement)
     - Subtract expenses (if after retirement)
     - Track balance
   - Record if money ran out (failure) or not (success)
2. Calculate statistics:
   - Success rate (% of simulations that didn't run out)
   - Median ending balance
   - 10th/25th/75th/90th percentiles
   - Years until depletion (for failures)

**Performance:**
- 1,000 simulations: ~100-200ms (acceptable for UI)
- 10,000 simulations: ~1-2 seconds (thorough analysis)
- Run in browser (client-side) for speed

**Return Model (Phase 1):**
- Stocks: Normal distribution (mean=10%, std=18%)
- Bonds: Normal distribution (mean=5%, std=8%)
- Cash: Fixed (1-2%)
- Portfolio return = weighted average based on allocation

**Enhanced Models (Later):**
- Historical return sequences
- Different market regimes
- Correlation between asset classes
- Sequence-of-returns risk

### Portfolio Optimizer
**Input:**
- Current scenario (age, savings, contributions, expenses)
- Constraints (min/max allocations, target success rate)
- Optimization method preference

**Output:**
- Optimized asset allocation
- Expected success rate
- Risk metrics (volatility, max drawdown)
- Comparison with user's original allocation

**Process:**
1. User provides initial allocation
2. Frontend sends to Python optimizer API
3. Optimizer runs chosen algorithm
4. For each candidate allocation:
   - Run Monte Carlo simulations
   - Calculate success rate
   - Check constraints
5. Return best allocation found
6. Frontend displays optimized allocation with comparison

### Visualizations
**Charts to Implement:**
- Success probability over different allocations
- Wealth trajectory over time (median + percentiles)
- Distribution of ending balances (histogram)
- Efficient frontier (risk vs. return)
- Comparison of scenarios side-by-side
- Sensitivity analysis (how changes affect success rate)

**Libraries:**
- Recharts (primary - React-based)
- Chart.js (alternative)
- D3.js (for custom visualizations if needed)

---

## Code Quality Principles

### SOLID Principles Application

**For detailed SOLID guidelines, see `CLAUDE.md`**

#### **Single Responsibility Principle** (ALWAYS)
- Separate UI components, business logic, and data access
- Monte Carlo simulator is standalone module
- Portfolio optimizer is separate from API layer
- Database access through repository pattern

**Example Structure:**
```
frontend/lib/simulation/monteCarlo.ts    (simulation only)
frontend/lib/calculations/returns.ts      (return calculations only)
frontend/services/database.ts             (data access only)
```

#### **Open/Closed Principle** (For Optimizers)
Use strategy pattern for multiple optimization algorithms:

```python
# Base abstraction
class PortfolioOptimizer:
    def optimize(self, scenario, constraints):
        raise NotImplementedError

# Concrete implementations
class GradientDescentOptimizer(PortfolioOptimizer):
    def optimize(self, scenario, constraints):
        # Implementation using scipy.optimize.minimize
        pass

class EvolutionaryOptimizer(PortfolioOptimizer):
    def optimize(self, scenario, constraints):
        # Implementation using differential_evolution
        pass

# Easy to add new optimizers without modifying existing code
class EfficientFrontierOptimizer(PortfolioOptimizer):
    def optimize(self, scenario, constraints):
        # Implementation for efficient frontier
        pass
```

#### **Dependency Inversion Principle** (External Services)
Create interfaces for database and authentication:

```typescript
// Interface (abstraction)
interface IDataRepository {
  saveScenario(scenario: Scenario): Promise<void>;
  loadScenario(id: string): Promise<Scenario>;
  listScenarios(userId: string): Promise<Scenario[]>;
}

// Implementation (concrete)
class SupabaseRepository implements IDataRepository {
  async saveScenario(scenario: Scenario): Promise<void> {
    // Supabase-specific implementation
  }
  // ... other methods
}

// Usage (depends on abstraction, not concrete class)
class ScenarioService {
  constructor(private repository: IDataRepository) {}

  async save(scenario: Scenario) {
    return this.repository.saveScenario(scenario);
  }
}
```

**Benefits:**
- Can swap Supabase for another database without changing business logic
- Easier to test (can mock the repository)
- Cleaner separation of concerns

---

## Deployment Strategy

### Development Workflow

**Working in Codespaces:**
1. Open repository in GitHub Codespaces
2. Use Claude Code to implement features
3. Test locally in Codespaces
4. Commit to feature branch
5. Push to GitHub
6. Automatic deployments trigger

**Deployment Pipeline:**
```
Code in Codespaces
    ↓
Commit to feature branch
    ↓
Push to GitHub
    ↓
├─ Vercel: Deploys preview of Next.js frontend
├─ Fly.io: Can deploy preview of Python backend
└─ Supabase: Shared database (or separate preview DB)
    ↓
Merge to main branch
    ↓
├─ Vercel: Deploys to production
└─ Fly.io: Deploys to production
```

### Deployment Configuration

**Vercel (Next.js):**
- Connect GitHub repository
- Auto-detect Next.js configuration
- Set environment variables:
  - `NEXT_PUBLIC_SUPABASE_URL`
  - `NEXT_PUBLIC_SUPABASE_ANON_KEY`
  - `OPTIMIZER_API_URL` (Fly.io endpoint)
- Deploy on push to main (production)
- Deploy on push to any branch (preview)

**Fly.io (Python API):**
- Install Fly CLI in Codespaces: `curl -L https://fly.io/install.sh | sh`
- Initialize: `fly launch`
- Configure `fly.toml`:
  ```toml
  app = "retirement-optimizer"

  [env]
    PORT = "8080"

  [[services]]
    internal_port = 8080
    protocol = "tcp"

    [[services.ports]]
      port = 80
      handlers = ["http"]
    [[services.ports]]
      port = 443
      handlers = ["tls", "http"]
  ```
- Deploy: `fly deploy`
- Set secrets: `fly secrets set SUPABASE_KEY=xxx`

**Supabase:**
- Create project at supabase.com
- Configure authentication providers
- Set up database schema (run migrations)
- Configure Row Level Security (RLS) policies
- Get connection details for frontend/backend

---

## Cost Estimates

### Monthly Costs (Starting Out)

| Service | Free Tier | Paid Tier | Notes |
|---------|-----------|-----------|-------|
| **GitHub** | ✅ Unlimited | N/A | Free for public/private repos |
| **Codespaces** | 60 hrs/month | $0.18/hr | ~2 hours/day free |
| **Vercel** | ✅ Generous | $20/month | Free tier sufficient for starting |
| **Supabase** | 500MB, 50K users | $25/month | Free tier sufficient for starting |
| **Fly.io** | 3 VMs free | $5-15/month | Free tier or small paid plan |
| **TOTAL** | **$0/month** | **$5-20/month** | Assuming moderate usage |

### Scaling Costs

**At 1,000 active users:**
- Vercel: Still free (likely)
- Supabase: $25/month (exceeded free tier)
- Fly.io: $15-30/month (more compute needed)
- **Total: ~$40-55/month**

**At 10,000 active users:**
- Vercel: $20/month
- Supabase: $25-100/month (depending on usage)
- Fly.io: $50-100/month (more compute/memory)
- **Total: ~$95-220/month**

---

## Testing Strategy

### Frontend Testing
- **Unit tests**: Business logic, calculations, utilities
  - Jest + React Testing Library
  - Test Monte Carlo simulator thoroughly
  - Test financial calculations
- **Integration tests**: Component interactions
  - Test form submissions
  - Test data flow between components
- **E2E tests**: Critical user paths
  - Playwright or Cypress
  - Complete retirement scenario flow
  - Authentication flows

### Backend Testing
- **Unit tests**: Individual functions
  - pytest
  - Test each optimizer algorithm
  - Test constraint handling
  - Test edge cases
- **Integration tests**: API endpoints
  - Test Flask/FastAPI routes
  - Test database operations
  - Test optimization API responses
- **Performance tests**: Algorithm speed
  - Ensure optimizations complete in reasonable time
  - Test with various problem sizes

### Test Coverage Goals
- Frontend: >80% coverage for business logic
- Backend: >90% coverage for optimization algorithms
- Critical paths: 100% E2E test coverage

---

## Security Considerations

### Authentication & Authorization
- Supabase handles authentication (proven, secure)
- Use Row Level Security (RLS) in database
- Never trust client-side data
- Validate all inputs on backend

### Data Privacy
- User financial data is sensitive
- Encrypt data at rest (Supabase default)
- Use HTTPS everywhere (Vercel/Fly.io default)
- Don't log sensitive information
- Consider GDPR compliance if serving EU users

### API Security
- Rate limiting on optimization endpoints (prevent abuse)
- API key authentication between frontend and Python backend
- Validate and sanitize all inputs
- Set reasonable resource limits (prevent DoS)

---

## Performance Optimization

### Frontend Performance
- **Code splitting**: Only load needed components
- **Lazy loading**: Load charts on demand
- **Web Workers**: Consider for heavy Monte Carlo simulations
- **Caching**: Cache simulation results for same inputs
- **Debouncing**: Debounce slider inputs before re-simulating

### Backend Performance
- **Caching**: Cache optimization results for common scenarios
- **Connection pooling**: Reuse database connections
- **Async processing**: Use async/await in Python
- **Resource limits**: Set timeouts on long-running optimizations

### Database Performance
- **Indexes**: On user_id, scenario_id, created_at
- **Query optimization**: Use Supabase's query builder efficiently
- **Pagination**: For listing scenarios
- **Archiving**: Move old results to cold storage

---

## Monitoring & Observability

### Metrics to Track
- **Frontend**: Page load times, error rates, user flows
- **Backend**: API response times, optimization success rates, error rates
- **Database**: Query performance, connection pool usage
- **Business**: Active users, scenarios created, optimizations run

### Tools
- **Vercel Analytics**: Built-in performance monitoring
- **Fly.io Metrics**: CPU, memory, request counts
- **Supabase Dashboard**: Database performance, auth stats
- **Sentry** (optional): Error tracking and alerting

---

## Future Enhancements

### Phase 4+ Ideas
- **Historical backtesting**: Test strategies against historical data
- **Tax optimization**: Roth vs. Traditional IRA, tax-loss harvesting
- **Healthcare costs**: Model Medicare, long-term care
- **Estate planning**: Legacy goals, beneficiaries
- **AI insights**: GPT-4 analysis of retirement scenarios
- **Mobile app**: React Native version
- **Advisor portal**: Financial advisors can manage client portfolios
- **Social features**: Share anonymous scenarios, community benchmarks

---

## References

### Documentation
- Next.js: https://nextjs.org/docs
- Supabase: https://supabase.com/docs
- Fly.io: https://fly.io/docs
- SciPy Optimize: https://docs.scipy.org/doc/scipy/reference/optimize.html

### Learning Resources
- Monte Carlo Simulation: https://www.investopedia.com/terms/m/montecarlosimulation.asp
- Portfolio Optimization: https://en.wikipedia.org/wiki/Portfolio_optimization
- Modern Portfolio Theory: https://www.investopedia.com/terms/m/modernportfoliotheory.asp

---

**Version**: 1.0
**Last Updated**: October 2025
**See Also**: `CLAUDE.md` for development workflow and process
