package com.endoadvice.repository

import com.endoadvice.model.Finding
import org.springframework.data.jpa.repository.JpaRepository
import org.springframework.data.jpa.repository.Query

interface FindingRepository : JpaRepository<Finding, Long> {

    @Query("""
        SELECT DISTINCT f FROM Finding f
        JOIN f.symptoms sy
        WHERE sy.slug = :slug
    """)
    fun findBySymptomSlug(slug: String): List<Finding>
}
