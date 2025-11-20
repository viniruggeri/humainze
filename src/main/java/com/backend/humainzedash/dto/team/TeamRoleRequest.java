package com.backend.humainzedash.dto.team;

import jakarta.validation.constraints.NotBlank;

public record TeamRoleRequest(@NotBlank String roleName) {
}

