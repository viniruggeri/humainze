package com.backend.humainzedash.repository;

import com.backend.humainzedash.domain.entity.Team;
import com.backend.humainzedash.domain.entity.TeamRole;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;

public interface TeamRoleRepository extends JpaRepository<TeamRole, Long> {

    @Query("SELECT tr FROM TeamRole tr JOIN FETCH tr.role WHERE tr.team = :team")
    List<TeamRole> findByTeam(@Param("team") Team team);
}

