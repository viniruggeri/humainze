package com.backend.humainzedash.config;

import com.backend.humainzedash.service.IAHealthService;
import lombok.RequiredArgsConstructor;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

@Component
@RequiredArgsConstructor
public class IAHealthScheduler {

    private final IAHealthService iaHealthService;

    @Scheduled(fixedDelayString = "${ia.health.interval-ms:300000}")
    public void run() {
        iaHealthService.checkHealth();
    }
}
