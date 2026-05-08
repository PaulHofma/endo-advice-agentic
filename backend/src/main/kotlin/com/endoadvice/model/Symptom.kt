package com.endoadvice.model

import jakarta.persistence.*
import java.time.Instant

@Entity
@Table(name = "symptoms")
class Symptom(
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    val id: Long = 0,

    @Column(nullable = false, unique = true)
    val name: String,

    @Column(nullable = false, unique = true)
    val slug: String,

    @Column(nullable = false)
    val createdAt: Instant = Instant.now(),

    @ManyToMany(mappedBy = "symptoms", fetch = FetchType.LAZY)
    val findings: MutableList<Finding> = mutableListOf()
)
