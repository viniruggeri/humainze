package com.backend.humainzedash.service;

import com.backend.humainzedash.domain.entity.MetricRecord;
import com.backend.humainzedash.domain.entity.SpanRecord;
import com.backend.humainzedash.domain.entity.LogRecord;
import com.backend.humainzedash.dto.telemetry.OtelExportResponse;
import com.backend.humainzedash.repository.MetricRecordRepository;
import com.backend.humainzedash.repository.SpanRecordRepository;
import com.backend.humainzedash.repository.LogRecordRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;

import java.time.Instant;
import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.Mockito.when;

class OTelExportServiceTest {

    @Mock
    private MetricRecordRepository metricRecordRepository;
    @Mock
    private SpanRecordRepository spanRecordRepository;
    @Mock
    private LogRecordRepository logRecordRepository;

    @InjectMocks
    private OTelExportService oTelExportService;

    @BeforeEach
    void setup() {
        MockitoAnnotations.openMocks(this);
    }

    @Test
    void shouldExportMetrics() {
        MetricRecord record = new MetricRecord();
        record.setId(1L);
        record.setTeamTag("IA");
        record.setTimestamp(Instant.now());
        record.setPayloadJson("{\"cpu\":75}");

        Pageable pageable = PageRequest.of(0, 10);
        Page<MetricRecord> page = new PageImpl<>(List.of(record), pageable, 1);

        when(metricRecordRepository.findByTeamTagIgnoreCase("IA", pageable)).thenReturn(page);

        Page<OtelExportResponse> result = oTelExportService.exportMetrics("IA", pageable);

        assertThat(result.getTotalElements()).isEqualTo(1);
        OtelExportResponse response = result.getContent().get(0);
        assertThat(response.id()).isEqualTo(1L);
        assertThat(response.teamTag()).isEqualTo("IA");
        assertThat(response.payloadJson()).isEqualTo("{\"cpu\":75}");
    }

    @Test
    void shouldExportTraces() {
        SpanRecord record = new SpanRecord();
        record.setId(2L);
        record.setTeamTag("IOT");
        record.setTimestamp(Instant.now());
        record.setPayloadJson("{\"spanId\":\"xyz\"}");

        Pageable pageable = PageRequest.of(0, 10);
        Page<SpanRecord> page = new PageImpl<>(List.of(record), pageable, 1);

        when(spanRecordRepository.findByTeamTagIgnoreCase("IOT", pageable)).thenReturn(page);

        Page<OtelExportResponse> result = oTelExportService.exportTraces("IOT", pageable);

        assertThat(result.getTotalElements()).isEqualTo(1);
        assertThat(result.getContent().get(0).teamTag()).isEqualTo("IOT");
    }

    @Test
    void shouldExportLogs() {
        LogRecord record = new LogRecord();
        record.setId(3L);
        record.setTeamTag("JAVA");
        record.setTimestamp(Instant.now());
        record.setPayloadJson("{\"message\":\"error\"}");

        Pageable pageable = PageRequest.of(0, 10);
        Page<LogRecord> page = new PageImpl<>(List.of(record), pageable, 1);

        when(logRecordRepository.findByTeamTagIgnoreCase("JAVA", pageable)).thenReturn(page);

        Page<OtelExportResponse> result = oTelExportService.exportLogs("JAVA", pageable);

        assertThat(result.getTotalElements()).isEqualTo(1);
        assertThat(result.getContent().get(0).teamTag()).isEqualTo("JAVA");
    }
}

