package com.endoadvice.domain

data class Finding(
    val id: Long,
    val supplementId: Long,
    val plainLanguageSummary: String,
    val evidenceSnapshot: String,
    val citations: List<Citation> = emptyList(),
    val symptoms: List<Symptom> = emptyList(),
    val dosage: String? = null,
    val duration: String? = null,
    val studyType: String? = null,
    val sampleSize: Int? = null,
    val placeboControlled: Boolean? = null,
    val safetyNotes: String? = null,
)
