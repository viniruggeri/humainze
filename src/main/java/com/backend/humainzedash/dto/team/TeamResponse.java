package com.backend.humainzedash.dto.team;

import java.util.List;

public record TeamResponse(
        Long id,
        String tag,
        String description,
        List<String> emails,
        List<String> roles
) {
}

