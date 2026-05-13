package com.endoadvice.infrastructure.persistence

import org.springframework.data.jpa.repository.JpaRepository
import org.springframework.data.jpa.repository.Query

interface SupplementJpaRepository : JpaRepository<SupplementEntity, Long> {
    @Query("SELECT DISTINCT s FROM Supplement s WHERE EXISTS (SELECT f FROM Finding f WHERE f.supplement = s)")
    fun findAllWithFindings(): List<SupplementEntity>
}
