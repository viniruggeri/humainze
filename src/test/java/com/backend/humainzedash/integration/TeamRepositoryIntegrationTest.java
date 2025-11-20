package com.backend.humainzedash.integration;

import com.backend.humainzedash.domain.entity.Role;
import com.backend.humainzedash.domain.entity.Team;
import com.backend.humainzedash.domain.entity.TeamRole;
import com.backend.humainzedash.repository.RoleRepository;
import com.backend.humainzedash.repository.TeamRepository;
import com.backend.humainzedash.repository.TeamRoleRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;

@SpringBootTest
@ActiveProfiles("test")
@Transactional
class TeamRepositoryIntegrationTest {

    @Autowired
    private TeamRepository teamRepository;

    @Autowired
    private RoleRepository roleRepository;

    @Autowired
    private TeamRoleRepository teamRoleRepository;

    private Team team;
    private Role role;

    @BeforeEach
    void setup() {
        // Cria role
        role = new Role();
        role.setName("ROLE_IA");
        role.setDescription("Teste role");
        role = roleRepository.save(role);

        // Cria team
        team = new Team();
        team.setTag("IA");
        team.setSecret("encoded-secret");
        team.setDescription("Time de IA para testes");
        team.setEmails(List.of("ia@test.com", "ia2@test.com"));
        team = teamRepository.save(team);

        // Associa role ao team
        TeamRole teamRole = new TeamRole();
        teamRole.setTeam(team);
        teamRole.setRole(role);
        teamRoleRepository.save(teamRole);
    }

    @Test
    void shouldFindTeamByTag() {
        var found = teamRepository.findByTagIgnoreCase("ia");

        assertThat(found).isPresent();
        assertThat(found.get().getTag()).isEqualTo("IA");
        assertThat(found.get().getEmails()).hasSize(2);
        assertThat(found.get().getEmails()).contains("ia@test.com", "ia2@test.com");
    }

    @Test
    void shouldFindTeamByTagIgnoringCase() {
        var found = teamRepository.findByTagIgnoreCase("Ia");

        assertThat(found).isPresent();
        assertThat(found.get().getTag()).isEqualTo("IA");
    }

    @Test
    void shouldFindRolesByTeam() {
        var roles = teamRoleRepository.findByTeam(team);

        assertThat(roles).hasSize(1);
        assertThat(roles.get(0).getRole().getName()).isEqualTo("ROLE_IA");
    }

    @Test
    void shouldPersistMultipleEmails() {
        Team newTeam = new Team();
        newTeam.setTag("IOT");
        newTeam.setSecret("iot-secret");
        newTeam.setEmails(List.of("iot1@test.com", "iot2@test.com", "iot3@test.com"));
        
        Team saved = teamRepository.save(newTeam);
        
        Team retrieved = teamRepository.findById(saved.getId()).orElseThrow();
        assertThat(retrieved.getEmails()).hasSize(3);
    }
}

