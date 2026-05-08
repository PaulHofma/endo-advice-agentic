## Why

The backend currently uses a flat layered structure where controllers depend directly on Spring Data repositories, conflating HTTP concerns with data access and leaving no room for domain logic or testable use-case boundaries. Adopting hexagonal architecture (ports & adapters) will make the application core independent of frameworks and infrastructure, enabling cleaner testing, easier evolution, and a clear separation of concerns.

## What Changes

- Introduce an **application layer** with explicit input ports (use-case interfaces) and output ports (repository interfaces owned by the domain)
- Introduce a **domain layer** housing pure domain models and business rules, independent of JPA or Spring
- Move REST controllers to an **infrastructure/web** inbound adapter package; they depend on input ports, not repositories
- Move JPA repositories to an **infrastructure/persistence** outbound adapter package; they implement output ports
- Move configuration to **infrastructure/config**
- Delete the current `api/`, `model/`, and `repository/` flat packages

## Capabilities

### New Capabilities

- `backend-architecture`: Package structure and layering rules for the hexagonal backend — domain, application ports, and infrastructure adapters. Defines allowed dependency directions and the boundary contracts (ports) between layers.

### Modified Capabilities

## Impact

- All Kotlin source files under `backend/src/main/kotlin/com/endoadvice/` are restructured
- No change to the external REST API surface (paths, request/response shapes remain identical)
- No database migration required
- Tests in `backend/src/test/` will need package imports updated to match new locations
- Build file (`build.gradle.kts`) unchanged — no new dependencies
