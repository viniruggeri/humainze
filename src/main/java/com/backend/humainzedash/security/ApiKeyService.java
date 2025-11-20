package com.backend.humainzedash.security;

import org.springframework.stereotype.Service;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

@Service
public class ApiKeyService {

    private static final Map<String, ApiKeyData> API_KEYS = new HashMap<>();

    static {
        API_KEYS.put("chave-ia", new ApiKeyData("IA", 2L, List.of("ROLE_IA")));
        API_KEYS.put("chave-iot", new ApiKeyData("IOT", 3L, List.of("ROLE_IOT")));
        API_KEYS.put("chave-java", new ApiKeyData("JAVA", 4L, List.of("ROLE_JAVA")));
        API_KEYS.put("chave-admin", new ApiKeyData("ADMIN", 1L, List.of("ROLE_ADMIN")));
    }

    public Optional<ApiKeyData> validateApiKey(String apiKey) {
        return Optional.ofNullable(API_KEYS.get(apiKey));
    }

    public record ApiKeyData(String teamTag, Long teamId, List<String> roles) {
    }
}

