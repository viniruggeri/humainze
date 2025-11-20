package com.backend.humainzedash.dto.team;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;

public record TeamMemberRequest(@Email @NotBlank String email) {
}

