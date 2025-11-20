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
import lombok.RequiredArgsConstructor;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
@RequiredArgsConstructor
public class AuthService {

    private final TeamRepository teamRepository;
    private final TeamRoleRepository teamRoleRepository;
    private final PasswordEncoder passwordEncoder;
    private final JwtService jwtService;

    @Transactional(readOnly = true)
    public LoginResponse login(LoginRequest request) {
        Team team = teamRepository.findByTagIgnoreCase(request.team())
                .orElseThrow(() -> new ResourceNotFoundException("Team not found"));
        if (!passwordEncoder.matches(request.secret(), team.getSecret())) {
            throw new IllegalArgumentException("Invalid credentials");
        }
        List<String> roles = teamRoleRepository.findByTeam(team).stream()
                .map(TeamRole::getRole)
                .map(role -> role.getName())
                .toList();
        JwtPayload payload = new JwtPayload(team.getId(), team.getTag(), team.getTag(), roles);
        String token = jwtService.generateToken(payload);
        return new LoginResponse(token, team.getTag(), roles);
    }
}
