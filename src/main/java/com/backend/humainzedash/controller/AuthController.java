package com.backend.humainzedash.controller;

import com.backend.humainzedash.dto.auth.LoginRequest;
import com.backend.humainzedash.dto.auth.LoginResponse;
import com.backend.humainzedash.security.JwtPayload;
import com.backend.humainzedash.service.AuthService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/auth")
@RequiredArgsConstructor
@Tag(name = "Auth")
public class AuthController {

    private final AuthService authService;

    @Operation(summary = "Login via team secret")
    @PostMapping("/login")
    public ResponseEntity<LoginResponse> login(@Valid @RequestBody LoginRequest request) {
        return ResponseEntity.ok(authService.login(request));
    }

    @Operation(summary = "Perfil do token atual")
    @GetMapping("/me")
    public ResponseEntity<JwtPayload> me(@AuthenticationPrincipal UserDetails userDetails) {
        JwtPayload payload = new JwtPayload(null, userDetails.getUsername(), userDetails.getUsername(),
                userDetails.getAuthorities().stream().map(Object::toString).toList());
        return ResponseEntity.ok(payload);
    }
}
