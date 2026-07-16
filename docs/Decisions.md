# Architecture Decisions

---

## ADR-001: Single User Application

**Status:** Accepted

### Decision

Compass will initially be designed as a single-user application.

All accounts, investments, expenses, assets, liabilities, goals, and documents belong to a single owner.

The data model will remain extensible so that future versions can support multiple people (e.g., spouse, parents, children) without major architectural changes.

### Reason

Keeping v1 focused on one user significantly reduces complexity while satisfying current requirements.