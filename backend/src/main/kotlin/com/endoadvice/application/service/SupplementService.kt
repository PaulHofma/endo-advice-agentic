package com.endoadvice.application.service

import com.endoadvice.application.port.`in`.GetSupplementDetailUseCase
import com.endoadvice.application.port.`in`.ListSupplementsUseCase
import com.endoadvice.application.port.out.SupplementPort
import com.endoadvice.domain.Supplement
import org.springframework.stereotype.Service

@Service
class SupplementService(private val supplementPort: SupplementPort) :
    ListSupplementsUseCase,
    GetSupplementDetailUseCase {

    override fun listSupplements(): List<Supplement> = supplementPort.findAll()

    override fun getSupplementDetail(id: Long): Supplement? = supplementPort.findById(id)
}
