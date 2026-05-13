package com.endoadvice.infrastructure.persistence

import jakarta.persistence.*
import java.io.Serializable
import java.time.Instant

@Embeddable
data class SupplementSymptomSummaryId(
    val supplementId: Long = 0,
    val symptomId: Long = 0
) : Serializable

@Entity
@Table(name = "supplement_symptom_summaries")
class SupplementSymptomSummaryEntity(
    @EmbeddedId
    val id: SupplementSymptomSummaryId,

    @Column(nullable = false, columnDefinition = "TEXT")
    val content: String,

    @Column(nullable = false, length = 20)
    val evidenceStrength: String,

    @Column(nullable = false)
    val generatedAt: Instant = Instant.now()
)
