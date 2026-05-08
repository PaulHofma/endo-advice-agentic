package com.endoadvice.model

import jakarta.persistence.*
import java.time.Instant

@Entity
@Table(name = "findings")
class Finding(
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    val id: Long = 0,

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "supplement_id", nullable = false)
    val supplement: Supplement,

    @Column(nullable = false, columnDefinition = "TEXT")
    val plainLanguageSummary: String,

    @Column(nullable = false, columnDefinition = "TEXT")
    val evidenceSnapshot: String,

    @Column(nullable = false)
    val createdAt: Instant = Instant.now(),

    @OneToMany(mappedBy = "finding", fetch = FetchType.LAZY, cascade = [CascadeType.ALL])
    val citations: MutableList<Citation> = mutableListOf(),

    @ManyToMany(fetch = FetchType.LAZY)
    @JoinTable(
        name = "finding_symptoms",
        joinColumns = [JoinColumn(name = "finding_id")],
        inverseJoinColumns = [JoinColumn(name = "symptom_id")]
    )
    val symptoms: MutableList<Symptom> = mutableListOf()
)
