package com.endoadvice.application.port.input

import com.endoadvice.domain.Supplement

interface ListSupplementsUseCase {
    fun listSupplements(): List<Supplement>
}
