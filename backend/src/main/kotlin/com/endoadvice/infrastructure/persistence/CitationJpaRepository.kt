package com.endoadvice.infrastructure.persistence

import org.springframework.data.jpa.repository.JpaRepository

interface CitationJpaRepository : JpaRepository<CitationEntity, Long>
