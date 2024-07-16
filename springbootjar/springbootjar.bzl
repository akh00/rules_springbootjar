# /
# /META-INF/
# /META-INF/MANIFEST.MF                      -- spring boot specific manifest                  
# /BOOT-INF
# /BOOT-INF/classes
# /BOOT-INF/classes/**/*.class                 -- app classes
# /BOOT-INF/classes/META-INF/*                 -- app config files (e.g. spring.factories)
# /BOOT-INF/lib
# /BOOT-INF/lib/*.jar                          -- app dependency jars
# /org/springframework/boot/loader
# /org/springframework/boot/loader/**/*.class  -- the Spring Boot Loader classes


# ***************************************************************
# Package spring boot jar

def _springbootjar_impl(ctx):
    # declare output file
    output = ctx.actions.declare_file(ctx.attr.name +".jar")
    outputs = [output]
    
    dependencies = [ctx.attr.java_library]
    dependencies += ctx.attr.deps

    dep_jars = java_common.merge([dep[java_common.provider] for dep in dependencies]).transitive_runtime_jars.to_list()

    inputs = []
    inputs += [ctx.attr.java_library.files.to_list()[0]]
    inputs += dep_jars

    input_args = ctx.actions.args()
    input_args.add(ctx.attr.java_library.files.to_list()[0])
    input_args.add(ctx.attr.boot_launcher_class)
    input_args.add(ctx.attr.boot_app_class)
    input_args.add(output.path)
    input_args.add_all(dep_jars)
    
    ctx.actions.run(
        executable = ctx.executable._script,
        outputs = outputs,
        inputs = inputs,
        arguments = [input_args],
        progress_message = "Building spring boot jar...",
        mnemonic = "SpringBootJarPkg",
    )
    return [DefaultInfo(files = depset(outputs))]

""" The rule for packaging an executable Spring Boot jar.
    Args:
      name: the name of the application.  Required.
      java_library: the main app library of this module. Required.
      boot_app_class: The fully qualified app main class name. Required.
      boot_launcher_class: The fully qualified boot loader class name. Default to 'org.springframework.boot.loader.JarLauncher'
      deps: Additional dependencies which aren't direct or transitive dependencies for 'java_library'. Default to []
    """

springbootjar = rule(
    implementation = _springbootjar_impl,
    attrs = {
        "_script": attr.label(
            default = Label("@rules_springbootjar//springbootjar:springbootjar"),
            executable = True,
            cfg = "exec",
            allow_files = True,
        ),
        "boot_app_class": attr.string(mandatory = True),
        "boot_launcher_class": attr.string( default = "org.springframework.boot.loader.JarLauncher"),
        "java_library": attr.label(),
        "deps":  attr.label_list( default = []),
    },
)
