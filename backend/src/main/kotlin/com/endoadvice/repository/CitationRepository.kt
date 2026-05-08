package com.endoadvice.repository

import com.endoadvice.model.Citation
import org.springframework.data.jpa.repository.JpaRepository

interface CitationRepository : JpaRepository<Citation, Long>
