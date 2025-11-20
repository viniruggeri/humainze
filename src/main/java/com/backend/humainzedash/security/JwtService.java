package com.backend.humainzedash.security;

import com.backend.humainzedash.config.JwtProperties;
import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.security.Keys;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import javax.crypto.SecretKey;
import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.Date;
import java.util.List;
import java.util.Map;

@Service
@RequiredArgsConstructor
public class JwtService {

    private final JwtProperties jwtProperties;

    private SecretKey key() {
        return Keys.hmacShaKeyFor(jwtProperties.secret().getBytes());
    }

    public String generateToken(JwtPayload payload) {
        Instant now = Instant.now();
        return Jwts.builder()
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
    }

    public JwtPayload parseToken(String token) {
        Claims claims = Jwts.parser()
                .verifyWith(key())
                .build()
                .parseSignedClaims(token)
                .getPayload();
        Long teamId = claims.get("teamId", Long.class);
        String teamTag = claims.getSubject();
        List<String> roles = claims.get("roles", List.class);
        return new JwtPayload(teamId, teamTag, teamTag, roles);
    }
}
