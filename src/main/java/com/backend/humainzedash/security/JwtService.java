package com.backend.humainzedash.security;

import com.backend.humainzedash.config.JwtProperties;
import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.security.Keys;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import javax.crypto.SecretKey;
import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.Date;
import java.util.List;

@Slf4j
@Service
@RequiredArgsConstructor
public class JwtService {

    private final JwtProperties jwtProperties;

    private SecretKey key() {
        return Keys.hmacShaKeyFor(jwtProperties.secret().getBytes());
    }

    public String generateToken(JwtPayload payload) {
        log.debug("[JwtService] Gerando token JWT para team: {}", payload.teamTag());
        Instant now = Instant.now();
        String token = Jwts.builder()
                .issuer(jwtProperties.issuer())
                .audience().add(jwtProperties.audience()).and()
                .subject(payload.teamTag())
                .issuedAt(Date.from(now))
                .expiration(Date.from(now.plus(jwtProperties.expirationMinutes(), ChronoUnit.MINUTES)))
                .claim("teamId", payload.teamId())
                .claim("teamTag", payload.teamTag())
                .claim("roles", payload.roles())
                .signWith(key())
                .compact();
        log.info("[JwtService] Token JWT gerado para team: {} com roles: {}", payload.teamTag(), payload.roles());
        return token;
    }

    public JwtPayload parseToken(String token) {
        Claims claims = Jwts.parser()
                .verifyWith(key())
                .build()
                .parseSignedClaims(token)
                .getPayload();
        Long teamId = claims.get("teamId", Long.class);
        String teamTag = claims.getSubject();
        @SuppressWarnings("unchecked")
        List<String> roles = (List<String>) claims.get("roles");
        return new JwtPayload(teamId, teamTag, teamTag, roles);
    }
}
