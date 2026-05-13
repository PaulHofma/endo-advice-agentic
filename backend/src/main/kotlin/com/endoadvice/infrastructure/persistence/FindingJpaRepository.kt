package com.endoadvice.infrastructure.persistence

import org.springframework.data.jpa.repository.JpaRepository
import org.springframework.data.jpa.repository.Query

interface FindingJpaRepository : JpaRepository<FindingEntity, Long> {
    @Query(
        """
        SELECT DISTINCT f FROM Finding f
        JOIN f.symptoms sy
        WHERE sy.slug = :slug
    """,
    )
    fun findBySymptomSlug(slug: String): List<FindingEntity>
}
