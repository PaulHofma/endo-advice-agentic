package com.endoadvice.domain

data class SymptomDetail(
    val symptom: Symptom,
    val symptomSummary: String?,
    val supplements: List<Supplement>
)
