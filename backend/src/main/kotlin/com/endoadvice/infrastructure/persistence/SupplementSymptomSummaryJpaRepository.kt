package com.endoadvice.infrastructure.persistence

import org.springframework.data.jpa.repository.JpaRepository

interface SupplementSymptomSummaryJpaRepository :
    JpaRepository<SupplementSymptomSummaryEntity, SupplementSymptomSummaryId> {

    fun findAllByIdSupplementId(supplementId: Long): List<SupplementSymptomSummaryEntity>
    fun findAllByIdSymptomId(symptomId: Long): List<SupplementSymptomSummaryEntity>
}
