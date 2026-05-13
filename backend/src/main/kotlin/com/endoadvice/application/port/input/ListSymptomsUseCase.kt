package com.endoadvice.application.port.input

import com.endoadvice.domain.Symptom

interface ListSymptomsUseCase {
    fun listSymptoms(): List<Symptom>
}
