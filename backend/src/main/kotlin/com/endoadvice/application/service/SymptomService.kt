package com.endoadvice.application.service

import com.endoadvice.application.port.input.GetSupplementsForSymptomUseCase
import com.endoadvice.application.port.input.ListSymptomsUseCase
import com.endoadvice.application.port.output.FindingPort
import com.endoadvice.application.port.output.SummaryPort
import com.endoadvice.application.port.output.SupplementPort
import com.endoadvice.application.port.output.SymptomPort
import com.endoadvice.domain.Symptom
import com.endoadvice.domain.SymptomDetail
import org.springframework.stereotype.Service

@Service
class SymptomService(
    private val symptomPort: SymptomPort,
    private val findingPort: FindingPort,
    private val supplementPort: SupplementPort,
    private val summaryPort: SummaryPort,
) : ListSymptomsUseCase, GetSupplementsForSymptomUseCase {
    override fun listSymptoms(): List<Symptom> = symptomPort.findAll()

    override fun getSupplementsForSymptom(slug: String): SymptomDetail? {
        val symptom = symptomPort.findBySlug(slug) ?: return null
        val findings = findingPort.findBySymptomSlug(slug)
        val supplements =
            findings.map { it.supplementId }.distinct()
                .mapNotNull { supplementPort.findById(it) }
                .map { sup ->
                    val pairSummaries = summaryPort.findPairSummariesForSupplement(sup.id)
                    sup.copy(pairSummaries = pairSummaries)
                }
        val symptomSummary = summaryPort.findSymptomSummary(symptom.id)
        return SymptomDetail(
            symptom = symptom,
            symptomSummary = symptomSummary,
            supplements = supplements,
        )
    }
}
