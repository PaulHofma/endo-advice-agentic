# Backend Architecture Spec

## Requirements

### Requirement: Domain layer is independent of frameworks
The domain package (`com.endoadvice.domain`) SHALL contain only plain Kotlin classes with no Spring, JPA, or other framework annotations. Domain model classes MAY use standard Kotlin library types only.

#### Scenario: Domain model has no JPA annotations
- **WHEN** a developer inspects any class in `com.endoadvice.domain`
- **THEN** the class MUST NOT import `javax.persistence`, `jakarta.persistence`, or any Spring annotation

#### Scenario: Domain model compiles without Spring or JPA on classpath
- **WHEN** the domain package classes are compiled in isolation (no Spring, no JPA on classpath)
- **THEN** compilation MUST succeed without errors

### Requirement: Input ports define use-case contracts
The application layer SHALL expose each use case as an interface in `com.endoadvice.application.port.in`. Controllers and other inbound adapters MUST depend on these interfaces, not on service implementations directly.

#### Scenario: Controller depends only on input port interface
- **WHEN** a REST controller requires a use case (e.g., list supplements)
- **THEN** the controller's constructor parameter type MUST be the input port interface, not the service class

#### Scenario: Input port interface has no infrastructure imports
- **WHEN** a developer inspects any interface in `com.endoadvice.application.port.in`
- **THEN** the interface MUST NOT import any class from `com.endoadvice.infrastructure`

### Requirement: Output ports define infrastructure contracts
The application layer SHALL define repository and other outbound dependency contracts as interfaces in `com.endoadvice.application.port.out`. Use-case services MUST depend on these interfaces. Spring Data JPA repositories MUST be confined to the infrastructure layer.

#### Scenario: Use-case service depends only on output port interface
- **WHEN** a use-case service in `com.endoadvice.application.service` needs to load data
- **THEN** its constructor parameter MUST be typed as an interface from `com.endoadvice.application.port.out`

#### Scenario: Spring Data JPA interfaces are in infrastructure only
- **WHEN** a developer searches for `JpaRepository` or `CrudRepository` usages
- **THEN** all usages MUST reside within `com.endoadvice.infrastructure.persistence`

### Requirement: Inbound adapters are confined to infrastructure web package
All REST controllers, DTOs, and HTTP-mapping code SHALL reside in `com.endoadvice.infrastructure.web`. No controller or DTO class SHALL exist outside this package.

#### Scenario: REST controller is in infrastructure.web
- **WHEN** a developer inspects all classes annotated with `@RestController`
- **THEN** every such class MUST be located in the `com.endoadvice.infrastructure.web` package

#### Scenario: DTO classes have no domain package imports for external APIs
- **WHEN** a developer inspects DTO data classes in `infrastructure.web`
- **THEN** DTOs MUST represent the API contract and be mapped from domain models, not be the domain models themselves

### Requirement: Outbound adapters are confined to infrastructure persistence package
All JPA entity classes, Spring Data repository interfaces, and persistence mapping code SHALL reside in `com.endoadvice.infrastructure.persistence`. No `@Entity`-annotated class SHALL exist outside this package.

#### Scenario: JPA entity is in infrastructure.persistence
- **WHEN** a developer searches for classes annotated with `@Entity`
- **THEN** every such class MUST be located in `com.endoadvice.infrastructure.persistence`

#### Scenario: Persistence adapter implements output port
- **WHEN** a persistence adapter class is created for a given repository port
- **THEN** the adapter class MUST implement the corresponding interface from `com.endoadvice.application.port.out`

### Requirement: External REST API surface is unchanged
The hexagonal refactor SHALL not alter any existing REST endpoint paths, HTTP methods, request parameters, or response shapes.

#### Scenario: GET /api/supplements returns same response shape
- **WHEN** a client calls `GET /api/supplements`
- **THEN** the response JSON structure and field names MUST be identical to the pre-refactor response

#### Scenario: GET /api/supplements/{id} returns same response shape
- **WHEN** a client calls `GET /api/supplements/{id}` with a valid id
- **THEN** the response JSON structure and field names MUST be identical to the pre-refactor response

#### Scenario: GET /api/symptoms returns same response shape
- **WHEN** a client calls `GET /api/symptoms`
- **THEN** the response JSON structure and field names MUST be identical to the pre-refactor response

#### Scenario: GET /api/symptoms/{slug}/supplements returns same response shape
- **WHEN** a client calls `GET /api/symptoms/{slug}/supplements` with a valid slug
- **THEN** the response JSON structure and field names MUST be identical to the pre-refactor response
