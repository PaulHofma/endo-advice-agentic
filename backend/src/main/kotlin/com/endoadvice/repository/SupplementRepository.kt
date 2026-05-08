package com.endoadvice.repository

import com.endoadvice.model.Supplement
import org.springframework.data.jpa.repository.JpaRepository
import org.springframework.data.jpa.repository.Query

interface SupplementRepository : JpaRepository<Supplement, Long> {

    @Query("SELECT DISTINCT s FROM Supplement s WHERE EXISTS (SELECT f FROM Finding f WHERE f.supplement = s)")
    fun findAllWithFindings(): List<Supplement>
}
