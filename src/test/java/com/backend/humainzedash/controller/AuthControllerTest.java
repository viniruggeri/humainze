package com.backend.humainzedash.controller;

import com.backend.humainzedash.config.WebMvcTestWithoutSecurity;
import com.backend.humainzedash.dto.auth.LoginRequest;
import com.backend.humainzedash.dto.auth.LoginResponse;
import com.backend.humainzedash.security.ApiKeyService;
import com.backend.humainzedash.service.AuthService;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultHandlers.print;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTestWithoutSecurity(AuthController.class)
class AuthControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private AuthService authService;

    @MockBean
    private ApiKeyService apiKeyService;

    @Test
    void shouldLoginTeam() throws Exception {
        LoginResponse response = new LoginResponse("token", "IA", java.util.List.of("ROLE_IA"));
        Mockito.when(authService.login(Mockito.any(LoginRequest.class))).thenReturn(response);

        mockMvc.perform(post("/auth/login")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"team\":\"IA\",\"secret\":\"secret\"}"))
                .andDo(print())
                .andExpect(status().isOk())
                .andExpect(content().contentType(MediaType.APPLICATION_JSON))
                .andExpect(jsonPath("$.token").value("token"))
                .andExpect(jsonPath("$.team").value("IA"));

        Mockito.verify(authService).login(Mockito.any(LoginRequest.class));
    }
}
