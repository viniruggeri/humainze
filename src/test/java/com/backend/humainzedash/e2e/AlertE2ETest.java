package com.backend.humainzedash.e2e;

import com.backend.humainzedash.domain.entity.Alert;
import com.backend.humainzedash.dto.auth.LoginResponse;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.web.client.TestRestTemplate;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.*;
import org.springframework.test.context.ActiveProfiles;

import java.util.Map;

import static org.assertj.core.api.Assertions.assertThat;

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@ActiveProfiles("dev")
class AlertE2ETest {

    @Autowired
    private TestRestTemplate restTemplate;

    @Test
    void fullAlertFlow_createListResolve() {
        // 1. Login como IA (tem permissão para alerts)
        Map<String, String> loginRequest = Map.of(
                "team", "IA",
                "secret", "ia-secret"
        );

        ResponseEntity<LoginResponse> loginResponse = restTemplate.postForEntity(
                "/auth/login",
                loginRequest,
                LoginResponse.class
        );

        assertThat(loginResponse.getStatusCode()).isEqualTo(HttpStatus.OK);
        String token = loginResponse.getBody().token();

        HttpHeaders headers = new HttpHeaders();
        headers.setBearerAuth(token);
        headers.setContentType(MediaType.APPLICATION_JSON);

        // 2. Cria alerta
        Map<String, Object> alertPayload = Map.of(
                "teamTag", "IA",
                "type", "DRIFT",
                "message", "Drift detectado no modelo"
        );

        HttpEntity<Map<String, Object>> createRequest = new HttpEntity<>(alertPayload, headers);

        ResponseEntity<Map<String, Object>> createResponse = restTemplate.exchange(
                "/alerts",
                HttpMethod.POST,
                createRequest,
                new ParameterizedTypeReference<>() {}
        );

        assertThat(createResponse.getStatusCode()).isEqualTo(HttpStatus.CREATED);
        assertThat(createResponse.getBody()).isNotNull();
        assertThat(createResponse.getBody().get("teamTag")).isEqualTo("IA");
        assertThat(createResponse.getBody().get("type")).isEqualTo("DRIFT");
        assertThat(createResponse.getBody().get("resolved")).isEqualTo(false);

        Long alertId = ((Number) createResponse.getBody().get("id")).longValue();

        // 3. Lista alertas
        HttpEntity<Void> listRequest = new HttpEntity<>(headers);

        ResponseEntity<Map<String, Object>> listResponse = restTemplate.exchange(
                "/alerts",
                HttpMethod.GET,
                listRequest,
                new ParameterizedTypeReference<>() {}
        );

        assertThat(listResponse.getStatusCode()).isEqualTo(HttpStatus.OK);
        @SuppressWarnings("unchecked")
        var content = (java.util.List<Map<String, Object>>) listResponse.getBody().get("content");
        assertThat(content).isNotEmpty();

        // 4. Resolve o alerta
        HttpEntity<Void> resolveRequest = new HttpEntity<>(headers);

        ResponseEntity<Map<String, Object>> resolveResponse = restTemplate.exchange(
                "/alerts/" + alertId + "/resolve",
                HttpMethod.PUT,
                resolveRequest,
                new ParameterizedTypeReference<>() {}
        );

        assertThat(resolveResponse.getStatusCode()).isEqualTo(HttpStatus.OK);
        assertThat(resolveResponse.getBody().get("resolved")).isEqualTo(true);
        assertThat(resolveResponse.getBody().get("id")).isEqualTo(alertId.intValue());
    }

    @Test
    void shouldFilterAlertsByTeam() {
        // Login como ADMIN
        Map<String, String> loginRequest = Map.of(
                "team", "ADMIN",
                "secret", "admin-secret"
        );

        ResponseEntity<LoginResponse> loginResponse = restTemplate.postForEntity(
                "/auth/login",
                loginRequest,
                LoginResponse.class
        );

        String token = loginResponse.getBody().token();

        HttpHeaders headers = new HttpHeaders();
        headers.setBearerAuth(token);

        // Cria alerta para IA
        Map<String, Object> alertPayload = Map.of(
                "teamTag", "IA",
                "type", "SERVICE_DOWN",
                "message", "Serviço IA offline"
        );

        HttpEntity<Map<String, Object>> createRequest = new HttpEntity<>(alertPayload, headers);
        restTemplate.exchange("/alerts", HttpMethod.POST, createRequest, new ParameterizedTypeReference<Map<String, Object>>() {});

        // Lista com filtro
        HttpEntity<Void> listRequest = new HttpEntity<>(headers);

        ResponseEntity<Map<String, Object>> response = restTemplate.exchange(
                "/alerts?team=IA",
                HttpMethod.GET,
                listRequest,
                new ParameterizedTypeReference<>() {}
        );

        assertThat(response.getStatusCode()).isEqualTo(HttpStatus.OK);
        @SuppressWarnings("unchecked")
        var content = (java.util.List<Map<String, Object>>) response.getBody().get("content");
        assertThat(content).allMatch(alert -> alert.get("teamTag").equals("IA"));
    }
}

