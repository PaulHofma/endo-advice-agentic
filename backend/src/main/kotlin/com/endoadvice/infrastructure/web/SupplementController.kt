package com.endoadvice.infrastructure.web

import com.endoadvice.application.port.`in`.GetSupplementDetailUseCase
import com.endoadvice.application.port.`in`.ListSupplementsUseCase
import org.springframework.http.ResponseEntity
import org.springframework.web.bind.annotation.*

@RestController
@RequestMapping("/api/supplements")
class SupplementController(
    private val listSupplementsUseCase: ListSupplementsUseCase,
    private val getSupplementDetailUseCase: GetSupplementDetailUseCase
) {

    @GetMapping
    fun listSupplements(): List<SupplementSummaryDto> =
        listSupplementsUseCase.listSupplements().map { it.toSummaryDto() }

    @GetMapping("/{id}")
    fun getSupplementDetail(@PathVariable id: Long): ResponseEntity<SupplementDetailDto> {
        val supplement = getSupplementDetailUseCase.getSupplementDetail(id)
            ?: return ResponseEntity.notFound().build()
        return ResponseEntity.ok(supplement.toDetailDto())
    }
}
