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
@Table(name = "span_records")
public class SpanRecord {

    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "span_seq")
    @jakarta.persistence.SequenceGenerator(name = "span_seq", sequenceName = "SPAN_RECORDS_SEQ", allocationSize = 1)
    private Long id;

    @Column(nullable = false)
    private String teamTag;

    @Column(nullable = false)
    private Instant timestamp;

    @Column(name = "payload", nullable = false, columnDefinition = "CLOB")
    private String payloadJson;
}
