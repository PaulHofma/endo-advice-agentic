package com.endoadvice.domain

data class Supplement(
    val id: Long,
    val name: String,
    val summary: String,
    val findings: List<Finding> = emptyList()
)
