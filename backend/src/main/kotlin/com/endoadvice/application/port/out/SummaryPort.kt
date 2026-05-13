package com.endoadvice.application.port.out

import com.endoadvice.domain.SupplementSymptomSummary

interface SummaryPort {
    fun findSupplementSummary(supplementId: Long): String?
    fun findSymptomSummary(symptomId: Long): String?
    fun findPairSummariesForSupplement(supplementId: Long): List<SupplementSymptomSummary>
    fun findPairSummariesForSymptom(symptomId: Long): List<SupplementSymptomSummary>
}
