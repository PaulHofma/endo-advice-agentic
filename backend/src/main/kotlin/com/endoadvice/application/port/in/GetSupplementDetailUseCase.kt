package com.endoadvice.application.port.`in`

import com.endoadvice.domain.Supplement

interface GetSupplementDetailUseCase {
    fun getSupplementDetail(id: Long): Supplement?
}
