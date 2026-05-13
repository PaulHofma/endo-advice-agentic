package com.endoadvice.application.port.out

import com.endoadvice.domain.Supplement

interface SupplementPort {
    fun findAll(): List<Supplement>
    fun findById(id: Long): Supplement?
}
