package com.backend.humainzedash.repository;

import com.backend.humainzedash.domain.entity.SpanRecord;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.JpaSpecificationExecutor;

public interface SpanRecordRepository extends JpaRepository<SpanRecord, Long>, JpaSpecificationExecutor<SpanRecord> {
    Page<SpanRecord> findByTeamTagIgnoreCase(String teamTag, Pageable pageable);
}
