package com.endoadvice.application.port.`in`

import com.endoadvice.domain.SymptomDetail

interface GetSupplementsForSymptomUseCase {
    fun getSupplementsForSymptom(slug: String): SymptomDetail?
}
