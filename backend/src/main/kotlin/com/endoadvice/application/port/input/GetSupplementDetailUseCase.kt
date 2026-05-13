package com.endoadvice.application.port.input

import com.endoadvice.domain.Supplement

interface GetSupplementDetailUseCase {
    fun getSupplementDetail(id: Long): Supplement?
}
