package com.backend.humainzedash.service;

import com.backend.humainzedash.domain.entity.LogRecord;
import com.backend.humainzedash.domain.entity.MetricRecord;
import com.backend.humainzedash.domain.entity.SpanRecord;
import com.backend.humainzedash.dto.telemetry.OtelExportResponse;
import com.backend.humainzedash.repository.LogRecordRepository;
import com.backend.humainzedash.repository.MetricRecordRepository;
import com.backend.humainzedash.repository.SpanRecordRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class OTelExportService {

    private final MetricRecordRepository metricRecordRepository;
    private final SpanRecordRepository spanRecordRepository;
    private final LogRecordRepository logRecordRepository;

    public Page<OtelExportResponse> exportMetrics(String teamTag, Pageable pageable) {
        return metricRecordRepository.findByTeamTagIgnoreCase(teamTag, pageable).map(this::toResponse);
    }

    public Page<OtelExportResponse> exportTraces(String teamTag, Pageable pageable) {
        return spanRecordRepository.findByTeamTagIgnoreCase(teamTag, pageable).map(this::toResponse);
    }

    public Page<OtelExportResponse> exportLogs(String teamTag, Pageable pageable) {
        return logRecordRepository.findByTeamTagIgnoreCase(teamTag, pageable).map(this::toResponse);
    }

    private OtelExportResponse toResponse(MetricRecord record) {
        return new OtelExportResponse(record.getId(), record.getTeamTag(), record.getTimestamp(), record.getPayloadJson());
    }

    private OtelExportResponse toResponse(SpanRecord record) {
        return new OtelExportResponse(record.getId(), record.getTeamTag(), record.getTimestamp(), record.getPayloadJson());
    }

    private OtelExportResponse toResponse(LogRecord record) {
        return new OtelExportResponse(record.getId(), record.getTeamTag(), record.getTimestamp(), record.getPayloadJson());
    }
}
