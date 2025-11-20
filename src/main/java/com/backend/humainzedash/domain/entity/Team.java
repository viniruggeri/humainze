package com.backend.humainzedash.domain.entity;

import jakarta.persistence.CollectionTable;
import jakarta.persistence.Column;
import jakarta.persistence.ElementCollection;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.Getter;
import lombok.Setter;

import java.util.List;

@Getter
@Setter
@Entity
@Table(name = "teams")
public class Team {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true, length = 64)
    private String tag;

    @Column(nullable = false, length = 512)
    private String secret;

    @Column(length = 1024)
    private String description;

    @ElementCollection
    @CollectionTable(name = "team_emails")
    @Column(name = "email", nullable = false)
    private List<String> emails;
}
