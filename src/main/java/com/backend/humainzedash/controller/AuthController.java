package com.backend.humainzedash.controller;

import com.backend.humainzedash.security.ApiKeyService;
import com.backend.humainzedash.security.JwtPayload;
import com.backend.humainzedash.security.JwtService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/auth")
@RequiredArgsConstructor
public class AuthController {

    private final ApiKeyService apiKeyService;
    private final JwtService jwtService;

    @PostMapping("/token")
    public ResponseEntity<?> generateToken(@RequestHeader("X-API-KEY") String apiKey) {
        return apiKeyService.validateApiKey(apiKey)
                .map(apiKeyData -> {
                    JwtPayload payload = new JwtPayload(
                            apiKeyData.teamId(),
                            apiKeyData.teamTag(),
                            apiKeyData.teamTag(),
                            apiKeyData.roles()
                    );
                    String token = jwtService.generateToken(payload);
                    return ResponseEntity.ok(Map.of("token", token));
                })
                .orElse(ResponseEntity.status(401).body(Map.of("error", "Invalid API Key")));
    }
}

