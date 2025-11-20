package com.backend.humainzedash.repository;

import com.backend.humainzedash.domain.entity.LogRecord;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.JpaSpecificationExecutor;

public interface LogRecordRepository extends JpaRepository<LogRecord, Long>, JpaSpecificationExecutor<LogRecord> {
    Page<LogRecord> findByTeamTagIgnoreCase(String teamTag, Pageable pageable);
}
