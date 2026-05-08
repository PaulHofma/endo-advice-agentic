## 1. Domain Layer

- [ ] 1.1 Create `com.endoadvice.domain` package; add plain Kotlin `Supplement` domain model (id, name, summary)
- [ ] 1.2 Add plain Kotlin `Finding` domain model (id, plainLanguageSummary, evidenceSnapshot, citations, symptoms)
- [ ] 1.3 Add plain Kotlin `Symptom` domain model (id, name, slug)
- [ ] 1.4 Add plain Kotlin `Citation` domain model (id, pmid, title, authors, year, abstractExcerpt)
- [ ] 1.5 Verify domain classes have zero Spring/JPA imports

## 2. Output Ports

- [ ] 2.1 Create `com.endoadvice.application.port.out` package; add `SupplementPort` interface with `findAll(): List<Supplement>` and `findById(id: Long): Supplement?`
- [ ] 2.2 Add `SymptomPort` interface with `findAll(): List<Symptom>` and `findBySlug(slug: String): Symptom?`
- [ ] 2.3 Add `FindingPort` interface with `findBySymptomSlug(slug: String): List<Finding>`
- [ ] 2.4 Verify output port interfaces have no infrastructure imports

## 3. Input Ports (Use-Case Interfaces)

- [ ] 3.1 Create `com.endoadvice.application.port.in` package; add `ListSupplementsUseCase` interface returning `List<Supplement>`
- [ ] 3.2 Add `GetSupplementDetailUseCase` interface accepting `id: Long` and returning `Supplement?`
- [ ] 3.3 Add `ListSymptomsUseCase` interface returning `List<Symptom>`
- [ ] 3.4 Add `GetSupplementsForSymptomUseCase` interface accepting `slug: String` and returning `List<Supplement>?` (null when symptom not found)
- [ ] 3.5 Verify input port interfaces have no infrastructure imports

## 4. Use-Case Services

- [ ] 4.1 Create `com.endoadvice.application.service` package; add `SupplementService` annotated `@Service`, implementing `ListSupplementsUseCase` and `GetSupplementDetailUseCase`, injecting `SupplementPort`
- [ ] 4.2 Add `SymptomService` annotated `@Service`, implementing `ListSymptomsUseCase` and `GetSupplementsForSymptomUseCase`, injecting `SymptomPort` and `FindingPort`
- [ ] 4.3 Run `./gradlew compileKotlin` to confirm application layer compiles cleanly

## 5. Persistence Adapters

- [ ] 5.1 Create `com.endoadvice.infrastructure.persistence` package; migrate JPA `Supplement` entity (rename to `SupplementEntity` or keep as `Supplement` within the package), retaining all JPA annotations
- [ ] 5.2 Migrate JPA `Finding`, `Symptom`, `Citation` entities to `infrastructure.persistence` the same way
- [ ] 5.3 Migrate Spring Data repository interfaces (`SupplementRepository`, `SymptomRepository`, `FindingRepository`, `CitationRepository`) to `infrastructure.persistence`
- [ ] 5.4 Create `SupplementPersistenceAdapter` implementing `SupplementPort`; add entity-to-domain mapping functions
- [ ] 5.5 Create `SymptomPersistenceAdapter` implementing `SymptomPort`; add entity-to-domain mapping
- [ ] 5.6 Create `FindingPersistenceAdapter` implementing `FindingPort`; add entity-to-domain mapping
- [ ] 5.7 Run `./gradlew compileKotlin` to confirm persistence layer compiles cleanly

## 6. Web Adapters (Controllers + DTOs)

- [ ] 6.1 Create `com.endoadvice.infrastructure.web` package; migrate DTOs from `api/Dtos.kt`, updating mapping functions to use domain models instead of JPA entities
- [ ] 6.2 Migrate `SupplementController` to `infrastructure.web`; update constructor to inject `ListSupplementsUseCase` and `GetSupplementDetailUseCase` input ports
- [ ] 6.3 Migrate `SymptomController` to `infrastructure.web`; update constructor to inject `ListSymptomsUseCase` and `GetSupplementsForSymptomUseCase` input ports
- [ ] 6.4 Run `./gradlew compileKotlin` to confirm web layer compiles cleanly

## 7. Configuration

- [ ] 7.1 Create `com.endoadvice.infrastructure.config` package; migrate `CorsConfig` from `config/`
- [ ] 7.2 Confirm `EndoAdviceApplication.kt` component-scan still covers all new packages (Spring Boot auto-configuration should handle this; verify)

## 8. Cleanup

- [ ] 8.1 Delete old `com.endoadvice.api` package (controllers, DTOs)
- [ ] 8.2 Delete old `com.endoadvice.model` package (JPA entities)
- [ ] 8.3 Delete old `com.endoadvice.repository` package
- [ ] 8.4 Delete old `com.endoadvice.config` package
- [ ] 8.5 Run `./gradlew compileKotlin` to confirm no dangling references

## 9. Tests

- [ ] 9.1 Update import statements in `SupplementControllerTest` and `SymptomControllerTest` to reference new package locations
- [ ] 9.2 Run `./gradlew test` and confirm all tests pass with zero failures
- [ ] 9.3 Verify API response shapes are unchanged by inspecting test assertions (enforce spec requirement: external surface identical)
