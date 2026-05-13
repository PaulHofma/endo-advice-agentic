package com.endoadvice.application.port.`in`

import com.endoadvice.domain.Supplement

interface GetSupplementsForSymptomUseCase {
    fun getSupplementsForSymptom(slug: String): List<Supplement>?
}
