package com.backend.humainzedash.dto.telemetry;

import java.time.Instant;

public record OtelExportResponse(
        Long id,
        String teamTag,
        Instant timestamp,
        String payloadJson
) {
}

