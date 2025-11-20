package com.backend.humainzedash.service;

import com.backend.humainzedash.domain.entity.Alert;
import com.backend.humainzedash.dto.alert.AlertRequest;
import com.backend.humainzedash.dto.alert.AlertResponse;
import com.backend.humainzedash.exception.ResourceNotFoundException;
import com.backend.humainzedash.repository.AlertRepository;
import com.backend.humainzedash.repository.TeamRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.ObjectProvider;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.mail.SimpleMailMessage;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.stereotype.Service;

import java.time.Instant;

@Service
@RequiredArgsConstructor
public class AlertService {

    private final AlertRepository alertRepository;
    private final TeamRepository teamRepository;
    private final ObjectProvider<JavaMailSender> mailSenderProvider;

    public AlertResponse createAlert(AlertRequest request) {
        Alert alert = new Alert();
        alert.setTeamTag(request.teamTag());
        alert.setType(request.type());
        alert.setMessage(request.message());
        alert.setTimestamp(Instant.now());
        alert.setResolved(false);
        Alert saved = alertRepository.save(alert);
        sendEmail(saved);
        return toResponse(saved);
    }

    public Page<AlertResponse> listAlerts(String teamTag, Pageable pageable) {
        if (teamTag == null) {
            return alertRepository.findAll(pageable).map(this::toResponse);
        }
        return alertRepository.findByTeamTag(teamTag, pageable).map(this::toResponse);
    }

    public AlertResponse resolveAlert(Long id) {
        Alert alert = alertRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Alert not found"));
        alert.setResolved(true);
        return toResponse(alertRepository.save(alert));
    }

    private void sendEmail(Alert alert) {
        JavaMailSender mailSender = mailSenderProvider.getIfAvailable();
        if (mailSender == null) {
            return; // e-mail não configurado, apenas ignora o envio
        }
        teamRepository.findByTagIgnoreCase(alert.getTeamTag()).ifPresent(team -> {
            if (team.getEmails() == null || team.getEmails().isEmpty()) {
                return;
            }
            SimpleMailMessage message = new SimpleMailMessage();
            message.setTo(team.getEmails().toArray(String[]::new));
            message.setSubject("Alert " + alert.getType());
            message.setText(alert.getMessage());
            mailSender.send(message);
        });
    }

    private AlertResponse toResponse(Alert alert) {
        return new AlertResponse(alert.getId(), alert.getTeamTag(), alert.getType(), alert.getMessage(), alert.getTimestamp(), alert.isResolved());
    }
}
