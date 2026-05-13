package com.endoadvice.infrastructure.persistence

import com.endoadvice.application.port.output.SymptomPort
import com.endoadvice.domain.Symptom
import org.springframework.stereotype.Component

@Component
class SymptomPersistenceAdapter(
    private val symptomJpaRepository: SymptomJpaRepository,
) : SymptomPort {
    override fun findAll(): List<Symptom> = symptomJpaRepository.findAllWithFindings().map { it.toDomain() }

    override fun findBySlug(slug: String): Symptom? = symptomJpaRepository.findBySlug(slug)?.toDomain()
}

private fun SymptomEntity.toDomain() = Symptom(id = id, name = name, slug = slug)
