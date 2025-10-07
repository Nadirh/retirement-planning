# Retirement Planning App

Web application for retirement planning using Monte Carlo simulations to help users optimize asset allocation and maximize probability of not running out of money.

## Project Status

🚧 **Currently in initial setup phase** - Project structure established, ready for Phase 1 development.

## Technology Stack

- **Frontend**: Next.js (React with TypeScript) on Vercel
- **Database & Auth**: Supabase (PostgreSQL + authentication)
- **Backend**: Python (Flask/FastAPI) on Fly.io for portfolio optimization
- **Development**: GitHub Codespaces

## Project Structure

```
retirement-planning/
├── .devcontainer/          # GitHub Codespaces configuration
├── frontend/               # Next.js application (Phase 1)
├── optimizer-api/          # Python optimization service (Phase 3)
├── CLAUDE.md              # Development workflow and methodology
├── ARCHITECTURE.md        # Complete technical architecture
└── README.md              # This file
```

## Development Phases

### Phase 1: MVP (Frontend Only)
- Next.js retirement calculator
- Monte Carlo simulation engine (client-side)
- Input forms and visualizations
- No database (calculations in browser only)

### Phase 2: Add Persistence
- Supabase integration
- User authentication
- Save/load scenarios
- Historical tracking

### Phase 3: Advanced Optimization
- Python optimizer API
- Multiple optimization algorithms (gradient descent, evolutionary)
- Efficient frontier calculations
- API integration with frontend

## Getting Started

### Prerequisites

- Node.js 20+
- Python 3.11+
- GitHub account (for Codespaces)

### Setup in Codespaces

1. Open this repository in GitHub Codespaces
2. The devcontainer will automatically configure Node.js 20 and Python 3.11
3. Wait for the environment to be ready

### Local Development (Alternative)

```bash
# Install Node.js dependencies (when Phase 1 begins)
cd frontend
npm install

# Install Python dependencies (when Phase 3 begins)
cd optimizer-api
pip install -r requirements.txt
```

## Documentation

- **[CLAUDE.md](./CLAUDE.md)** - Development workflow, process, and guidelines
- **[ARCHITECTURE.md](./ARCHITECTURE.md)** - Complete technical architecture and design
- **[todo.md](./todo.md)** - Current development tasks and planning

## Development Workflow

This project follows a structured development workflow defined in `CLAUDE.md`:

1. **Deep thinking** - Analyze problem thoroughly before coding
2. **Plan in todo.md** - Create detailed implementation plan
3. **Get approval** - Wait for review before proceeding
4. **Feature branches** - All work on `feature/[name]` branches
5. **Incremental commits** - Small, focused changes with clear messages
6. **Code review** - Human review before merging to main

## Core Principles

- **Think deeply before coding** - Planning prevents problems
- **Simplicity over cleverness** - Simple code is maintainable code
- **Incremental progress** - Small changes, frequent commits
- **Human verification** - Approval at key decision points
- **Documentation as you go** - Future you will thank present you

## License

Private project - Not licensed for public use

## Contact

For questions or feedback, please see the project documentation in `CLAUDE.md` and `ARCHITECTURE.md`.

---

**Version**: 0.1.0
**Last Updated**: October 2025
