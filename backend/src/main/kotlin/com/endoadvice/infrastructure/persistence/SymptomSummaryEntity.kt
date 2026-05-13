package com.endoadvice.infrastructure.persistence

import jakarta.persistence.*
import java.time.Instant

@Entity
@Table(name = "symptom_summaries")
class SymptomSummaryEntity(
    @Id
    val symptomId: Long,

    @Column(nullable = false, columnDefinition = "TEXT")
    val content: String,

    @Column(nullable = false)
    val generatedAt: Instant = Instant.now()
)
