package com.bazel.springbootjar.examples.app;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class App {

    public static void main(String[] args) {
        System.out.println("App: Launching the SpringBoot application example...");
        SpringApplication.run(App.class, args);

    }
}
