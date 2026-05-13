package com.endoadvice.application.port.`in`

import com.endoadvice.domain.Symptom

interface ListSymptomsUseCase {
    fun listSymptoms(): List<Symptom>
}
