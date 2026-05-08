package com.endoadvice.repository

import com.endoadvice.model.Symptom
import org.springframework.data.jpa.repository.JpaRepository
import org.springframework.data.jpa.repository.Query

interface SymptomRepository : JpaRepository<Symptom, Long> {

    @Query("""
        SELECT DISTINCT sy FROM Symptom sy
        WHERE EXISTS (
            SELECT f FROM Finding f
            JOIN f.symptoms s WHERE s = sy
        )
    """)
    fun findAllWithFindings(): List<Symptom>

    fun findBySlug(slug: String): Symptom?
}
