package com.bazel.springbootjar.examples.app;

import org.springframework.beans.BeansException;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.ApplicationContext;
import org.springframework.context.ApplicationContextAware;
import org.springframework.context.annotation.Import;

import com.bazel.springbootjar.examples.lib.LibClass;

@SpringBootApplication
@Import(LibClass.class)
public class App implements ApplicationContextAware {

    public static void main(String[] args) {
        System.out.println("App: Launching the SpringBoot application example...");
        SpringApplication.run(App.class, args);

    }

    @Override
    public void setApplicationContext(ApplicationContext applicationContext) throws BeansException {
        String bean1 = applicationContext.getBean("bean1", String.class);
        System.out.println("++++++++++++++++++++++++++++++Bean 1 is loaded:" + bean1 );
        String bean2 = applicationContext.getBean("bean2", String.class);
        System.out.println("++++++++++++++++++++++++++++++Bean 2 is loaded due to indirectLib:" + bean2 );
    }
}
