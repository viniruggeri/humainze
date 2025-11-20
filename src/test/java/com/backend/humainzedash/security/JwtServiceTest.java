package com.backend.humainzedash.security;

import com.backend.humainzedash.config.JwtProperties;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;

class JwtServiceTest {

    private JwtService jwtService;

    @BeforeEach
    void setup() {
        JwtProperties properties = new JwtProperties(
                "humainze-test",
                "test-audience",
                "test-secret-must-be-at-least-256-bits-long-for-HS256",
                120
        );
        jwtService = new JwtService(properties);
    }

    @Test
    void shouldGenerateToken() {
        JwtPayload payload = new JwtPayload(1L, "IA", "IA", List.of("ROLE_IA"));

        String token = jwtService.generateToken(payload);

        assertThat(token).isNotNull();
        assertThat(token).isNotEmpty();
        assertThat(token.split("\\.")).hasSize(3); // JWT tem 3 partes separadas por ponto
    }

    @Test
    void shouldParseToken() {
        JwtPayload original = new JwtPayload(1L, "IA", "IA", List.of("ROLE_IA", "ROLE_ADMIN"));
        String token = jwtService.generateToken(original);

        JwtPayload parsed = jwtService.parseToken(token);

        assertThat(parsed.teamId()).isEqualTo(1L);
        assertThat(parsed.teamTag()).isEqualTo("IA");
        assertThat(parsed.email()).isEqualTo("IA");
        assertThat(parsed.roles()).containsExactlyInAnyOrder("ROLE_IA", "ROLE_ADMIN");
    }

    @Test
    void shouldGenerateAndParseMultipleTokens() {
        JwtPayload payload1 = new JwtPayload(1L, "IA", "IA", List.of("ROLE_IA"));
        JwtPayload payload2 = new JwtPayload(2L, "IOT", "IOT", List.of("ROLE_IOT"));

        String token1 = jwtService.generateToken(payload1);
        String token2 = jwtService.generateToken(payload2);

        JwtPayload parsed1 = jwtService.parseToken(token1);
        JwtPayload parsed2 = jwtService.parseToken(token2);

        assertThat(parsed1.teamTag()).isEqualTo("IA");
        assertThat(parsed2.teamTag()).isEqualTo("IOT");
    }
}

