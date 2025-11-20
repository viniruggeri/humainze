package com.backend.humainzedash.controller;

import com.backend.humainzedash.dto.team.TeamRequest;
import com.backend.humainzedash.dto.team.TeamResponse;
import com.backend.humainzedash.dto.team.TeamRoleRequest;
import com.backend.humainzedash.service.TeamService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PatchMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/teams")
@RequiredArgsConstructor
@Tag(name = "Teams")
public class TeamController {

    private final TeamService teamService;

    @Operation(summary = "Cria um novo time")
    @PostMapping
    public ResponseEntity<TeamResponse> create(@Valid @RequestBody TeamRequest request) {
        return ResponseEntity.status(HttpStatus.CREATED).body(teamService.createTeam(request));
    }

    @Operation(summary = "Lista times")
    @GetMapping
    public ResponseEntity<List<TeamResponse>> list() {
        return ResponseEntity.ok(teamService.listTeams());
    }

    @Operation(summary = "Detalha um time")
    @GetMapping("/{id}")
    public ResponseEntity<TeamResponse> get(@PathVariable Long id) {
        return ResponseEntity.ok(teamService.getTeam(id));
    }

    @Operation(summary = "Atualiza um time")
    @PatchMapping("/{id}")
    public ResponseEntity<TeamResponse> update(@PathVariable Long id, @Valid @RequestBody TeamRequest request) {
        return ResponseEntity.ok(teamService.updateTeam(id, request));
    }

    @Operation(summary = "Remove um time")
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable Long id) {
        teamService.deleteTeam(id);
        return ResponseEntity.noContent().build();
    }

    @Operation(summary = "Adiciona role ao time")
    @PostMapping("/{id}/roles")
    public ResponseEntity<Void> addRole(@PathVariable Long id, @Valid @RequestBody TeamRoleRequest request) {
        teamService.addRole(id, request.roleName());
        return ResponseEntity.status(HttpStatus.CREATED).build();
    }

    @Operation(summary = "Remove role do time")
    @DeleteMapping("/{id}/roles/{roleId}")
    public ResponseEntity<Void> removeRole(@PathVariable Long id, @PathVariable Long roleId) {
        teamService.removeRole(id, roleId);
        return ResponseEntity.noContent().build();
    }
}

