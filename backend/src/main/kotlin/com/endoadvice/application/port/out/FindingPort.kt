package com.endoadvice.application.port.out

import com.endoadvice.domain.Finding

interface FindingPort {
    fun findBySymptomSlug(slug: String): List<Finding>
}
