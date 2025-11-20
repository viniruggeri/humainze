package com.backend.humainzedash.service;

import com.backend.humainzedash.domain.entity.Alert;
import com.backend.humainzedash.dto.alert.AlertRequest;
import com.backend.humainzedash.dto.alert.AlertResponse;
import com.backend.humainzedash.exception.ResourceNotFoundException;
import com.backend.humainzedash.repository.AlertRepository;
import com.backend.humainzedash.repository.TeamRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.ArgumentCaptor;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.springframework.beans.factory.ObjectProvider;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.mail.javamail.JavaMailSender;

import java.util.List;
import java.util.Optional;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

class AlertServiceTest {

    @Mock
    private AlertRepository alertRepository;
    @Mock
    private TeamRepository teamRepository;
    @Mock
    private ObjectProvider<JavaMailSender> mailSenderProvider;

    @InjectMocks
    private AlertService alertService;

    @BeforeEach
    void setup() {
        MockitoAnnotations.openMocks(this);
        // Simula que não há mailSender configurado
        when(mailSenderProvider.getIfAvailable()).thenReturn(null);
    }

    @Test
    void shouldCreateAlert() {
        Alert alert = new Alert();
        alert.setId(1L);
        alert.setTeamTag("IA");
        alert.setType(Alert.AlertType.DRIFT);
        alert.setMessage("Drift detected");

        when(alertRepository.save(any(Alert.class))).thenReturn(alert);

        AlertRequest request = new AlertRequest("IA", Alert.AlertType.DRIFT, "Drift detected");
        AlertResponse response = alertService.createAlert(request);

        assertThat(response.id()).isEqualTo(1L);
        assertThat(response.teamTag()).isEqualTo("IA");
        assertThat(response.type()).isEqualTo(Alert.AlertType.DRIFT);
        assertThat(response.resolved()).isFalse();

        ArgumentCaptor<Alert> captor = ArgumentCaptor.forClass(Alert.class);
        verify(alertRepository).save(captor.capture());
        assertThat(captor.getValue().isResolved()).isFalse();
    }

    @Test
    void shouldResolveAlert() {
        Alert alert = new Alert();
        alert.setId(1L);
        alert.setTeamTag("IA");
        alert.setType(Alert.AlertType.SERVICE_DOWN);
        alert.setMessage("Service is down");
        alert.setResolved(false);

        Alert resolved = new Alert();
        resolved.setId(1L);
        resolved.setResolved(true);

        when(alertRepository.findById(1L)).thenReturn(Optional.of(alert));
        when(alertRepository.save(any(Alert.class))).thenReturn(resolved);

        AlertResponse response = alertService.resolveAlert(1L);

        assertThat(response.resolved()).isTrue();
        verify(alertRepository).save(any(Alert.class));
    }

    @Test
    void shouldThrowWhenAlertNotFound() {
        when(alertRepository.findById(999L)).thenReturn(Optional.empty());

        assertThatThrownBy(() -> alertService.resolveAlert(999L))
                .isInstanceOf(ResourceNotFoundException.class)
                .hasMessageContaining("Alert not found");
    }

    @Test
    void shouldListAllAlertsWhenTeamTagIsNull() {
        Alert alert = new Alert();
        alert.setId(1L);
        alert.setTeamTag("IA");

        Pageable pageable = PageRequest.of(0, 20);
        Page<Alert> page = new PageImpl<>(List.of(alert), pageable, 1);

        when(alertRepository.findAll(pageable)).thenReturn(page);

        Page<AlertResponse> result = alertService.listAlerts(null, pageable);

        assertThat(result.getTotalElements()).isEqualTo(1);
        verify(alertRepository).findAll(pageable);
    }

    @Test
    void shouldListAlertsByTeamTag() {
        Alert alert = new Alert();
        alert.setId(1L);
        alert.setTeamTag("IA");

        Pageable pageable = PageRequest.of(0, 20);
        Page<Alert> page = new PageImpl<>(List.of(alert), pageable, 1);

        when(alertRepository.findByTeamTag("IA", pageable)).thenReturn(page);

        Page<AlertResponse> result = alertService.listAlerts("IA", pageable);

        assertThat(result.getTotalElements()).isEqualTo(1);
        assertThat(result.getContent().get(0).teamTag()).isEqualTo("IA");
        verify(alertRepository).findByTeamTag("IA", pageable);
    }
}

