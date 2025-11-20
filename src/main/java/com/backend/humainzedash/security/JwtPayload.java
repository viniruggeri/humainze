package com.backend.humainzedash.security;

import java.util.List;

public record JwtPayload(Long teamId,
                         String teamTag,
                         String email,
                         List<String> roles) {
}

