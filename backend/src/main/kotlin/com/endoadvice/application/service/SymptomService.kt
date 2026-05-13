package com.endoadvice.application.service

import com.endoadvice.application.port.`in`.GetSupplementsForSymptomUseCase
import com.endoadvice.application.port.`in`.ListSymptomsUseCase
import com.endoadvice.application.port.out.FindingPort
import com.endoadvice.application.port.out.SupplementPort
import com.endoadvice.application.port.out.SymptomPort
import com.endoadvice.domain.Supplement
import com.endoadvice.domain.Symptom
import org.springframework.stereotype.Service

@Service
class SymptomService(
    private val symptomPort: SymptomPort,
    private val findingPort: FindingPort,
    private val supplementPort: SupplementPort
) : ListSymptomsUseCase, GetSupplementsForSymptomUseCase {

    override fun listSymptoms(): List<Symptom> = symptomPort.findAll()

    override fun getSupplementsForSymptom(slug: String): List<Supplement>? {
        symptomPort.findBySlug(slug) ?: return null
        val findings = findingPort.findBySymptomSlug(slug)
        return findings.map { it.supplementId }.distinct()
            .mapNotNull { supplementPort.findById(it) }
    }
}
