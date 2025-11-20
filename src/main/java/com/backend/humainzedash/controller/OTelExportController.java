package com.backend.humainzedash.controller;

import com.backend.humainzedash.dto.telemetry.OtelExportResponse;
import com.backend.humainzedash.service.OTelExportService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/export")
@RequiredArgsConstructor
@Tag(name = "OTel Export")
public class OTelExportController {

    private final OTelExportService oTelExportService;

    @Operation(summary = "Exporta métricas em formato OTLP")
    @GetMapping("/metrics")
    public ResponseEntity<Page<OtelExportResponse>> metrics(@RequestParam(required = false) String teamTag,
                                                            Pageable pageable,
                                                            Authentication authentication) {
        return ResponseEntity.ok(oTelExportService.exportMetrics(resolveTeam(authentication, teamTag), pageable));
    }

    @Operation(summary = "Exporta traces em formato OTLP")
    @GetMapping("/traces")
    public ResponseEntity<Page<OtelExportResponse>> traces(@RequestParam(required = false) String teamTag,
                                                           Pageable pageable,
                                                           Authentication authentication) {
        return ResponseEntity.ok(oTelExportService.exportTraces(resolveTeam(authentication, teamTag), pageable));
    }

    @Operation(summary = "Exporta logs em formato OTLP")
    @GetMapping("/logs")
    public ResponseEntity<Page<OtelExportResponse>> logs(@RequestParam(required = false) String teamTag,
                                                         Pageable pageable,
                                                         Authentication authentication) {
        return ResponseEntity.ok(oTelExportService.exportLogs(resolveTeam(authentication, teamTag), pageable));
    }

    private String resolveTeam(Authentication authentication, String requested) {
        boolean admin = authentication.getAuthorities().stream()
                .map(GrantedAuthority::getAuthority)
                .anyMatch("ROLE_ADMIN"::equals);
        if (admin && requested != null) {
            return requested;
        }
        return authentication.getName();
    }
}

