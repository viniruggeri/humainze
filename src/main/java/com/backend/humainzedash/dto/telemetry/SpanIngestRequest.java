package com.backend.humainzedash.dto.telemetry;

import com.backend.humainzedash.domain.enums.ModuleType;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;

import java.time.Instant;
import java.util.Map;

public record SpanIngestRequest(
        @NotBlank String traceId,
        @NotBlank String spanId,
        String parentSpanId,
        @NotNull Instant timestamp,
        Long durationMs,
        @NotNull ModuleType originModule,
        String name,
        Map<String, Object> attributes
) {
}

