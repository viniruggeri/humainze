package com.backend.humainzedash.config;

import io.micrometer.core.instrument.MeterRegistry;
import io.opentelemetry.exporter.otlp.logs.OtlpGrpcLogRecordExporter;
import io.opentelemetry.exporter.otlp.metrics.OtlpGrpcMetricExporter;
import io.opentelemetry.exporter.otlp.trace.OtlpGrpcSpanExporter;
import io.opentelemetry.sdk.OpenTelemetrySdk;
import io.opentelemetry.sdk.logs.SdkLoggerProvider;
import io.opentelemetry.sdk.logs.export.LogRecordExporter;
import io.opentelemetry.sdk.logs.export.SimpleLogRecordProcessor;
import io.opentelemetry.sdk.metrics.SdkMeterProvider;
import io.opentelemetry.sdk.metrics.export.PeriodicMetricReader;
import io.opentelemetry.sdk.metrics.export.MetricExporter;
import io.opentelemetry.sdk.resources.Resource;
import io.opentelemetry.sdk.trace.SdkTracerProvider;
import io.opentelemetry.sdk.trace.export.BatchSpanProcessor;
import io.opentelemetry.sdk.trace.export.SpanExporter;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.actuate.autoconfigure.metrics.MeterRegistryCustomizer;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class TelemetryConfig {

    @Value("${otel.exporter.otlp.endpoint:http://signoz:4317}")
    private String otlpEndpoint;

    @Bean
    public SpanExporter spanExporter() {
        return OtlpGrpcSpanExporter.builder().setEndpoint(otlpEndpoint).build();
    }

    @Bean
    public MetricExporter metricExporter() {
        return OtlpGrpcMetricExporter.builder().setEndpoint(otlpEndpoint).build();
    }

    @Bean
    public LogRecordExporter logRecordExporter() {
        return OtlpGrpcLogRecordExporter.builder().setEndpoint(otlpEndpoint).build();
    }

    @Bean
    @ConditionalOnProperty(prefix = "otel.export", name = "enabled", havingValue = "true", matchIfMissing = true)
    public OpenTelemetrySdk openTelemetrySdk(SpanExporter spanExporter,
                                             MetricExporter metricExporter,
                                             LogRecordExporter logRecordExporter,
                                             @Value("${telemetry.teamTag:humanize}") String teamTag) {
        Resource resource = Resource.builder()
                .put("service.name", "humainze-dash")
                .put("team", teamTag)
                .build();

        SdkTracerProvider tracerProvider = SdkTracerProvider.builder()
                .setResource(resource)
                .addSpanProcessor(BatchSpanProcessor.builder(spanExporter).build())
                .build();

        SdkMeterProvider meterProvider = SdkMeterProvider.builder()
                .setResource(resource)
                .registerMetricReader(PeriodicMetricReader.builder(metricExporter).build())
                .build();

        SdkLoggerProvider loggerProvider = SdkLoggerProvider.builder()
                .setResource(resource)
                .addLogRecordProcessor(SimpleLogRecordProcessor.create(logRecordExporter))
                .build();

        return OpenTelemetrySdk.builder()
                .setTracerProvider(tracerProvider)
                .setMeterProvider(meterProvider)
                .setLoggerProvider(loggerProvider)
                .build();
    }

    /**
     * Customiza o MeterRegistry já criado pelo Spring Boot (micrometer-registry-otlp)
     * adicionando tags padrão, sem precisar de OpenTelemetryMeterRegistry.
     */
    @Bean
    MeterRegistryCustomizer<MeterRegistry> meterRegistryCustomizer(
            @Value("${telemetry.teamTag:humanize}") String teamTag) {
        return registry -> registry.config().commonTags("service", "humainze-dash", "team", teamTag);
    }
}
