package com.backend.humainzedash.controller;

import com.backend.humainzedash.dto.alert.AlertRequest;
import com.backend.humainzedash.dto.alert.AlertResponse;
import com.backend.humainzedash.service.AlertService;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;
import org.springframework.data.domain.PageRequest;
import org.springframework.http.MediaType;
import org.springframework.security.test.context.support.WithMockUser;
import org.springframework.test.web.servlet.MockMvc;

import java.time.Instant;
import java.util.List;

import static org.springframework.security.test.web.servlet.request.SecurityMockMvcRequestPostProcessors.csrf;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@WebMvcTest(AlertController.class)
@AutoConfigureMockMvc(addFilters = false)
class AlertControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private AlertService alertService;

    @Test
    @WithMockUser(roles = "IA")
    void shouldCreateAlert() throws Exception {
        AlertResponse response = new AlertResponse(1L, "IA", com.backend.humainzedash.domain.entity.Alert.AlertType.DRIFT, "msg", Instant.now(), false);
        Mockito.when(alertService.createAlert(Mockito.any(AlertRequest.class))).thenReturn(response);

        mockMvc.perform(post("/alerts")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"teamTag\":\"IA\",\"type\":\"DRIFT\",\"message\":\"msg\"}"))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.teamTag").value("IA"));
    }

    @Test
    void shouldListAlerts() throws Exception {
        Page<AlertResponse> page = new PageImpl<>(List.of(new AlertResponse(1L, "IA", com.backend.humainzedash.domain.entity.Alert.AlertType.DRIFT, "msg", Instant.now(), false)), PageRequest.of(0, 20), 1);
        Mockito.when(alertService.listAlerts(Mockito.any(), Mockito.any())).thenReturn(page);

        mockMvc.perform(get("/alerts"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.content[0].teamTag").value("IA"));
    }
}
