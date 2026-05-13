package com.endoadvice.application.port.`in`

import com.endoadvice.domain.Supplement

interface ListSupplementsUseCase {
    fun listSupplements(): List<Supplement>
}
