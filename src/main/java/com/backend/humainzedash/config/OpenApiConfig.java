package com.backend.humainzedash.config;

import io.swagger.v3.oas.annotations.enums.SecuritySchemeIn;
import io.swagger.v3.oas.annotations.enums.SecuritySchemeType;
import io.swagger.v3.oas.annotations.security.SecurityRequirement;
import io.swagger.v3.oas.annotations.security.SecurityScheme;
import io.swagger.v3.oas.annotations.OpenAPIDefinition;
import io.swagger.v3.oas.models.info.Contact;
import io.swagger.v3.oas.models.info.Info;
import io.swagger.v3.oas.models.info.License;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
@OpenAPIDefinition(
        security = {
                @SecurityRequirement(name = "jwtAuth"),
                @SecurityRequirement(name = "apiKeyAuth")
        }
)
@SecurityScheme(
        name = "jwtAuth",
        type = SecuritySchemeType.HTTP,
        scheme = "bearer",
        bearerFormat = "JWT"
)
@SecurityScheme(
        name = "apiKeyAuth",
        type = SecuritySchemeType.APIKEY,
        in = SecuritySchemeIn.HEADER,
        paramName = "X-API-KEY"
)
public class OpenApiConfig {

    @Bean
    public io.swagger.v3.oas.models.OpenAPI humainzeOpenAPI() {
        return new io.swagger.v3.oas.models.OpenAPI()
                .info(new Info()
                        .title("Humainze Telemetry API")
                        .description("Backend centralizando telemetria OTEL com RBAC por times")
                        .version("v1")
                        .contact(new Contact()
                                .name("Humainze Platform Team")
                                .email("platform@humainze.com"))
                        .license(new License().name("Proprietary")));
    }
}
