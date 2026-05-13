package com.endoadvice.application.port.output

import com.endoadvice.domain.Finding

interface FindingPort {
    fun findBySymptomSlug(slug: String): List<Finding>
}
