package com.backend.humainzedash.dto.auth;

import jakarta.validation.constraints.NotBlank;

public record LoginRequest(
        @NotBlank(message = "Team tag is required") String team,
        @NotBlank(message = "Secret is required") String secret
) {
}

