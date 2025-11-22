package com.backend.humainzedash.config;

import io.opentelemetry.api.OpenTelemetry;
import io.opentelemetry.instrumentation.logback.appender.v1_0.OpenTelemetryAppender;
import io.opentelemetry.sdk.OpenTelemetrySdk;
import jakarta.annotation.PostConstruct;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.context.annotation.Configuration;

@Slf4j
@Configuration
@RequiredArgsConstructor
public class LoggingConfig {

    private final OpenTelemetrySdk openTelemetrySdk;

    @PostConstruct
    public void initializeOpenTelemetryAppender() {
        log.info("Inicializando OpenTelemetry Appender para Logback");
        OpenTelemetryAppender.install(openTelemetrySdk);
        log.info("OpenTelemetry Appender configurado com sucesso");
    }
}
