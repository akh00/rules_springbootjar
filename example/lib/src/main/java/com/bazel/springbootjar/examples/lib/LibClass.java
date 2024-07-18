package com.bazel.springbootjar.examples.lib;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.PropertySource;

@Configuration
@PropertySource(value = "additional.properties", ignoreResourceNotFound = true)
public class LibClass {

    @Value("app.property1")
    private String appProp;
    @Bean
    public String bean1() {
        return "property:" + appProp;
    }

    @Bean
    @ConditionalOnProperty(value = "external.property.load.bean2", havingValue = "true", matchIfMissing = false)
    public String bean2() {
        return "bean2";
    }
}
