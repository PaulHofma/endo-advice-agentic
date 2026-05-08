package com.endoadvice.model

import jakarta.persistence.*
import java.time.Instant

@Entity
@Table(name = "supplements")
class Supplement(
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    val id: Long = 0,

    @Column(nullable = false, unique = true)
    val name: String,

    @Column(nullable = false, columnDefinition = "TEXT")
    val summary: String,

    @Column(nullable = false)
    val createdAt: Instant = Instant.now(),

    @OneToMany(mappedBy = "supplement", fetch = FetchType.LAZY, cascade = [CascadeType.ALL])
    val findings: MutableList<Finding> = mutableListOf()
)
