package com.endoadvice.application.port.input

import com.endoadvice.domain.SymptomDetail

interface GetSupplementsForSymptomUseCase {
    fun getSupplementsForSymptom(slug: String): SymptomDetail?
}
