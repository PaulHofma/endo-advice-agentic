package com.endoadvice.infrastructure.persistence

import jakarta.persistence.*
import java.time.Instant

@Entity(name = "Finding")
@Table(name = "findings")
class FindingEntity(
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    val id: Long = 0,

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "supplement_id", nullable = false)
    val supplement: SupplementEntity,

    @Column(nullable = false, columnDefinition = "TEXT")
    val plainLanguageSummary: String,

    @Column(nullable = false, columnDefinition = "TEXT")
    val evidenceSnapshot: String,

    @Column(nullable = false)
    val createdAt: Instant = Instant.now(),

    @OneToMany(mappedBy = "finding", fetch = FetchType.LAZY, cascade = [CascadeType.ALL])
    val citations: MutableList<CitationEntity> = mutableListOf(),

    @ManyToMany(fetch = FetchType.LAZY)
    @JoinTable(
        name = "finding_symptoms",
        joinColumns = [JoinColumn(name = "finding_id")],
        inverseJoinColumns = [JoinColumn(name = "symptom_id")]
    )
    val symptoms: MutableList<SymptomEntity> = mutableListOf()
)
