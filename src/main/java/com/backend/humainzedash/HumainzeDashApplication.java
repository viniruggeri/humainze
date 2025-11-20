package com.backend.humainzedash;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableScheduling;

@SpringBootApplication
@EnableScheduling
public class HumainzeDashApplication {

    public static void main(String[] args) {
        SpringApplication.run(HumainzeDashApplication.class, args);
    }

}
