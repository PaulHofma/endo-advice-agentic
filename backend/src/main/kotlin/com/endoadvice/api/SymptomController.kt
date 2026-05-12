package com.endoadvice.api

import com.endoadvice.repository.FindingRepository
import com.endoadvice.repository.SupplementRepository
import com.endoadvice.repository.SymptomRepository
import org.springframework.http.ResponseEntity
import org.springframework.transaction.annotation.Transactional
import org.springframework.web.bind.annotation.*

@RestController
@RequestMapping("/api/symptoms")
class SymptomController(
    private val symptomRepository: SymptomRepository,
    private val supplementRepository: SupplementRepository,
    private val findingRepository: FindingRepository
) {

    @GetMapping
    fun listSymptoms(): List<SymptomSummaryDto> =
        symptomRepository.findAllWithFindings().map { it.toSummaryDto() }

    @GetMapping("/{slug}/supplements")
    @Transactional(readOnly = true)
    fun getSupplementsForSymptom(@PathVariable slug: String): ResponseEntity<List<SupplementDetailDto>> {
        symptomRepository.findBySlug(slug) ?: return ResponseEntity.notFound().build()

        val findings = findingRepository.findBySymptomSlug(slug)
        val supplements = findings.map { it.supplement }.distinctBy { it.id }
        return ResponseEntity.ok(supplements.map { it.toDetailDto() })
    }
}
