package com.endoadvice.infrastructure.persistence

import com.endoadvice.application.port.output.FindingPort
import com.endoadvice.domain.Citation
import com.endoadvice.domain.Finding
import com.endoadvice.domain.Symptom
import org.springframework.stereotype.Component
import org.springframework.transaction.annotation.Transactional

@Component
class FindingPersistenceAdapter(
    private val findingJpaRepository: FindingJpaRepository,
) : FindingPort {
    @Transactional(readOnly = true)
    override fun findBySymptomSlug(slug: String): List<Finding> = findingJpaRepository.findBySymptomSlug(slug).map { it.toDomain() }
}

private fun FindingEntity.toDomain() =
    Finding(
        id = id,
        supplementId = supplement.id,
        plainLanguageSummary = plainLanguageSummary,
        evidenceSnapshot = evidenceSnapshot,
        citations = citations.map { it.toDomain() },
        symptoms = symptoms.map { it.toDomain() },
        dosage = dosage,
        duration = duration,
        studyType = studyType,
        sampleSize = sampleSize,
        placeboControlled = placeboControlled,
        safetyNotes = safetyNotes,
    )

private fun CitationEntity.toDomain() =
    Citation(
        id = id,
        pmid = pmid,
        title = title,
        authors = authors,
        year = year,
        abstractExcerpt = abstractExcerpt,
    )

private fun SymptomEntity.toDomain() = Symptom(id = id, name = name, slug = slug)
