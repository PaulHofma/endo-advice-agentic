package com.endoadvice.infrastructure.web

import com.endoadvice.domain.Citation
import com.endoadvice.domain.Finding
import com.endoadvice.domain.Supplement
import com.endoadvice.domain.Symptom
import com.endoadvice.domain.SymptomDetail

data class SupplementSummaryDto(
    val id: Long,
    val name: String,
    val summary: String,
)

data class CitationDto(
    val id: Long,
    val pmid: String,
    val title: String,
    val authors: String,
    val year: Int,
    val abstractExcerpt: String,
    val pubmedUrl: String,
)

data class FindingDto(
    val id: Long,
    val plainLanguageSummary: String,
    val evidenceSnapshot: String,
    val citations: List<CitationDto>,
    val symptoms: List<SymptomSummaryDto>,
    val dosage: String?,
    val duration: String?,
    val studyType: String?,
    val sampleSize: Int?,
    val placeboControlled: Boolean?,
    val safetyNotes: String?,
)

data class SupplementSymptomSectionDto(
    val symptom: SymptomSummaryDto,
    val pairSummary: String?,
    val evidenceStrength: String?,
    val findings: List<FindingDto>,
)

data class SupplementDetailDto(
    val id: Long,
    val name: String,
    val summary: String,
    val supplementSummary: String?,
    val symptomSections: List<SupplementSymptomSectionDto>,
)

data class SymptomSummaryDto(
    val id: Long,
    val name: String,
    val slug: String,
)

data class SymptomSupplementSectionDto(
    val supplement: SupplementSummaryDto,
    val pairSummary: String?,
    val evidenceStrength: String?,
    val findings: List<FindingDto>,
)

data class SymptomDetailResponseDto(
    val symptomSummary: String?,
    val supplements: List<SymptomSupplementSectionDto>,
)

fun Supplement.toSummaryDto() = SupplementSummaryDto(id, name, summary)

fun Citation.toDto() =
    CitationDto(
        id = id,
        pmid = pmid,
        title = title,
        authors = authors,
        year = year,
        abstractExcerpt = abstractExcerpt,
        pubmedUrl = "https://pubmed.ncbi.nlm.nih.gov/$pmid/",
    )

fun Symptom.toSummaryDto() = SymptomSummaryDto(id, name, slug)

fun Finding.toDto() =
    FindingDto(
        id = id,
        plainLanguageSummary = plainLanguageSummary,
        evidenceSnapshot = evidenceSnapshot,
        citations = citations.map { it.toDto() },
        symptoms = symptoms.map { it.toSummaryDto() },
        dosage = dosage,
        duration = duration,
        studyType = studyType,
        sampleSize = sampleSize,
        placeboControlled = placeboControlled,
        safetyNotes = safetyNotes,
    )

fun Supplement.toDetailDto(): SupplementDetailDto {
    val pairBySymptom = pairSummaries.associateBy { it.symptomId }
    val findingsBySymptom =
        findings.flatMap { f ->
            f.symptoms.map { s -> s to f }
        }.groupBy({ it.first }, { it.second })

    val symptomSections =
        findingsBySymptom.entries.map { (symptom, sFindings) ->
            val pair = pairBySymptom[symptom.id]
            SupplementSymptomSectionDto(
                symptom = symptom.toSummaryDto(),
                pairSummary = pair?.content,
                evidenceStrength = pair?.evidenceStrength,
                findings = sFindings.map { it.toDto() },
            )
        }

    // Include findings with no symptom in an "Other" section if present
    val findingsWithNoSymptom = findings.filter { it.symptoms.isEmpty() }
    val allSections =
        if (findingsWithNoSymptom.isNotEmpty()) {
            symptomSections +
                SupplementSymptomSectionDto(
                    symptom = SymptomSummaryDto(id = 0, name = "Other", slug = "other"),
                    pairSummary = null,
                    evidenceStrength = null,
                    findings = findingsWithNoSymptom.map { it.toDto() },
                )
        } else {
            symptomSections
        }

    return SupplementDetailDto(
        id = id,
        name = name,
        summary = summary,
        supplementSummary = supplementSummary,
        symptomSections = allSections,
    )
}

fun SymptomDetail.toResponseDto(): SymptomDetailResponseDto {
    val supplementSections =
        supplements.map { sup ->
            val pairForThisSymptom = sup.pairSummaries.firstOrNull { it.symptomId == symptom.id }
            val findingsForSymptom =
                sup.findings.filter { f ->
                    f.symptoms.any { s -> s.id == symptom.id }
                }
            SymptomSupplementSectionDto(
                supplement = sup.toSummaryDto(),
                pairSummary = pairForThisSymptom?.content,
                evidenceStrength = pairForThisSymptom?.evidenceStrength,
                findings = findingsForSymptom.map { it.toDto() },
            )
        }
    return SymptomDetailResponseDto(
        symptomSummary = symptomSummary,
        supplements = supplementSections,
    )
}
