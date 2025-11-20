package com.backend.humainzedash.controller;

import com.backend.humainzedash.config.WebMvcTestWithoutSecurity;
import com.backend.humainzedash.dto.telemetry.OtelExportResponse;
import com.backend.humainzedash.service.OTelExportService;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;
import org.springframework.data.domain.PageRequest;
import org.springframework.test.web.servlet.MockMvc;

import java.time.Instant;
import java.util.List;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@WebMvcTestWithoutSecurity(OTelExportController.class)
class OTelExportControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private OTelExportService oTelExportService;

    @Test
    void shouldExportMetricsForOwnTeam() throws Exception {
        OtelExportResponse response = new OtelExportResponse(1L, "IA", Instant.now(), "{}");
        Page<OtelExportResponse> page = new PageImpl<>(List.of(response), PageRequest.of(0, 20), 1);

        Mockito.when(oTelExportService.exportMetrics(eq("IA"), any())).thenReturn(page);

        mockMvc.perform(get("/export/metrics"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.content[0].teamTag").value("IA"));

        Mockito.verify(oTelExportService).exportMetrics(eq("IA"), any());
    }

    @Test
    void shouldExportMetricsForOtherTeamAsAdmin() throws Exception {
        OtelExportResponse response = new OtelExportResponse(1L, "IOT", Instant.now(), "{}");
        Page<OtelExportResponse> page = new PageImpl<>(List.of(response), PageRequest.of(0, 20), 1);

        Mockito.when(oTelExportService.exportMetrics(eq("IOT"), any())).thenReturn(page);

        mockMvc.perform(get("/export/metrics?teamTag=IOT"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.content[0].teamTag").value("IOT"));

        Mockito.verify(oTelExportService).exportMetrics(eq("IOT"), any());
    }

    @Test
    void shouldExportTracesForOwnTeam() throws Exception {
        OtelExportResponse response = new OtelExportResponse(2L, "IA", Instant.now(), "{\"traceId\":\"abc\"}");
        Page<OtelExportResponse> page = new PageImpl<>(List.of(response), PageRequest.of(0, 20), 1);

        Mockito.when(oTelExportService.exportTraces(eq("IA"), any())).thenReturn(page);

        mockMvc.perform(get("/export/traces"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.content[0].teamTag").value("IA"));
    }

    @Test
    void shouldExportLogsForOwnTeam() throws Exception {
        OtelExportResponse response = new OtelExportResponse(3L, "IOT", Instant.now(), "{\"level\":\"ERROR\"}");
        Page<OtelExportResponse> page = new PageImpl<>(List.of(response), PageRequest.of(0, 20), 1);

        Mockito.when(oTelExportService.exportLogs(eq("IOT"), any())).thenReturn(page);

        mockMvc.perform(get("/export/logs"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.content[0].teamTag").value("IOT"));
    }
}

