package com.endoadvice.api

import com.endoadvice.repository.SupplementRepository
import org.springframework.http.ResponseEntity
import org.springframework.transaction.annotation.Transactional
import org.springframework.web.bind.annotation.*

@RestController
@RequestMapping("/api/supplements")
class SupplementController(private val supplementRepository: SupplementRepository) {

    @GetMapping
    fun listSupplements(): List<SupplementSummaryDto> =
        supplementRepository.findAllWithFindings().map { it.toSummaryDto() }

    @GetMapping("/{id}")
    @Transactional(readOnly = true)
    fun getSupplementDetail(@PathVariable id: Long): ResponseEntity<SupplementDetailDto> {
        val supplement = supplementRepository.findById(id).orElse(null)
            ?: return ResponseEntity.notFound().build()
        return ResponseEntity.ok(supplement.toDetailDto())
    }
}
