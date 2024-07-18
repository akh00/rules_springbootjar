## Spring Boot jar rule for Bazel

The repository contains single rule that can be used to build proper executable [Spring Boot Jar](https://docs.spring.io/spring-boot/specification/executable-jar/index.html)
The rule was partially inspired by [salesforce rules_spring](https://github.com/salesforce/rules_spring)
but implemented from the scratch using only python (no shell scripts) so it works on Windows as well.


## Usage

In order to use this rule in your project you need to add the selected release version your the WORKSPACE file
(mind to look at the exact sha256 value and current release version in the [releases page](https://github.com/akh00/rules_springbootjar/releases/)

```starlark
http_archive(
    name = "rules_springbootjar",
    sha256 = "fe6bafdc2a13be0bf551b0c9eea2e1d5e2b54a5e31bcaf942014f8fe3f1871a9",
    urls = [
        "https://github.com/akh00/rules_springbootjar/releases/download/0.0.2/rules-springbootjar-0.0.2.zip",
    ],
)
```
then you can use the rule defined like this

```starlark
load("@rules_springbootjar//springbootjar:springbootjar.bzl", "springbootjar")
...

java_library(
    name = "example_applib",
    srcs = glob(["src/main/java/**/*.java"]),
    resources = glob(["src/main/resources/**"]),
    visibility = ["//visibility:public"],
    deps = springboot_deps + ["//example/lib"],
)

springbootjar(
    name = "example_app_boot",
    boot_app_class = "com.bazel.springbootjar.examples.app.App",
    boot_launcher_class = "org.springframework.boot.loader.launch.JarLauncher",
    java_library = ":example_applib",
    deps = ["@maven//:org_springframework_boot_spring_boot_loader", "//example/indirectLib"],
)
```
Also please look at the example app provided
It can be run as the following

```bash
bazel build //example/app:example_app_boot 
```
The you can run the built spring boot jar
```bash
java -jar bazel-bin/example/app/example_app_boot.jar 
```
