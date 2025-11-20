package com.backend.humainzedash.dto.telemetry;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;

import java.time.Instant;

public record OtelIngestRequest(
        @NotBlank String teamTag,
        @NotNull Instant timestamp,
        @NotBlank String payloadJson
) {
}

