package com.backend.humainzedash.domain.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.Getter;
import lombok.Setter;

import java.time.Instant;

@Getter
@Setter
@Entity
@Table(name = "metric_records")
public class MetricRecord {

    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private Long id;

    @Column(nullable = false)
    private String teamTag;

    @Column(nullable = false)
    private Instant timestamp;

    @Column(name = "payload", nullable = false, columnDefinition = "CLOB")
    private String payloadJson;
}
