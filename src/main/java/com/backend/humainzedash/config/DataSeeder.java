package com.backend.humainzedash.config;

import com.backend.humainzedash.domain.entity.Role;
import com.backend.humainzedash.domain.entity.Team;
import com.backend.humainzedash.domain.entity.TeamRole;
import com.backend.humainzedash.repository.RoleRepository;
import com.backend.humainzedash.repository.TeamRepository;
import com.backend.humainzedash.repository.TeamRoleRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Configuration;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.beans.factory.annotation.Value;

import java.util.List;

@Configuration
@RequiredArgsConstructor
@ConditionalOnProperty(prefix = "seed", name = "enabled", havingValue = "true", matchIfMissing = true)
public class DataSeeder implements CommandLineRunner {

    private final RoleRepository roleRepository;
    private final TeamRepository teamRepository;
    private final TeamRoleRepository teamRoleRepository;
    private final PasswordEncoder passwordEncoder;

    @Value("${seed.admin-secret:admin-secret}")
    private String adminSecret;

    @Value("${seed.ia-secret:ia-secret}")
    private String iaSecret;

    @Value("${seed.iot-secret:iot-secret}")
    private String iotSecret;

    @Override
    public void run(String... args) {
        seedRoles();
        seedAdminTeam();
        seedIaTeam();
        seedIotTeam();
    }

    private void seedRoles() {
        List<String> roles = List.of("ROLE_IA", "ROLE_IOT", "ROLE_JAVA", "ROLE_ADMIN");
        roles.forEach(name -> roleRepository.findByName(name)
                .orElseGet(() -> {
                    Role role = new Role();
                    role.setName(name);
                    role.setDescription("Seeded role " + name);
                    return roleRepository.save(role);
                }));
    }

    private void seedAdminTeam() {
        Team admin = teamRepository.findByTagIgnoreCase("ADMIN")
                .orElseGet(() -> {
                    Team team = new Team();
                    team.setTag("ADMIN");
                    team.setSecret(passwordEncoder.encode(adminSecret));
                    team.setDescription("Time administrativo padrão");
                    team.setEmails(List.of("admin@humanize.ai"));
                    return teamRepository.save(team);
                });
        assignRole(admin, "ROLE_ADMIN");
    }

    private void seedIaTeam() {
        Team ia = teamRepository.findByTagIgnoreCase("IA")
                .orElseGet(() -> {
                    Team team = new Team();
                    team.setTag("IA");
                    team.setSecret(passwordEncoder.encode(iaSecret));
                    team.setDescription("Time IA padrão");
                    team.setEmails(List.of("ia@humanize.ai"));
                    return teamRepository.save(team);
                });
        assignRole(ia, "ROLE_IA");
    }

    private void seedIotTeam() {
        Team iot = teamRepository.findByTagIgnoreCase("IOT")
                .orElseGet(() -> {
                    Team team = new Team();
                    team.setTag("IOT");
                    team.setSecret(passwordEncoder.encode(iotSecret));
                    team.setDescription("Time IoT padrão");
                    team.setEmails(List.of("iot@humanize.ai"));
                    return teamRepository.save(team);
                });
        assignRole(iot, "ROLE_IOT");
    }

    private void assignRole(Team team, String roleName) {
        Role role = roleRepository.findByName(roleName).orElseThrow();
        boolean alreadyAssigned = teamRoleRepository.findByTeam(team).stream()
                .anyMatch(tr -> tr.getRole().getName().equals(roleName));
        if (!alreadyAssigned) {
            TeamRole teamRole = new TeamRole();
            teamRole.setTeam(team);
            teamRole.setRole(role);
            teamRoleRepository.save(teamRole);
        }
    }
}
