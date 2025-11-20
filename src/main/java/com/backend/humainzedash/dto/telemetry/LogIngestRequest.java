package com.backend.humainzedash.dto.telemetry;

import com.backend.humainzedash.domain.enums.ModuleType;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;

import java.time.Instant;
import java.util.Map;

public record LogIngestRequest(
        @NotNull ModuleType originModule,
        @NotNull Instant timestamp,
        @NotBlank String level,
        @NotBlank String message,
        String traceId,
        String spanId,
        Map<String, Object> attributes
) {
}

