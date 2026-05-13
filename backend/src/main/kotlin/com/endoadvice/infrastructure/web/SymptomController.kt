package com.endoadvice.infrastructure.web

import com.endoadvice.application.port.input.GetSupplementsForSymptomUseCase
import com.endoadvice.application.port.input.ListSymptomsUseCase
import org.springframework.http.ResponseEntity
import org.springframework.web.bind.annotation.*

@RestController
@RequestMapping("/api/symptoms")
class SymptomController(
    private val listSymptomsUseCase: ListSymptomsUseCase,
    private val getSupplementsForSymptomUseCase: GetSupplementsForSymptomUseCase,
) {
    @GetMapping
    fun listSymptoms(): List<SymptomSummaryDto> = listSymptomsUseCase.listSymptoms().map { it.toSummaryDto() }

    @GetMapping("/{slug}/supplements")
    fun getSupplementsForSymptom(
        @PathVariable slug: String,
    ): ResponseEntity<SymptomDetailResponseDto> {
        val detail =
            getSupplementsForSymptomUseCase.getSupplementsForSymptom(slug)
                ?: return ResponseEntity.notFound().build()
        return ResponseEntity.ok(detail.toResponseDto())
    }
}
