package com.backend.humainzedash.service;

import com.backend.humainzedash.domain.entity.Alert;
import com.backend.humainzedash.dto.alert.AlertRequest;
import com.backend.humainzedash.dto.alert.AlertResponse;
import com.backend.humainzedash.exception.ResourceNotFoundException;
import com.backend.humainzedash.repository.AlertRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;

import java.time.Instant;

@Slf4j
@Service
@RequiredArgsConstructor
public class AlertService {

    private final AlertRepository alertRepository;

    public AlertResponse createAlert(AlertRequest request) {
        log.warn("[AlertService] Criando alerta cognitivo - Team: {}, Type: {}", request.teamTag(), request.type());
        Alert alert = new Alert();
        alert.setTeamTag(request.teamTag());
        alert.setType(request.type());
        alert.setMessage(request.message());
        alert.setTimestamp(Instant.now());
        alert.setResolved(false);
        Alert saved = alertRepository.save(alert);
        log.info("[AlertService] Alerta salvo com ID: {}", saved.getId());
        return toResponse(saved);
    }

    public Page<AlertResponse> listAlerts(String teamTag, Pageable pageable) {
        if (teamTag == null) {
            return alertRepository.findAll(pageable).map(this::toResponse);
        }
        return alertRepository.findByTeamTag(teamTag, pageable).map(this::toResponse);
    }

    public long countUnresolvedAlerts(String teamTag) {
        if (teamTag == null) {
            return alertRepository.countByResolvedFalse();
        }
        return alertRepository.countByTeamTagAndResolvedFalse(teamTag);
    }

    public Page<AlertResponse> listUnresolvedAlerts(String teamTag, Pageable pageable) {
        if (teamTag == null) {
            return alertRepository.findByResolvedFalse(pageable).map(this::toResponse);
        }
        return alertRepository.findByTeamTagAndResolvedFalse(teamTag, pageable).map(this::toResponse);
    }

    public AlertResponse resolveAlert(Long id) {
        log.info("[AlertService] Resolvendo alerta ID: {}", id);
        Alert alert = alertRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Alert not found"));
        alert.setResolved(true);
        Alert resolved = alertRepository.save(alert);
        log.info("[AlertService] Alerta ID: {} marcado como resolvido", id);
        return toResponse(resolved);
    }

    private AlertResponse toResponse(Alert alert) {
        return new AlertResponse(alert.getId(), alert.getTeamTag(), alert.getType(), alert.getMessage(),
                alert.getTimestamp(), alert.isResolved());
    }
}
