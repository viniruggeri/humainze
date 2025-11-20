package com.backend.humainzedash.integration;

import com.backend.humainzedash.domain.entity.MetricRecord;
import com.backend.humainzedash.domain.entity.SpanRecord;
import com.backend.humainzedash.domain.entity.LogRecord;
import com.backend.humainzedash.dto.telemetry.OtelExportResponse;
import com.backend.humainzedash.repository.MetricRecordRepository;
import com.backend.humainzedash.repository.SpanRecordRepository;
import com.backend.humainzedash.repository.LogRecordRepository;
import com.backend.humainzedash.service.OTelExportService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.transaction.annotation.Transactional;

import java.time.Instant;

import static org.assertj.core.api.Assertions.assertThat;

@SpringBootTest
@ActiveProfiles("test")
@Transactional
class OTelExportIntegrationTest {

    @Autowired
    private MetricRecordRepository metricRecordRepository;

    @Autowired
    private SpanRecordRepository spanRecordRepository;

    @Autowired
    private LogRecordRepository logRecordRepository;

    @Autowired
    private OTelExportService oTelExportService;

    @BeforeEach
    void setup() {
        // Insere métricas
        MetricRecord metric1 = new MetricRecord();
        metric1.setTeamTag("IA");
        metric1.setTimestamp(Instant.now());
        metric1.setPayloadJson("{\"cpu\":75}");
        metricRecordRepository.save(metric1);

        MetricRecord metric2 = new MetricRecord();
        metric2.setTeamTag("IA");
        metric2.setTimestamp(Instant.now());
        metric2.setPayloadJson("{\"cpu\":85}");
        metricRecordRepository.save(metric2);

        MetricRecord metric3 = new MetricRecord();
        metric3.setTeamTag("IOT");
        metric3.setTimestamp(Instant.now());
        metric3.setPayloadJson("{\"temperature\":25}");
        metricRecordRepository.save(metric3);

        // Insere spans
        SpanRecord span = new SpanRecord();
        span.setTeamTag("IA");
        span.setTimestamp(Instant.now());
        span.setPayloadJson("{\"traceId\":\"abc123\"}");
        spanRecordRepository.save(span);

        // Insere logs
        LogRecord log = new LogRecord();
        log.setTeamTag("IA");
        log.setTimestamp(Instant.now());
        log.setPayloadJson("{\"level\":\"INFO\"}");
        logRecordRepository.save(log);
    }

    @Test
    void shouldExportMetricsByTeamTag() {
        Page<OtelExportResponse> result = oTelExportService.exportMetrics("IA", PageRequest.of(0, 10));

        assertThat(result.getTotalElements()).isEqualTo(2);
        assertThat(result.getContent()).allMatch(r -> r.teamTag().equals("IA"));
        assertThat(result.getContent().get(0).payloadJson()).contains("cpu");
    }

    @Test
    void shouldExportTracesForTeam() {
        Page<OtelExportResponse> result = oTelExportService.exportTraces("IA", PageRequest.of(0, 10));

        assertThat(result.getTotalElements()).isEqualTo(1);
        assertThat(result.getContent().get(0).payloadJson()).contains("traceId");
    }

    @Test
    void shouldExportLogsForTeam() {
        Page<OtelExportResponse> result = oTelExportService.exportLogs("IA", PageRequest.of(0, 10));

        assertThat(result.getTotalElements()).isEqualTo(1);
        assertThat(result.getContent().get(0).payloadJson()).contains("level");
    }

    @Test
    void shouldReturnEmptyPageWhenNoMetricsForTeam() {
        Page<OtelExportResponse> result = oTelExportService.exportMetrics("JAVA", PageRequest.of(0, 10));

        assertThat(result.getTotalElements()).isZero();
    }

    @Test
    void shouldPaginateResults() {
        Page<OtelExportResponse> page1 = oTelExportService.exportMetrics("IA", PageRequest.of(0, 1));
        Page<OtelExportResponse> page2 = oTelExportService.exportMetrics("IA", PageRequest.of(1, 1));

        assertThat(page1.getContent()).hasSize(1);
        assertThat(page2.getContent()).hasSize(1);
        assertThat(page1.getContent().get(0).id()).isNotEqualTo(page2.getContent().get(0).id());
    }
}

