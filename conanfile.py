from conans import ConanFile, CMake, tools

class ZBarConan(ConanFile):
    name = 'zbar'
    lib_version = '0.23.93'
    revision = '1'
    version = '{}-{}'.format(lib_version, revision)
    settings = 'os', 'compiler', 'build_type', 'arch'
    description = 'ZBar QR Code Reader'
    url = 'git@github.com:Pix4D/ZBar.git'
    license = 'LGPL'
    generators = 'cmake'
    exports_sources = [
            'zbar/*',
            'include/*',
            'cmake/*',
            'CMakeLists.txt',
            ]
    options = {
            'shared' : [True, False],
            }
    default_options = 'shared=True'

    def requirements(self):
        if self.settings.os == 'Windows':
            self.requires('libiconv/[>=1.15.0-0, include_prerelease=True]@pix4d/stable')

    def build(self):
        cmake = CMake(self, parallel=True)
        cmake.definitions['BUILD_SHARED_LIBS'] = self.options.shared

        cmake.configure()
        cmake.build(target='install')

    def package_info(self):
        self.cpp_info.includedirs = ['include']  # Ordered list of include paths
        self.cpp_info.libdirs = ['lib']  # Directories where libs are located
        self.cpp_info.libs = ['zbar']

    def package_id(self):
        # Make all options and dependencies (direct and transitive) contribute
        # to the package id
        self.info.requires.full_package_mode()
