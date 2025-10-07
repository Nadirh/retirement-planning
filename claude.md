# Working with Claude Code

## About This Document

This document defines my preferred working methodology for software development with Claude Code. It applies to all projects regardless of tech stack or domain. For project-specific details, see `ARCHITECTURE.md`.

---

## Philosophy

- **Think deeply before coding** - Planning prevents problems
- **Simplicity over cleverness** - Simple code is maintainable code
- **Incremental progress** - Small changes, frequent commits
- **Human verification** - Approval at key decision points
- **Documentation as you go** - Future you will thank present you

---

## 🧠 Core Principle: Deep Thinking Before Implementation

**CRITICAL**: Before writing ANY code, you must think deeply and create a detailed plan.

### Required Thinking Process

Before implementing anything, work through these steps:

1. **Understand**: What problem are we really solving? Why this approach?
2. **Decompose**: Break into smallest logical steps
3. **Dependencies**: What files/components are affected? What could break?
4. **Edge cases**: What could go wrong? What error handling is needed?
5. **Simplicity check**: Is this the simplest solution possible?
6. **Architecture alignment**: Does this follow project principles (SOLID, etc.)?

Document this thinking process in `todo.md`. Wait for approval. Then code.

**Remember**: Thinking time is free. Fixing poorly-planned code is expensive.
*Hours of debugging can save you minutes of planning.*

### Example of Deep Thinking

**User Request**: "Add authentication"

**Your Thinking Process** (before any code):
```
Understanding the problem:
- Need secure user login/signup
- Must integrate with existing auth provider
- Affects: login page, signup page, protected routes, session management

Decomposition:
- Set up auth provider integration
- Create login UI component
- Create signup UI component
- Add session management
- Protect routes with middleware
- Handle auth state globally

Dependencies:
- Frontend: Pages, components, state management
- Backend: API routes, database schema
- Configuration: Environment variables, auth provider setup

Edge cases:
- Session expiration
- Failed login attempts
- Already logged in user accessing login page
- Password reset flow
- Email verification

Simplicity check:
✓ Use existing auth provider (don't build from scratch)
✓ Use provider's UI components where available
✓ Minimal custom code
✓ Clear separation of concerns

Architecture alignment:
✓ Dependency Inversion: Use auth provider interface
✓ Single Responsibility: Separate auth logic from business logic
✓ Keep it simple: Leverage existing solutions

Now creating detailed plan in todo.md...
```

---

## Development Workflow

Follow this systematic process for every task:

### **1. Problem Analysis & Planning** 🧠 THINK DEEPLY FIRST

```
First think deeply through the problem before any implementation:
- What are we really trying to solve and why?
- What's the simplest possible solution?
- What are ALL the affected files and components?
- What edge cases or error scenarios exist?
- What dependencies or conflicts could arise?
- Does this align with project architecture principles?

Then document your thinking and write a plan to todo.md.

ONLY after deep analysis should you create the todo list.
```

### **2. Create Structured Todo List**

The plan should have:
- List of todo items with checkboxes `[ ]`
- Estimated complexity (simple/medium/complex) for each item
- Any potential risks or dependencies
- Order of implementation

**Template for todo.md:**
```markdown
# Feature: [Feature Name]

## Deep Thinking Analysis

### Problem Understanding
[What problem are we solving and why?]

### Why This Approach
[Justification for chosen solution]

### Decomposition
[Break down into smallest steps]

### Dependencies Analysis
Files to create: [list]
Files to modify: [list]
Potential conflicts: [list]

### Edge Cases Identified
- [Edge case 1]
- [Edge case 2]
- [etc.]

### Simplicity Check
✓ [How this is the simplest approach]
✓ [What we're NOT doing to keep it simple]

### Architecture Alignment
✓ [Which principles this follows]
✓ [How it integrates with existing code]

## Todo Items
- [ ] [Task 1] (Complexity level)
- [ ] [Task 2] (Complexity level)
- [ ] [etc.]

## Risks
- [Risk 1 and mitigation]
- [Risk 2 and mitigation]

## Dependencies
- [List any dependencies on other work]
```

### **3. Human Verification Checkpoint** ⚠️ CRITICAL

```
Before you begin working, check in with me and I will verify the plan.
Wait for my approval before proceeding.
```

**STOP and WAIT for approval.** Do not proceed to coding without explicit human approval of the plan.

### **4. Create Feature Branch**

```
Create a git branch for this work: feature/[descriptive-name]
```

Example: `feature/add-authentication` or `feature/monte-carlo-simulation`

### **5. Incremental Implementation**

```
Begin working on the todo items one at a time:
- Mark them as complete [x] as you go
- Commit after each major todo item with clear commit message
- Give me high-level explanation of what changed after each item
```

**Example progress updates:**
```
✅ Created AuthContext component
   - Manages auth state across app
   - Provides login/logout functions
   - Follows Single Responsibility principle

[Committed: "feat: add AuthContext for global auth state"]

✅ Built login page UI
   - Form with email/password fields
   - Error handling and validation
   - Integrates with AuthContext

[Committed: "feat: add login page with validation"]
```

### **6. Simplicity Mandate** 🎯 MOST IMPORTANT

```
Make every task and code change as simple as possible:
- Avoid making any massive or complex changes
- Every change should impact as little code as possible
- Everything is about simplicity
- If something seems complex, break it into smaller steps
- Prefer multiple small functions over one large function
- Create new files rather than adding to existing large files
```

**Good (Simple):**
```typescript
// One function, one purpose - easy to understand
function calculateMonthlyPayment(principal: number, rate: number, months: number): number {
  const monthlyRate = rate / 12;
  return principal * (monthlyRate * Math.pow(1 + monthlyRate, months)) /
         (Math.pow(1 + monthlyRate, months) - 1);
}
```

**Bad (Complex):**
```typescript
// Does too much - hard to understand and maintain
function processUserFinancialData(userData: any): any {
  // 300 lines of mixed concerns
  // calculation + validation + database + email notification + logging
}
```

### **7. Documentation & Review**

```
After completing all items, add to todo.md:
- Review section: summary of changes made
- Testing section: how to verify changes work
- Files changed: list of new/modified files
- Any follow-up items or technical debt created
```

**Template for review section:**
```markdown
## Review
[Summary of what was implemented]
- Key decisions made
- Final code stats (lines, files)
- How it follows architecture principles

## Files Changed
- Created: [list]
- Modified: [list]
- Deleted: [list]

## Testing
```bash
[Commands to run tests]
```
Expected results: [what should happen]

Manual testing:
1. [Step 1]
2. [Step 2]
3. Expected outcome: [description]

## Follow-up Items
- [ ] [Future enhancement 1]
- [ ] [Future enhancement 2]
- [ ] [Technical debt to address]
```

### **8. Human Review Before Merge**

```
Ask me to review the changes before merging to main branch.
```

Wait for approval, then merge and clean up branch.

---

## Code Quality Standards

### SOLID Principles

Apply SOLID principles pragmatically:

**Always Apply:**
- ✅ **Single Responsibility**: Each module/class does one thing
- ✅ **Dependency Inversion**: Depend on abstractions for external services

**Apply When Relevant:**
- ✅ **Open/Closed**: When you know there will be multiple implementations
- ✅ **Liskov Substitution**: When using inheritance
- ✅ **Interface Segregation**: When interfaces grow large

**Don't Over-Engineer:**
- ❌ Don't create abstractions for things that won't change
- ❌ Don't add layers of indirection without clear benefit
- ❌ Ship working code first, refactor later if needed

### Testing Requirements

- **Unit tests**: For business logic and calculations
- **Integration tests**: For API endpoints and database operations
- **End-to-end tests**: For critical user workflows
- Make code testable through dependency injection
- Mock external services in tests

### Documentation Standards

- **Code comments**: For complex algorithms or non-obvious logic
- **Docstrings/JSDoc**: For all public functions and classes
- **README files**: In each major directory explaining structure
- **todo.md**: Track decisions and progress
- **Architecture Decision Records (ADRs)**: For major design choices

---

## Communication Guidelines

### When Creating Plans

- ✅ Show your thinking process explicitly
- ✅ Identify risks and trade-offs
- ✅ Provide reasoning for chosen approach
- ✅ Ask questions if requirements are unclear
- ✅ Wait for approval before proceeding

### When Implementing

- ✅ Explain what changed (high-level, not line-by-line)
- ✅ Commit frequently with clear messages
- ✅ Flag any deviations from approved plan
- ✅ Ask for guidance when stuck
- ✅ Update todo.md as you progress

### When Completing Work

- ✅ Summarize all changes made
- ✅ Document how to test/verify
- ✅ Identify any follow-up items
- ✅ Request code review
- ✅ Wait for approval to merge

### Commit Message Format

Use conventional commits:

```
feat: add user authentication
fix: resolve login redirect issue
docs: update API documentation
refactor: simplify payment calculation
test: add unit tests for simulator
chore: update dependencies
```

---

## Command Template

When I give you a task, I'll use this format:

```
Task: [What to build]

IMPORTANT: Think deeply before implementing. Analyze the problem
thoroughly, consider all edge cases and dependencies, and create
a detailed plan before writing any code.

Follow the development workflow:
1. Deep thinking: Analyze problem, decompose, identify edge cases
2. Create detailed plan in todo.md with your thinking documented
3. Wait for my approval
4. Create feature branch: feature/[name]
5. Work through todo items incrementally
6. Keep every change as simple as possible
7. Commit after each major item
8. Add review section when complete
9. Wait for my approval to merge

Additional context:
- [Specific requirements]
- [Constraints or preferences]
```

---

## Tips for Success

### DO:
- ✅ Think deeply and document your thinking
- ✅ Wait for approval at checkpoints
- ✅ Keep changes simple and focused
- ✅ Commit frequently with clear messages
- ✅ Explain your reasoning
- ✅ Ask questions when unclear
- ✅ Test thoroughly before requesting review
- ✅ Use feature branches
- ✅ Update documentation as you go

### DON'T:
- ❌ Jump straight to coding without planning
- ❌ Proceed without approval
- ❌ Make complex, sweeping changes
- ❌ Work directly on main branch
- ❌ Skip the review section
- ❌ Merge without testing
- ❌ Leave unclear commit messages
- ❌ Accept "I'll figure it out as I code" approaches

---

## Example Complete Workflow

**User**: "Add user authentication"

**Claude Code**:
```
I'll think through this deeply before implementing...

[Shows detailed thinking process as documented above]

Creating plan in todo.md now...
```

[Creates detailed todo.md with deep thinking analysis]

**Claude Code**: "Plan is ready in todo.md. Please review and approve before I begin implementation."

**User**: "Approved, but use OAuth instead of password auth"

**Claude Code**:
```bash
git checkout -b feature/oauth-authentication
```

"✅ Starting work. Updated plan to use OAuth..."

[Works through todo items incrementally with updates]

"✅ All todo items complete. Added review section to todo.md. Please review before I merge to main."

**User**: "Looks good, merge it"

**Claude Code**:
```bash
git checkout main
git merge feature/oauth-authentication
git push
```

"✅ Merged to main. Authentication feature is complete and deployed."

---

## Project-Specific Information

For details specific to the current project, see:
- **ARCHITECTURE.md** - Tech stack, deployment, system design
- **README.md** - What the project does, how to run it

---

**Version**: 1.0
**Last Updated**: October 2025

---

## Notes

This is a living document. As we work together and discover what works well, we'll refine these guidelines. Suggest improvements when you notice patterns that could be documented.
