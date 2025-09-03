from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps, cmake_layout

class ZBarConan(ConanFile):
    name = 'zbar'
    version = '0.23.93'
    settings = 'os', 'compiler', 'build_type', 'arch'
    description = 'ZBar QR Code Reader'
    url = 'git@github.com:Pix4D/ZBar.git'
    license = 'LGPL'
    exports_sources = [
            'zbar/*',
            'include/*',
            'cmake/*',
            'CMakeLists.txt',
            ]
    package_type = "library"
    options = {
        "shared" : [True],
    }
    default_options = {
        "shared": True
    }

    def layout(self):
        cmake_layout(self)
        self.cpp.package.builddirs.append("lib/cmake")

    def package_info(self):
        self.cpp_info.set_property("cmake_find_mode", "none")

    def requirements(self):
        if self.settings.os == 'Windows':
            self.requires('libiconv/[>=1.15]')

    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()
        tc = CMakeToolchain(self)
        cmake_defs = {
            'BUILD_SHARED_LIBS': True,
        }
        tc.variables.update(cmake_defs)
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()
