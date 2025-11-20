package com.backend.humainzedash.controller;

import com.backend.humainzedash.dto.team.TeamRequest;
import com.backend.humainzedash.dto.team.TeamResponse;
import com.backend.humainzedash.dto.team.TeamRoleRequest;
import com.backend.humainzedash.service.TeamService;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.security.test.context.support.WithMockUser;
import org.springframework.test.web.servlet.MockMvc;

import java.util.List;

import static org.springframework.security.test.web.servlet.request.SecurityMockMvcRequestPostProcessors.csrf;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@WebMvcTest(TeamController.class)
class TeamControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private TeamService teamService;

    @Test
    @WithMockUser(roles = "ADMIN")
    void shouldCreateTeam() throws Exception {
        TeamResponse response = new TeamResponse(1L, "IA", "Time IA", List.of("ia@humanize.ai"), List.of("ROLE_IA"));
        Mockito.when(teamService.createTeam(Mockito.any(TeamRequest.class))).thenReturn(response);

        mockMvc.perform(post("/teams")
                .with(csrf())
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"tag\":\"IA\",\"secret\":\"secret123\",\"description\":\"Time IA\",\"emails\":[\"ia@humanize.ai\"]}"))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.id").value(1))
                .andExpect(jsonPath("$.tag").value("IA"));
    }

    @Test
    @WithMockUser(roles = "ADMIN")
    void shouldListTeams() throws Exception {
        List<TeamResponse> teams = List.of(
                new TeamResponse(1L, "IA", "Time IA", List.of(), List.of("ROLE_IA")),
                new TeamResponse(2L, "IOT", "Time IOT", List.of(), List.of("ROLE_IOT"))
        );
        Mockito.when(teamService.listTeams()).thenReturn(teams);

        mockMvc.perform(get("/teams"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$[0].tag").value("IA"))
                .andExpect(jsonPath("$[1].tag").value("IOT"));
    }

    @Test
    @WithMockUser(roles = "ADMIN")
    void shouldGetTeam() throws Exception {
        TeamResponse response = new TeamResponse(1L, "IA", "Time IA", List.of(), List.of("ROLE_IA"));
        Mockito.when(teamService.getTeam(1L)).thenReturn(response);

        mockMvc.perform(get("/teams/1"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.tag").value("IA"));
    }

    @Test
    @WithMockUser(roles = "ADMIN")
    void shouldAddRoleToTeam() throws Exception {
        Mockito.doNothing().when(teamService).addRole(1L, "ROLE_IA");

        mockMvc.perform(post("/teams/1/roles")
                .with(csrf())
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"roleName\":\"ROLE_IA\"}"))
                .andExpect(status().isCreated());

        Mockito.verify(teamService).addRole(1L, "ROLE_IA");
    }

    @Test
    @WithMockUser(roles = "ADMIN")
    void shouldRemoveRoleFromTeam() throws Exception {
        Mockito.doNothing().when(teamService).removeRole(1L, 2L);

        mockMvc.perform(delete("/teams/1/roles/2")
                .with(csrf()))
                .andExpect(status().isNoContent());

        Mockito.verify(teamService).removeRole(1L, 2L);
    }
}

