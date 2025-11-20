package com.backend.humainzedash.service;

import com.backend.humainzedash.domain.entity.Role;
import com.backend.humainzedash.domain.entity.Team;
import com.backend.humainzedash.domain.entity.TeamRole;
import com.backend.humainzedash.dto.team.TeamRequest;
import com.backend.humainzedash.dto.team.TeamResponse;
import com.backend.humainzedash.exception.ResourceNotFoundException;
import com.backend.humainzedash.repository.RoleRepository;
import com.backend.humainzedash.repository.TeamRepository;
import com.backend.humainzedash.repository.TeamRoleRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class TeamService {

    private final TeamRepository teamRepository;
    private final RoleRepository roleRepository;
    private final TeamRoleRepository teamRoleRepository;
    private final PasswordEncoder passwordEncoder;

    public TeamResponse createTeam(TeamRequest request) {
        Team team = new Team();
        team.setTag(request.tag());
        team.setSecret(passwordEncoder.encode(request.secret()));
        team.setDescription(request.description());
        team.setEmails(request.emails());
        Team saved = teamRepository.save(team);
        return toResponse(saved);
    }

    public List<TeamResponse> listTeams() {
        return teamRepository.findAll().stream().map(this::toResponse).toList();
    }

    public TeamResponse getTeam(Long id) {
        return toResponse(findTeam(id));
    }

    public TeamResponse updateTeam(Long id, TeamRequest request) {
        Team team = findTeam(id);
        team.setDescription(request.description());
        team.setEmails(request.emails());
        if (request.secret() != null && !request.secret().isBlank()) {
            team.setSecret(passwordEncoder.encode(request.secret()));
        }
        return toResponse(teamRepository.save(team));
    }

    public void deleteTeam(Long id) {
        teamRepository.delete(findTeam(id));
    }

    public void addRole(Long teamId, String roleName) {
        Team team = findTeam(teamId);
        Role role = roleRepository.findByName(roleName)
                .orElseThrow(() -> new ResourceNotFoundException("Role not found"));
        TeamRole teamRole = new TeamRole();
        teamRole.setTeam(team);
        teamRole.setRole(role);
        teamRoleRepository.save(teamRole);
    }

    public void removeRole(Long teamId, Long roleId) {
        Team team = findTeam(teamId);
        TeamRole teamRole = teamRoleRepository.findByTeam(team).stream()
                .filter(tr -> tr.getRole().getId().equals(roleId))
                .findFirst()
                .orElseThrow(() -> new ResourceNotFoundException("Team role not found"));
        teamRoleRepository.delete(teamRole);
    }

    private Team findTeam(Long id) {
        return teamRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Team not found"));
    }

    private TeamResponse toResponse(Team team) {
        List<String> roles = teamRoleRepository.findByTeam(team).stream()
                .map(tr -> tr.getRole().getName()).toList();
        return new TeamResponse(team.getId(), team.getTag(), team.getDescription(), team.getEmails(), roles);
    }
}

