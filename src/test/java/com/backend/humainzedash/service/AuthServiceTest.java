package com.backend.humainzedash.service;

import com.backend.humainzedash.domain.entity.Team;
import com.backend.humainzedash.domain.entity.TeamRole;
import com.backend.humainzedash.dto.auth.LoginRequest;
import com.backend.humainzedash.dto.auth.LoginResponse;
import com.backend.humainzedash.exception.ResourceNotFoundException;
import com.backend.humainzedash.repository.TeamRepository;
import com.backend.humainzedash.repository.TeamRoleRepository;
import com.backend.humainzedash.security.JwtPayload;
import com.backend.humainzedash.security.JwtService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.springframework.security.crypto.password.PasswordEncoder;

import java.util.List;
import java.util.Optional;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.when;

class AuthServiceTest {

    @Mock
    private TeamRepository teamRepository;
    @Mock
    private TeamRoleRepository teamRoleRepository;
    @Mock
    private PasswordEncoder passwordEncoder;
    @Mock
    private JwtService jwtService;

    @InjectMocks
    private AuthService authService;

    @BeforeEach
    void setup() {
        MockitoAnnotations.openMocks(this);
    }

    @Test
    void shouldLoginTeam() {
        Team team = new Team();
        team.setId(1L);
        team.setTag("IA");
        team.setSecret("encoded");

        when(teamRepository.findByTagIgnoreCase("IA")).thenReturn(Optional.of(team));
        when(passwordEncoder.matches(anyString(), anyString())).thenReturn(true);
        when(teamRoleRepository.findByTeam(team)).thenReturn(List.of(new TeamRole()));
        when(jwtService.generateToken(any(JwtPayload.class))).thenReturn("token");

        LoginResponse response = authService.login(new LoginRequest("IA", "secret"));

        assertThat(response.token()).isEqualTo("token");
    }

    @Test
    void shouldThrowWhenTeamNotFound() {
        when(teamRepository.findByTagIgnoreCase("X")).thenReturn(Optional.empty());
        assertThatThrownBy(() -> authService.login(new LoginRequest("X", "secret")))
                .isInstanceOf(ResourceNotFoundException.class);
    }
}

