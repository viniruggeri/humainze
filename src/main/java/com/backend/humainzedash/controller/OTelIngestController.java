package com.backend.humainzedash.controller;

import com.backend.humainzedash.dto.telemetry.OtelIngestRequest;
import com.backend.humainzedash.service.OTelService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@Slf4j
@RestController
@RequestMapping("/otel/v1")
@RequiredArgsConstructor
@Tag(name = "OTel Ingest")
public class OTelIngestController {

    private final OTelService oTelService;

    @Operation(summary = "Recebe métricas OTLP")
    @PostMapping("/metrics")
    public ResponseEntity<Void> metrics(@Valid @RequestBody OtelIngestRequest request) {
        log.debug("Recebendo métricas OTLP");
        oTelService.storeMetrics(request);
        log.info("Métricas armazenadas com sucesso");
        return ResponseEntity.accepted().build();
    }

    @Operation(summary = "Recebe traces OTLP")
    @PostMapping("/traces")
    public ResponseEntity<Void> traces(@Valid @RequestBody OtelIngestRequest request) {
        log.debug("Recebendo traces OTLP");
        oTelService.storeTraces(request);
        log.info("Traces armazenados com sucesso");
        return ResponseEntity.accepted().build();
    }

    @Operation(summary = "Recebe logs OTLP")
    @PostMapping("/logs")
    public ResponseEntity<Void> logs(@Valid @RequestBody OtelIngestRequest request) {
        log.debug("Recebendo logs OTLP");
        oTelService.storeLogs(request);
        log.info("Logs armazenados com sucesso");
        return ResponseEntity.accepted().build();
    }
}
