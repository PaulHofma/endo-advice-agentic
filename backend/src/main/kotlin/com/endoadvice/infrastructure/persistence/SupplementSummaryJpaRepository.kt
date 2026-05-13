package com.endoadvice.infrastructure.persistence

import org.springframework.data.jpa.repository.JpaRepository

interface SupplementSummaryJpaRepository :
    JpaRepository<SupplementSummaryEntity, Long>
