package com.backend.humainzedash.repository;

import com.backend.humainzedash.domain.entity.Alert;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;

public interface AlertRepository extends JpaRepository<Alert, Long> {
    Page<Alert> findByTeamTag(String teamTag, Pageable pageable);

    long countByResolvedFalse();

    long countByTeamTagAndResolvedFalse(String teamTag);

    Page<Alert> findByResolvedFalse(Pageable pageable);

    Page<Alert> findByTeamTagAndResolvedFalse(String teamTag, Pageable pageable);
}
