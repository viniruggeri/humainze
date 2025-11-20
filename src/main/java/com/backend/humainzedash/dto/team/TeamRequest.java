package com.backend.humainzedash.dto.team;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

import java.util.List;

public record TeamRequest(
        @NotBlank String tag,
        @NotBlank @Size(min = 8) String secret,
        @Size(max = 1024) String description,
        List<@NotBlank String> emails
) {
}

