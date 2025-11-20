package com.backend.humainzedash.dto.alert;

import com.backend.humainzedash.domain.entity.Alert;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;

public record AlertRequest(
        @NotBlank String teamTag,
        @NotNull Alert.AlertType type,
        @NotBlank String message
) {
}

