package com.endoadvice.infrastructure.persistence

import jakarta.persistence.*
import java.time.Instant

@Entity
@Table(name = "supplement_summaries")
class SupplementSummaryEntity(
    @Id
    val supplementId: Long,

    @Column(nullable = false, columnDefinition = "TEXT")
    val content: String,

    @Column(nullable = false)
    val generatedAt: Instant = Instant.now()
)
