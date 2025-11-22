package com.backend.humainzedash.controller;

import com.backend.humainzedash.dto.team.TeamRequest;
import com.backend.humainzedash.dto.team.TeamResponse;
import com.backend.humainzedash.dto.team.TeamRoleRequest;
import com.backend.humainzedash.service.TeamService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
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

@Slf4j
@RestController
@RequestMapping("/teams")
@RequiredArgsConstructor
@Tag(name = "Teams")
public class TeamController {

    private final TeamService teamService;

    @Operation(summary = "Cria um novo time")
    @PostMapping
    public ResponseEntity<TeamResponse> create(@Valid @RequestBody TeamRequest request) {
        log.info("Criando novo time: {}", request.tag());
        TeamResponse response = teamService.createTeam(request);
        log.info("Time criado com sucesso - ID: {}, Tag: {}", response.id(), response.tag());
        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }

    @Operation(summary = "Lista times")
    @GetMapping
    public ResponseEntity<List<TeamResponse>> list() {
        log.debug("Listando todos os times");
        List<TeamResponse> teams = teamService.listTeams();
        log.info("Total de times encontrados: {}", teams.size());
        return ResponseEntity.ok(teams);
    }

    @Operation(summary = "Detalha um time")
    @GetMapping("/{id}")
    public ResponseEntity<TeamResponse> get(@PathVariable Long id) {
        log.debug("Buscando detalhes do time ID: {}", id);
        TeamResponse team = teamService.getTeam(id);
        log.info("Time encontrado - ID: {}, Tag: {}", team.id(), team.tag());
        return ResponseEntity.ok(team);
    }

    @Operation(summary = "Atualiza um time")
    @PatchMapping("/{id}")
    public ResponseEntity<TeamResponse> update(@PathVariable Long id, @Valid @RequestBody TeamRequest request) {
        return ResponseEntity.ok(teamService.updateTeam(id, request));
    }

    @Operation(summary = "Remove um time")
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable Long id) {
        log.warn("Deletando time ID: {}", id);
        teamService.deleteTeam(id);
        log.info("Time ID: {} deletado com sucesso", id);
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
