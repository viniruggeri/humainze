package com.backend.humainzedash.dto.alert;

import com.backend.humainzedash.domain.entity.Alert;

import java.time.Instant;

public record AlertResponse(
        Long id,
        String teamTag,
        Alert.AlertType type,
        String message,
        Instant timestamp,
        boolean resolved
) {
}

