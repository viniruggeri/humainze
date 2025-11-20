package com.backend.humainzedash.e2e;

import com.backend.humainzedash.dto.auth.LoginResponse;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.web.client.TestRestTemplate;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.*;
import org.springframework.test.context.ActiveProfiles;

import java.time.Instant;
import java.util.Map;

import static org.assertj.core.api.Assertions.assertThat;

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@ActiveProfiles("dev")
class AuthAndMetricsE2ETest {

    @Autowired
    private TestRestTemplate restTemplate;

    @Test
    void fullFlow_authIngestExport() {
        // 1. Login
        Map<String, String> loginRequest = Map.of(
                "team", "ADMIN",
                "secret", "admin-secret"
        );

        ResponseEntity<LoginResponse> loginResponse = restTemplate.postForEntity(
                "/auth/login",
                loginRequest,
                LoginResponse.class
        );

        assertThat(loginResponse.getStatusCode()).isEqualTo(HttpStatus.OK);
        assertThat(loginResponse.getBody()).isNotNull();
        assertThat(loginResponse.getBody().token()).isNotEmpty();
        assertThat(loginResponse.getBody().team()).isEqualTo("ADMIN");

        String token = loginResponse.getBody().token();

        // 2. Ingest de métrica
        HttpHeaders headers = new HttpHeaders();
        headers.setBearerAuth(token);
        headers.setContentType(MediaType.APPLICATION_JSON);

        Map<String, Object> metricPayload = Map.of(
                "teamTag", "ADMIN",
                "timestamp", Instant.now().toString(),
                "payloadJson", "{\"cpu\":90,\"memory\":75}"
        );

        HttpEntity<Map<String, Object>> ingestRequest = new HttpEntity<>(metricPayload, headers);

        ResponseEntity<Void> ingestResponse = restTemplate.postForEntity(
                "/otel/v1/metrics",
                ingestRequest,
                Void.class
        );

        assertThat(ingestResponse.getStatusCode()).isEqualTo(HttpStatus.ACCEPTED);

        // 3. Export de métricas
        HttpEntity<Void> exportRequest = new HttpEntity<>(headers);

        ResponseEntity<Map<String, Object>> exportResponse = restTemplate.exchange(
                "/export/metrics",
                HttpMethod.GET,
                exportRequest,
                new ParameterizedTypeReference<>() {}
        );

        assertThat(exportResponse.getStatusCode()).isEqualTo(HttpStatus.OK);
        assertThat(exportResponse.getBody()).isNotNull();
        assertThat(exportResponse.getBody()).containsKey("content");

        // Verifica que há pelo menos 1 registro
        @SuppressWarnings("unchecked")
        var content = (java.util.List<Map<String, Object>>) exportResponse.getBody().get("content");
        assertThat(content).isNotEmpty();
        assertThat(content.get(0).get("teamTag")).isEqualTo("ADMIN");
    }

    @Test
    void shouldRejectUnauthenticatedIngest() {
        Map<String, Object> metricPayload = Map.of(
                "teamTag", "IA",
                "timestamp", Instant.now().toString(),
                "payloadJson", "{}"
        );

        ResponseEntity<Void> response = restTemplate.postForEntity(
                "/otel/v1/metrics",
                metricPayload,
                Void.class
        );

        assertThat(response.getStatusCode()).isEqualTo(HttpStatus.UNAUTHORIZED);
    }

    @Test
    void shouldRejectInvalidCredentials() {
        Map<String, String> loginRequest = Map.of(
                "team", "ADMIN",
                "secret", "wrong-secret"
        );

        ResponseEntity<LoginResponse> response = restTemplate.postForEntity(
                "/auth/login",
                loginRequest,
                LoginResponse.class
        );

        assertThat(response.getStatusCode()).isIn(HttpStatus.UNAUTHORIZED, HttpStatus.BAD_REQUEST, HttpStatus.INTERNAL_SERVER_ERROR);
    }
}

