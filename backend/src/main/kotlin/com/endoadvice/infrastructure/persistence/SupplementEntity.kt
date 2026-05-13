package com.endoadvice.infrastructure.persistence

import jakarta.persistence.*
import java.time.Instant

@Entity(name = "Supplement")
@Table(name = "supplements")
class SupplementEntity(
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    val id: Long = 0,

    @Column(nullable = false, unique = true)
    val name: String,

    @Column(nullable = false, columnDefinition = "TEXT")
    val summary: String,

    @Column(nullable = false)
    val createdAt: Instant = Instant.now(),

    @OneToMany(mappedBy = "supplement", fetch = FetchType.LAZY, cascade = [CascadeType.ALL])
    val findings: MutableList<FindingEntity> = mutableListOf()
)
