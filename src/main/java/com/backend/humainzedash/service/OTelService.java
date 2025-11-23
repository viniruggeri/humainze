package com.backend.humainzedash.service;

import com.backend.humainzedash.domain.entity.LogRecord;
import com.backend.humainzedash.domain.entity.MetricRecord;
import com.backend.humainzedash.domain.entity.SpanRecord;
import com.backend.humainzedash.dto.telemetry.OtelIngestRequest;
import com.backend.humainzedash.repository.LogRecordRepository;
import com.backend.humainzedash.repository.MetricRecordRepository;
import com.backend.humainzedash.repository.SpanRecordRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@RequiredArgsConstructor
public class OTelService {

    private final MetricRecordRepository metricRecordRepository;
    private final SpanRecordRepository spanRecordRepository;
    private final LogRecordRepository logRecordRepository;

    @Transactional
    public void storeMetrics(OtelIngestRequest request) {
        MetricRecord record = new MetricRecord();
        record.setTeamTag(request.teamTag());
        record.setTimestamp(request.timestamp());
        record.setPayloadJson(request.payloadJson());
        metricRecordRepository.save(record);
    }

    @Transactional
    public void storeTraces(OtelIngestRequest request) {
        SpanRecord record = new SpanRecord();
        record.setTeamTag(request.teamTag());
        record.setTimestamp(request.timestamp());
        record.setPayloadJson(request.payloadJson());
        spanRecordRepository.save(record);
    }

    @Transactional
    public void storeLogs(OtelIngestRequest request) {
        LogRecord record = new LogRecord();
        record.setTeamTag(request.teamTag());
        record.setTimestamp(request.timestamp());
        record.setPayloadJson(request.payloadJson());
        logRecordRepository.save(record);
    }
}
