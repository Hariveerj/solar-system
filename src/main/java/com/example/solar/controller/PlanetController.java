package com.example.solar.controller;

import com.example.solar.model.Planet;
import com.example.solar.repository.PlanetRepository;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/planet")
public class PlanetController {

    private final PlanetRepository planetRepository;

    public PlanetController(PlanetRepository planetRepository) {
        this.planetRepository = planetRepository;
    }

    @PostMapping("/{id}")
    public Planet getPlanet(@PathVariable String id) {
        return planetRepository.findById(Long.parseLong(id))
                .orElseThrow(() -> new RuntimeException("Planet not found"));
    }
}