package com.endoadvice.infrastructure.persistence

import org.springframework.data.jpa.repository.JpaRepository
import org.springframework.data.jpa.repository.Query

interface SymptomJpaRepository : JpaRepository<SymptomEntity, Long> {

    @Query("""
        SELECT DISTINCT sy FROM Symptom sy
        WHERE EXISTS (
            SELECT f FROM Finding f
            JOIN f.symptoms s WHERE s = sy
        )
    """)
    fun findAllWithFindings(): List<SymptomEntity>

    fun findBySlug(slug: String): SymptomEntity?
}
