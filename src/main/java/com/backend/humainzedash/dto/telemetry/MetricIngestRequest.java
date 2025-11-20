package com.backend.humainzedash.dto.telemetry;

import com.backend.humainzedash.domain.enums.ModuleType;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;

import java.time.Instant;
import java.util.Map;

public record MetricIngestRequest(
        @NotBlank String key,
        @NotNull Double value,
        @NotNull Instant timestamp,
        @NotNull ModuleType originModule,
        Map<String, Object> metadata
) {
}

