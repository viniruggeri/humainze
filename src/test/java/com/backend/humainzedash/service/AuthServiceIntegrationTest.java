package com.backend.humainzedash.service;

import com.backend.humainzedash.dto.auth.LoginRequest;
import com.backend.humainzedash.dto.auth.LoginResponse;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.ActiveProfiles;

import static org.assertj.core.api.Assertions.assertThat;
import static org.junit.jupiter.api.Assertions.assertNotNull;

@SpringBootTest
@ActiveProfiles("dev")
class AuthServiceIntegrationTest {

    @Autowired
    private AuthService authService;

    @Test
    void shouldLoginSuccessfully_WithoutLazyInitializationException() {
        // Given
        LoginRequest request = new LoginRequest("IA", "ia-secret");

        // When
        LoginResponse response = authService.login(request);

        // Then
        assertNotNull(response);
        assertNotNull(response.token());
        assertThat(response.team()).isEqualTo("IA");
        assertThat(response.roles()).contains("ROLE_IA");
    }

    @Test
    void shouldLoginAdmin() {
        // Given
        LoginRequest request = new LoginRequest("ADMIN", "admin-secret");

        // When
        LoginResponse response = authService.login(request);

        // Then
        assertNotNull(response);
        assertThat(response.team()).isEqualTo("ADMIN");
        assertThat(response.roles()).contains("ROLE_ADMIN");
    }

    @Test
    void shouldLoginIoT() {
        // Given
        LoginRequest request = new LoginRequest("IOT", "iot-secret");

        // When
        LoginResponse response = authService.login(request);

        // Then
        assertNotNull(response);
        assertThat(response.team()).isEqualTo("IOT");
        assertThat(response.roles()).contains("ROLE_IOT");
    }
}

