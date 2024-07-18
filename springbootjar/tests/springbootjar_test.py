import os
import zipfile
import tempfile
import shutil
import unittest
import springbootjar


class TestSpringBootJar(unittest.TestCase):

    def setUp(self):
        self.tempdir = tempfile.mkdtemp()
        tempfile.tempdir = self.tempdir
        os.chdir(self.tempdir)

    def tearDown(self):
        shutil.rmtree(self.tempdir)

    def test_springbootjar_happy_path(self):
        appjar = self._create_app_jarfile("com/my/app.jar")
        jar1 = self._create_jarfile("basedir/com/something/jar1.jar", ["com/something/My1.class", "com/something/My2.class"])
        jar2 = self._create_jarfile("basedir/com/somethingelse/jar2.jar", ["org/something/My3.class", "org/something/My4.class"])
        loader = self._create_loader_jarfile("basedir/com/spring-boot-loader.jar")
        springbootjar.run(appjar, "com.something.JarLoader", "com.my.App", "com/my/app_boot.jar", [jar1, jar2, loader])

        assert os.path.exists("com/my/app_boot.jar")
        assert zipfile.is_zipfile("com/my/app_boot.jar")
        assert zipfile.Path("com/my/app_boot.jar", "META-INF/MANIFEST.MF").exists()
        manifest: str = zipfile.Path("com/my/app_boot.jar", "META-INF/MANIFEST.MF").read_text('utf-8')
        assert 'Created-By: bazel_springbootjar_rule' in manifest
        assert 'Main-Class: com.something.JarLoader' in manifest
        assert 'Start-Class: com.my.App' in manifest
        assert zipfile.Path("com/my/app_boot.jar", "META-INF/MANIFEST.MF").exists()
        assert zipfile.Path("com/my/app_boot.jar", "BOOT-INF/lib/jar1.jar").exists()
        assert zipfile.Path("com/my/app_boot.jar", "BOOT-INF/lib/jar2.jar").exists()
        assert zipfile.Path("com/my/app_boot.jar", "BOOT-INF/classes/").exists()
        assert zipfile.Path("com/my/app_boot.jar", "BOOT-INF/classes/application.properties").exists()
        assert zipfile.Path("com/my/app_boot.jar", "BOOT-INF/classes/com/my/pkg/SomeClass.class").exists()
        assert zipfile.Path("com/my/app_boot.jar", "BOOT-INF/classes/com/my/springjar/App.class").exists()
        assert zipfile.Path("com/my/app_boot.jar", "META-INF/services/java.nio.file.spi.FileSystemProvider").exists()
        assert zipfile.Path("com/my/app_boot.jar", "org/springframework/boot/loader/Launcher.class").exists()
        assert zipfile.Path("com/my/app_boot.jar", "org/springframework/boot/loader/tools/LibraryScope.class").exists()

    def _create_jarfile(self, jarname, files = ["com/something/My.class"]):
        with tempfile.TemporaryDirectory() as jar_temp:
            for file in files:
                file_path = os.path.join(jar_temp, file)
                dir_path = os.path.dirname(file_path)
                if not os.path.exists(dir_path):
                    os.makedirs(dir_path)
                with open(file_path, "wb") as fl:
                    fl.write(bytes('deadbeef', 'utf-8'))
            dir_path = os.path.dirname(jarname)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            with zipfile.ZipFile(jarname, 'w') as jar_file:
                for root, dirs, files in os.walk(jar_temp):
                    for directory in dirs:
                        file_path = os.path.join(root, directory)
                        archive_path = os.path.relpath(file_path, jar_temp)
                        jar_file.write(file_path, archive_path)
                    for file in files:
                        file_path = os.path.join(root, file)
                        archive_path = os.path.relpath(file_path, jar_temp)
                        jar_file.write(file_path, archive_path)
        assert os.path.exists(jarname)
        return jarname

    def _create_app_jarfile(self, jarname):
        return self._create_jarfile(jarname, ["com/my/springjar/App.class", "com/my/pkg/SomeClass.class", "application.properties"])

    def _create_loader_jarfile(self, jarname):
        return self._create_jarfile(jarname,
                        ["org/springframework/boot/loader/Launcher.class",
                              "org/springframework/boot/loader/tools/LibraryScope.class",
                              "META-INF/MANIFEST.MF", # this file should not be in the root  
                              "META-INF/services/java.nio.file.spi.FileSystemProvider"])     # this file should be


if __name__ == '__main__':
    unittest.main()
