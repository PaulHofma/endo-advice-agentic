package com.endoadvice.infrastructure.persistence

import com.endoadvice.application.port.out.SummaryPort
import com.endoadvice.domain.SupplementSymptomSummary
import org.springframework.stereotype.Component

@Component
class SummaryPersistenceAdapter(
    private val supplementSummaryJpaRepository: SupplementSummaryJpaRepository,
    private val symptomSummaryJpaRepository: SymptomSummaryJpaRepository,
    private val pairSummaryJpaRepository: SupplementSymptomSummaryJpaRepository
) : SummaryPort {

    override fun findSupplementSummary(supplementId: Long): String? =
        supplementSummaryJpaRepository.findById(supplementId).orElse(null)?.content

    override fun findSymptomSummary(symptomId: Long): String? =
        symptomSummaryJpaRepository.findById(symptomId).orElse(null)?.content

    override fun findPairSummariesForSupplement(supplementId: Long): List<SupplementSymptomSummary> =
        pairSummaryJpaRepository.findAllByIdSupplementId(supplementId).map { it.toDomain() }

    override fun findPairSummariesForSymptom(symptomId: Long): List<SupplementSymptomSummary> =
        pairSummaryJpaRepository.findAllByIdSymptomId(symptomId).map { it.toDomain() }
}

private fun SupplementSymptomSummaryEntity.toDomain() = SupplementSymptomSummary(
    supplementId = id.supplementId,
    symptomId = id.symptomId,
    content = content,
    evidenceStrength = evidenceStrength
)
