package com.endoadvice.api

import com.endoadvice.model.Citation
import com.endoadvice.model.Finding
import com.endoadvice.model.Supplement
import com.endoadvice.model.Symptom

data class SupplementSummaryDto(
    val id: Long,
    val name: String,
    val summary: String
)

data class CitationDto(
    val id: Long,
    val pmid: String,
    val title: String,
    val authors: String,
    val year: Int,
    val abstractExcerpt: String,
    val pubmedUrl: String
)

data class FindingDto(
    val id: Long,
    val plainLanguageSummary: String,
    val evidenceSnapshot: String,
    val citations: List<CitationDto>,
    val symptoms: List<SymptomSummaryDto>
)

data class SupplementDetailDto(
    val id: Long,
    val name: String,
    val summary: String,
    val findings: List<FindingDto>
)

data class SymptomSummaryDto(
    val id: Long,
    val name: String,
    val slug: String
)

fun Supplement.toSummaryDto() = SupplementSummaryDto(id, name, summary)

fun Citation.toDto() = CitationDto(
    id = id,
    pmid = pmid,
    title = title,
    authors = authors,
    year = year,
    abstractExcerpt = abstractExcerpt,
    pubmedUrl = "https://pubmed.ncbi.nlm.nih.gov/$pmid/"
)

fun Symptom.toSummaryDto() = SymptomSummaryDto(id, name, slug)

fun Finding.toDto() = FindingDto(
    id = id,
    plainLanguageSummary = plainLanguageSummary,
    evidenceSnapshot = evidenceSnapshot,
    citations = citations.map { it.toDto() },
    symptoms = symptoms.map { it.toSummaryDto() }
)

fun Supplement.toDetailDto() = SupplementDetailDto(
    id = id,
    name = name,
    summary = summary,
    findings = findings.map { it.toDto() }
)
