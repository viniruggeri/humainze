package com.backend.humainzedash.controller;

import com.backend.humainzedash.security.ApiKeyService;
import com.backend.humainzedash.security.JwtPayload;
import com.backend.humainzedash.security.JwtService;
import io.opentelemetry.api.trace.Span;
import io.opentelemetry.api.trace.Tracer;
import io.opentelemetry.context.Scope;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@Slf4j
@RestController
@RequestMapping("/auth")
@RequiredArgsConstructor
public class AuthController {

    private final ApiKeyService apiKeyService;
    private final JwtService jwtService;
    private final Tracer tracer;

    @PostMapping("/token")
    public ResponseEntity<?> generateToken(@RequestHeader("X-API-KEY") String apiKey) {
        Span span = tracer.spanBuilder("generate-jwt-token").startSpan();
        try (Scope scope = span.makeCurrent()) {
            log.info("Tentativa de autenticação com API Key");
            span.setAttribute("auth.method", "api-key");

            return apiKeyService.validateApiKey(apiKey)
                    .map(apiKeyData -> {
                        span.setAttribute("team.tag", apiKeyData.teamTag());
                        log.info("Autenticação bem-sucedida para team: {}", apiKeyData.teamTag());

                        JwtPayload payload = new JwtPayload(
                                apiKeyData.teamId(),
                                apiKeyData.teamTag(),
                                apiKeyData.teamTag() + "@humainze.com",
                                apiKeyData.roles());
                        String token = jwtService.generateToken(payload);
                        span.addEvent("Token JWT gerado com sucesso");
                        return ResponseEntity.ok(Map.of("token", token));
                    })
                    .orElseGet(() -> {
                        log.warn("Falha na autenticação: API Key inválida");
                        span.setAttribute("auth.failed", true);
                        return ResponseEntity.status(401).body(Map.of("error", "Invalid API Key"));
                    });
        } finally {
            span.end();
        }
    }
}
