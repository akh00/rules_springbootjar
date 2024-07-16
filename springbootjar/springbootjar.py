import os
import sys
import logging
import tempfile
import shutil
import zipfile

logger = logging.getLogger('springbootjar')

manifest_template = """Manifest-Version: 1.0
Created-By: bazel_springbootjar_rule
Main-Class: {0}
Start-Class: {1}
"""


def springbootjar_impl(appjar, bootloader, mainclass, outputjar, deplibs):
    try:
        orig_dir = os.getcwd()
        tempfile.tempdir = orig_dir
        logger.error(f"orig_dir {orig_dir=}")
        with tempfile.TemporaryDirectory() as base_working_dir:
            working_dir = base_working_dir + "/working"
            boot_classes = working_dir + "/BOOT-INF/classes"
            boot_libs = working_dir + "/BOOT-INF/lib"
            meta_inf = working_dir + "/META-INF"
            os.makedirs(boot_classes)
            os.makedirs(boot_libs)
            os.makedirs(meta_inf)
            with open(meta_inf + "/MANIFEST.MF", "w") as manifest:
                manifest.write(manifest_template.format(bootloader, mainclass))
            with zipfile.ZipFile(appjar, 'r') as app_jar_ref:
                app_jar_ref.extractall(boot_classes)
            deplibs.remove(appjar)
            for jarname in deplibs:
                #   logger.info(f"jarpath {jarname=}")
                if ("spring-boot-loader" in jarname
                    or "spring_boot_loader" in jarname):
                    with zipfile.ZipFile(jarname, "r") as loader_jar:
                        loader_jar.extractall(working_dir,
                                              [info for info in loader_jar.infolist()
                                               if ((info.filename.startswith("org/") or
                                                    info.filename.startswith("com/") or
                                                    info.filename.startswith("META-INF/services/"))
                                                   and not info.is_dir())])
                else:
                    base_jar_name = os.path.basename(jarname)
                    if not os.path.exists(os.path.join(boot_libs, base_jar_name)):
                        shutil.copy(jarname, boot_libs)
                    else:
                        logger.warning(f"skipping duplicate file {jarname=}")
            #   logger.info(f"creating output jar {outputjar=}")
            with zipfile.ZipFile(outputjar, 'w') as jarf:
                for root, dirs, files in os.walk(working_dir):
                    for dir in dirs:
                        file_path = os.path.join(root, dir)
                        archive_path = os.path.relpath(file_path, working_dir)
                        jarf.write(file_path, archive_path)
                    for file in files:
                        file_path = os.path.join(root, file)
                        archive_path = os.path.relpath(file_path, working_dir)
                        jarf.write(file_path, archive_path)

    except Exception as err:
        logger.error(f"Unexpected {err=}, {type(err)=}, {err.args=}")
    return


def run(appjar, bootloader, mainclass, outputjar, deplibs):
    springbootjar_impl(appjar, bootloader, mainclass, outputjar, deplibs)


if __name__ == "__main__":
    # arg1  appjar - contains the .class files for the Spring Boot application
    # arg2  bootloader - classname of the Spring Boot Loader to use - optional
    # arg3  mainclass - classname of the @SpringBootApplication class for the manifest.MF file entry
    # arg4  output jar
    # arg5....  deplibs - list of upstream transitive dependencies, these will be incorporated into the jar file in BOOT-INF/lib
    outputjar = str(sys.argv[1])
    if len(sys.argv[4]) > 0:
        outputjar = sys.argv[4]
    bootloader = "org.springframework.boot.loader.launch.JarLauncher"
    if len(sys.argv[2]) > 0:
        bootloader = sys.argv[2]
    deplibs = sys.argv[5:]

    run(sys.argv[1], bootloader, sys.argv[3], outputjar, deplibs)
