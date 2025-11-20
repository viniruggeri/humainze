package com.backend.humainzedash.service;

import com.backend.humainzedash.domain.entity.Alert;
import com.backend.humainzedash.dto.alert.AlertRequest;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import org.springframework.web.reactive.function.client.WebClientResponseException;

@Service
@RequiredArgsConstructor
public class IAHealthService {

    private final AlertService alertService;
    private final WebClient.Builder webClientBuilder;

    @Value("${ia.health.url:http://ia-service:8000/health}")
    private String healthUrl;

    public void checkHealth() {
        WebClient client = webClientBuilder.build();
        client.get()
                .uri(healthUrl)
                .retrieve()
                .bodyToMono(String.class)
                .doOnError(WebClientResponseException.class,
                        ex -> trigger(Alert.AlertType.SERVICE_DOWN, "IA service unreachable: " + ex.getStatusCode()))
                .subscribe(this::evaluatePayload,
                        ex -> trigger(Alert.AlertType.SERVICE_DOWN, "IA service error: " + ex.getMessage()));
    }

    private void evaluatePayload(String body) {
        if (body == null || body.isBlank()) {
            return;
        }
        String normalized = body.toLowerCase();
        if (normalized.contains("drift")) {
            trigger(Alert.AlertType.DRIFT, "Detected drift: " + body);
        }
        if (normalized.contains("error")) {
            trigger(Alert.AlertType.MODEL_ERROR, "Model error reported: " + body);
        }
    }

    private void trigger(Alert.AlertType type, String message) {
        alertService.createAlert(new AlertRequest("IA", type, message));
    }
}
