package com.endoadvice.domain

data class Citation(
    val id: Long,
    val pmid: String,
    val title: String,
    val authors: String,
    val year: Int,
    val abstractExcerpt: String
)
