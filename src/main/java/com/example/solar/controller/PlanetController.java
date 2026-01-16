package com.example.solar.controller;

import com.example.solar.model.Planet;
import com.example.solar.repository.PlanetRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Optional;

@RestController
@RequestMapping("/planet")
public class PlanetController {

    private final PlanetRepository planetRepository;

    @Autowired
    public PlanetController(PlanetRepository planetRepository) {
        this.planetRepository = planetRepository;
    }

    @PostMapping
    public ResponseEntity<Planet> getPlanetById(@RequestBody String id) {
        Optional<Planet> planet = planetRepository.findById(id);
        return planet.map(ResponseEntity::ok).orElseGet(() -> ResponseEntity.notFound().build());
    }
}