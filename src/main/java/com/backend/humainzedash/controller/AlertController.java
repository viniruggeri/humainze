package com.backend.humainzedash.controller;

import com.backend.humainzedash.dto.alert.AlertRequest;
import com.backend.humainzedash.dto.alert.AlertResponse;
import com.backend.humainzedash.service.AlertService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
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

@RestController
@RequestMapping("/alerts")
@RequiredArgsConstructor
@Tag(name = "Alerts")
public class AlertController {

    private final AlertService alertService;

    @Operation(summary = "Cria alerta cognitivo")
    @PostMapping
    public ResponseEntity<AlertResponse> create(@Valid @RequestBody AlertRequest request) {
        return ResponseEntity.status(HttpStatus.CREATED).body(alertService.createAlert(request));
    }

    @Operation(summary = "Lista alertas por time")
    @GetMapping
    public ResponseEntity<Page<AlertResponse>> list(@RequestParam(required = false) String team,
                                                    Pageable pageable) {
        return ResponseEntity.ok(alertService.listAlerts(team, pageable));
    }

    @Operation(summary = "Resolve alerta")
    @PutMapping("/{id}/resolve")
    public ResponseEntity<AlertResponse> resolve(@PathVariable Long id) {
        return ResponseEntity.ok(alertService.resolveAlert(id));
    }
}

