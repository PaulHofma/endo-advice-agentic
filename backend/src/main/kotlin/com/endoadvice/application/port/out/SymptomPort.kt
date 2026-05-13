package com.endoadvice.application.port.out

import com.endoadvice.domain.Symptom

interface SymptomPort {
    fun findAll(): List<Symptom>
    fun findBySlug(slug: String): Symptom?
}
