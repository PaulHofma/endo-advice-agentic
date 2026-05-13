package com.endoadvice.infrastructure.persistence

import jakarta.persistence.*

@Entity(name = "Citation")
@Table(name = "citations")
class CitationEntity(
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    val id: Long = 0,
    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "finding_id", nullable = false)
    val finding: FindingEntity,
    @Column(nullable = false, length = 20)
    val pmid: String,
    @Column(nullable = false, columnDefinition = "TEXT")
    val title: String,
    @Column(nullable = false, columnDefinition = "TEXT")
    val authors: String,
    @Column(nullable = false)
    val year: Int,
    @Column(nullable = false, columnDefinition = "TEXT")
    val abstractExcerpt: String,
)
