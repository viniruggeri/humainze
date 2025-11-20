package com.backend.humainzedash.service;

import com.backend.humainzedash.domain.entity.Role;
import com.backend.humainzedash.domain.entity.Team;
import com.backend.humainzedash.domain.entity.TeamRole;
import com.backend.humainzedash.dto.team.TeamRequest;
import com.backend.humainzedash.repository.RoleRepository;
import com.backend.humainzedash.repository.TeamRepository;
import com.backend.humainzedash.repository.TeamRoleRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.springframework.security.crypto.password.PasswordEncoder;

import java.util.List;
import java.util.Optional;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

class TeamServiceTest {

    @Mock
    private TeamRepository teamRepository;
    @Mock
    private RoleRepository roleRepository;
    @Mock
    private TeamRoleRepository teamRoleRepository;
    @Mock
    private PasswordEncoder passwordEncoder;

    @InjectMocks
    private TeamService teamService;

    @BeforeEach
    void setup() {
        MockitoAnnotations.openMocks(this);
        when(passwordEncoder.encode(any())).thenReturn("encoded");
    }

    @Test
    void shouldCreateTeam() {
        TeamRequest request = new TeamRequest("IA", "secret123", "desc", List.of("ia@humanize.ai"));
        Team saved = new Team();
        saved.setId(1L);
        saved.setTag("IA");
        saved.setDescription("desc");
        saved.setEmails(List.of("ia@humanize.ai"));

        when(teamRepository.save(any(Team.class))).thenReturn(saved);
        when(teamRoleRepository.findByTeam(any())).thenReturn(List.of());

        var response = teamService.createTeam(request);

        assertThat(response.id()).isEqualTo(1L);
        assertThat(response.tag()).isEqualTo("IA");
        verify(teamRepository).save(any(Team.class));
    }
}

