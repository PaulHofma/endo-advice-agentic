## Context

The backend is a Kotlin/Spring Boot 3 application currently structured as a flat three-layer monolith:

```
com.endoadvice.api          → REST controllers + DTOs (directly inject repositories)
com.endoadvice.model        → JPA entities
com.endoadvice.repository   → Spring Data JPA interfaces
com.endoadvice.config       → CORS configuration
```

Controllers own all mapping logic and call repositories directly. There is no application layer, no explicit ports, and no seam for testing business logic without the database. The domain objects are JPA entities — coupling persistence annotations into the domain.

## Goals / Non-Goals

**Goals:**
- Restructure packages to express hexagonal layers: domain, application, and infrastructure
- Define explicit input ports (use-case interfaces) and output ports (repository interfaces) owned by the application core
- Make the application core (domain + application layers) independent of Spring and JPA annotations
- Keep the external REST API surface identical — no URL, request, or response shape changes
- Retain all existing test coverage with only import updates needed

**Non-Goals:**
- Adding new API endpoints or business features
- Changing the database schema
- Migrating JPA entities to annotation-free domain objects (out of scope; JPA annotations remain on entities in the infrastructure layer or mapped to domain objects there)
- Introducing CQRS, event sourcing, or other advanced patterns

## Decisions

### D1 — Package structure mirrors hexagonal layers

**Decision**: Reorganise all source under three top-level packages:

```
com.endoadvice.domain            → Pure domain models (no framework deps)
com.endoadvice.application       → Use cases (input ports) + output port interfaces
  .port.in                       → Input port interfaces (use-case contracts)
  .port.out                      → Output port interfaces (what infra the app needs)
  .service                       → Use-case implementations (orchestrate domain + call output ports)
com.endoadvice.infrastructure    → All framework/library-specific code
  .web                           → REST controllers + DTOs (inbound adapters)
  .persistence                   → JPA entities, Spring Data repos, outbound adapter impls
  .config                        → Spring configuration beans
```

**Alternatives considered:**
- Keep flat structure, add a service layer only → Cheaper but doesn't express port contracts; controllers still depend on Spring Data interfaces directly.
- Use `hexagonal` / `adapters` top-level names → Non-standard; `infrastructure` is conventional for Spring projects.

### D2 — Domain models are plain Kotlin classes; JPA entities live in infrastructure

**Decision**: `com.endoadvice.domain` holds plain `data class` or open-class domain models with no JPA annotations. JPA entity classes (annotated with `@Entity`) live in `infrastructure.persistence` and map to/from domain models in the outbound adapter.

**Alternatives considered:**
- Annotate domain classes with JPA directly → Common pragmatic shortcut but couples the domain to Hibernate; violated the core constraint of hexagonal arch.

### D3 — Input ports are interfaces; use-case services implement them

**Decision**: Each logical use case (e.g., `ListSupplements`, `GetSupplementDetail`, `ListSymptoms`, `GetSupplementsForSymptom`) becomes an interface in `application.port.in`. A Spring `@Service` class in `application.service` implements those interfaces and calls output ports.

**Alternatives considered:**
- Skip input port interfaces, have controllers call services directly → Fine for small apps; interfaces make the boundary explicit and mockable without Spring context.

### D4 — Output ports are interfaces in the application layer; JPA repos implement them

**Decision**: Output port interfaces (e.g., `SupplementRepository`, `SymptomRepository`, `FindingRepository`) are defined in `application.port.out`. The Spring Data JPA interfaces in `infrastructure.persistence` either extend them or dedicated adapter classes delegate to them.

**Alternatives considered:**
- Re-use Spring Data repository interfaces as the port → Leaks Spring's `JpaRepository` type into the application layer, breaking infrastructure independence.

## Risks / Trade-offs

- **More files for the same behaviour** → The refactor adds boilerplate (port interfaces, mapping logic). Mitigation: the boundaries are small now; the overhead is proportional to the codebase.
- **JPA entity ↔ domain model mapping** → Two representations of the same data require mapping code. Mitigation: keep mappers co-located with persistence adapters; use simple extension functions.
- **Test import churn** → All existing tests will need import updates. Mitigation: only import paths change; logic is identical.
- **Risk of accidental regressions during move** → Files get renamed and moved. Mitigation: run `./gradlew test` at each phase before proceeding.

## Migration Plan

The refactor is performed as a sequence of phases, each independently buildable and testable:

1. Create new package directories; add domain model classes (plain Kotlin)
2. Define output port interfaces in `application.port.out`
3. Create use-case input port interfaces in `application.port.in`
4. Write use-case service implementations in `application.service`
5. Move and adapt infrastructure persistence (JPA entities + repo adapters) to `infrastructure.persistence`
6. Move and adapt REST controllers + DTOs to `infrastructure.web`
7. Move config to `infrastructure.config`
8. Delete old `api/`, `model/`, `repository/` packages
9. Update test imports; run full test suite

**Rollback**: This is a source-level refactor with no runtime or schema changes. Any phase can be rolled back via git.

## Open Questions

- None — scope is well-defined; all decisions made above.
