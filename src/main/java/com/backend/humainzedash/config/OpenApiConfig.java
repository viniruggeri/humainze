package com.backend.humainzedash.config;

import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Contact;
import io.swagger.v3.oas.models.info.Info;
import io.swagger.v3.oas.models.info.License;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class OpenApiConfig {

    @Bean
    public OpenAPI humainzeOpenAPI() {
        return new OpenAPI()
                .info(new Info()
                        .title("Humainze Telemetry API")
                        .description("Backend centralizando telemetria OTEL com RBAC por times")
                        .version("v1")
                        .contact(new Contact().name("Humainze Platform Team").email("platform@humainze.com"))
                        .license(new License().name("Proprietary")));
    }
}

