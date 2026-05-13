package com.endoadvice.application.service

import com.endoadvice.application.port.input.GetSupplementDetailUseCase
import com.endoadvice.application.port.input.ListSupplementsUseCase
import com.endoadvice.application.port.output.SummaryPort
import com.endoadvice.application.port.output.SupplementPort
import com.endoadvice.domain.Supplement
import org.springframework.stereotype.Service

@Service
class SupplementService(
    private val supplementPort: SupplementPort,
    private val summaryPort: SummaryPort,
) : ListSupplementsUseCase, GetSupplementDetailUseCase {
    override fun listSupplements(): List<Supplement> = supplementPort.findAll()

    override fun getSupplementDetail(id: Long): Supplement? {
        val supplement = supplementPort.findById(id) ?: return null
        val supplementSummary = summaryPort.findSupplementSummary(id)
        val pairSummaries = summaryPort.findPairSummariesForSupplement(id)
        return supplement.copy(
            supplementSummary = supplementSummary,
            pairSummaries = pairSummaries,
        )
    }
}
