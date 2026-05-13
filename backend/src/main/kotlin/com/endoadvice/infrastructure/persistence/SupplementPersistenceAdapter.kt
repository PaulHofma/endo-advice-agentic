package com.endoadvice.infrastructure.persistence

import com.endoadvice.application.port.out.SupplementPort
import com.endoadvice.domain.Citation
import com.endoadvice.domain.Finding
import com.endoadvice.domain.Supplement
import com.endoadvice.domain.Symptom
import org.springframework.stereotype.Component
import org.springframework.transaction.annotation.Transactional

@Component
class SupplementPersistenceAdapter(
    private val supplementJpaRepository: SupplementJpaRepository
) : SupplementPort {

    override fun findAll(): List<Supplement> =
        supplementJpaRepository.findAllWithFindings().map { it.toDomain() }

    @Transactional(readOnly = true)
    override fun findById(id: Long): Supplement? =
        supplementJpaRepository.findById(id).orElse(null)?.toDomainWithFindings()
}

private fun SupplementEntity.toDomain() = Supplement(id = id, name = name, summary = summary)

private fun SupplementEntity.toDomainWithFindings() = Supplement(
    id = id,
    name = name,
    summary = summary,
    findings = findings.map { it.toDomain() }
)

private fun FindingEntity.toDomain() = Finding(
    id = id,
    supplementId = supplement.id,
    plainLanguageSummary = plainLanguageSummary,
    evidenceSnapshot = evidenceSnapshot,
    citations = citations.map { it.toDomain() },
    symptoms = symptoms.map { it.toDomain() }
)

private fun CitationEntity.toDomain() = Citation(
    id = id,
    pmid = pmid,
    title = title,
    authors = authors,
    year = year,
    abstractExcerpt = abstractExcerpt
)

private fun SymptomEntity.toDomain() = Symptom(id = id, name = name, slug = slug)
