package com.backend.humainzedash.controller;

import com.backend.humainzedash.dto.alert.AlertRequest;
import com.backend.humainzedash.dto.alert.AlertResponse;
import com.backend.humainzedash.service.AlertService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.security.SecurityRequirement;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@Slf4j
@RestController
@RequestMapping("/alerts")
@RequiredArgsConstructor
@Tag(name = "Alerts")
@SecurityRequirement(name = "jwtAuth")
public class AlertController {

    private final AlertService alertService;

    @Operation(summary = "Cria alerta cognitivo")
    @PostMapping
    public ResponseEntity<AlertResponse> create(@Valid @RequestBody AlertRequest request) {
        log.warn("Alerta cognitivo recebido - Team: {}, Type: {}", request.teamTag(), request.type());
        AlertResponse response = alertService.createAlert(request);
        log.info("Alerta criado com ID: {}", response.id());
        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }

    @Operation(summary = "Lista alertas por time")
    @GetMapping
    public ResponseEntity<Page<AlertResponse>> list(@RequestParam(required = false) String team,
            Pageable pageable) {
        log.debug("Listando alertas - Team: {}", team != null ? team : "ALL");
        Page<AlertResponse> alerts = alertService.listAlerts(team, pageable);
        log.info("Total de alertas: {}", alerts.getTotalElements());
        return ResponseEntity.ok(alerts);
    }

    @Operation(summary = "Lista apenas alertas não resolvidos")
    @GetMapping("/unresolved")
    public ResponseEntity<Page<AlertResponse>> listUnresolved(@RequestParam(required = false) String team,
            Pageable pageable) {
        log.debug("Listando alertas não resolvidos - Team: {}", team != null ? team : "ALL");
        Page<AlertResponse> alerts = alertService.listUnresolvedAlerts(team, pageable);
        log.info("Total de alertas não resolvidos: {}", alerts.getTotalElements());
        return ResponseEntity.ok(alerts);
    }

    @Operation(summary = "Conta alertas não resolvidos")
    @GetMapping("/unresolved/count")
    public ResponseEntity<Long> countUnresolved(@RequestParam(required = false) String team) {
        log.debug("Contando alertas não resolvidos - Team: {}", team != null ? team : "ALL");
        long count = alertService.countUnresolvedAlerts(team);
        log.info("Alertas não resolvidos: {}", count);
        return ResponseEntity.ok(count);
    }

    @Operation(summary = "Resolve alerta")
    @PutMapping("/{id}/resolve")
    public ResponseEntity<AlertResponse> resolve(@PathVariable Long id) {
        log.info("Resolvendo alerta ID: {}", id);
        AlertResponse response = alertService.resolveAlert(id);
        log.info("Alerta ID: {} resolvido com sucesso", id);
        return ResponseEntity.ok(response);
    }
}
