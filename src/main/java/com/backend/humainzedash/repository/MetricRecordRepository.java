package com.backend.humainzedash.repository;

import com.backend.humainzedash.domain.entity.MetricRecord;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.JpaSpecificationExecutor;

import java.util.List;

public interface MetricRecordRepository extends JpaRepository<MetricRecord, Long>, JpaSpecificationExecutor<MetricRecord> {
    List<MetricRecord> findByTeamTagIgnoreCase(String teamTag);
    Page<MetricRecord> findByTeamTagIgnoreCase(String teamTag, Pageable pageable);
}
