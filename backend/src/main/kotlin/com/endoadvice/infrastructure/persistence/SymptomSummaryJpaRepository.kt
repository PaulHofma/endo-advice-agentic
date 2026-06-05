package com.endoadvice.infrastructure.persistence

import org.springframework.data.jpa.repository.JpaRepository

interface SymptomSummaryJpaRepository : JpaRepository<SymptomSummaryEntity, Long>
