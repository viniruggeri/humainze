package com.backend.humainzedash.controller;

import com.backend.humainzedash.config.WebMvcTestWithoutSecurity;
import com.backend.humainzedash.dto.telemetry.OtelIngestRequest;
import com.backend.humainzedash.security.ApiKeyService;
import com.backend.humainzedash.service.OTelService;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import java.time.Instant;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@WebMvcTestWithoutSecurity(OTelIngestController.class)
class OTelIngestControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private OTelService oTelService;

    @MockBean
    private ApiKeyService apiKeyService;

    @Test
    void shouldAcceptMetricIngest() throws Exception {
        Mockito.doNothing().when(oTelService).storeMetrics(Mockito.any(OtelIngestRequest.class));

        mockMvc.perform(post("/otel/v1/metrics")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"teamTag\":\"IA\",\"timestamp\":\"" + Instant.now().toString()
                        + "\",\"payloadJson\":\"{}\"}"))
                .andExpect(status().isAccepted());
    }
}
