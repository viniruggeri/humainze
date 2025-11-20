package com.backend.humainzedash.dto.auth;

import java.util.List;

public record LoginResponse(
        String token,
        String team,
        List<String> roles
) {
}

