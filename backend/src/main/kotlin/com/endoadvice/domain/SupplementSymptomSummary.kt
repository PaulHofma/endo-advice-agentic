package com.endoadvice.domain

data class SupplementSymptomSummary(
    val supplementId: Long,
    val symptomId: Long,
    val content: String,
    val evidenceStrength: String
)
