from conans import ConanFile, CMake, tools
import os


class SpdlogsetupConan(ConanFile):
    name = "spdlog_setup"
    version = "0.3.0-alpha.2"
    license = "MIT"
    author = "guangie88"
    url = "https://github.com/guangie88/spdlog_setup"
    description = "Easy setup of spdlog"
    topics = ("spdlog")
    settings = "os"
    options = { 'threads_prefer_pthread_flag': [True, False],
                'enable_syslog': [True, False] }
    default_options = (
            'threads_prefer_pthread_flag=True',
            'enable_syslog=False'
        )
    generators = "cmake"

    requires = (
        "spdlog/1.3.1@bincrafters/stable",
        "Catch2/2.6.1@catchorg/stable"
    )

    source_dir_name = 'spdlog_setup-' + version

    def source(self):
        tools.download("https://github.com/guangie88/spdlog_setup/archive/v%s.tar.gz" % (self.version), 
                    "spdlog_setup_v%s.tar.gz" % (self.version) )
        tools.untargz("spdlog_setup_v%s.tar.gz" % (self.version) )

        tools.replace_in_file("%s/CMakeLists.txt" % (self.source_dir_name), "project(spdlog_setup VERSION 0.3.0 LANGUAGES CXX)",
        '''project(spdlog_setup VERSION 0.3.0 LANGUAGES CXX)
           include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
           conan_basic_setup()''')

        tools.replace_in_file("%s/CMakeLists.txt" % (self.source_dir_name), 'set(SPDLOG_MIN_VERSION "0.14.0")', 'set(SPDLOG_MIN_VERSION "1.0.0")')

    def build(self):
        cmake = CMake(self)
        cmake.definitions['THREADS_PREFER_PTHREAD_FLAG'] = self.options.threads_prefer_pthread_flag
        cmake.definitions['SPDLOG_ENABLE_SYSLOG'] = self.options.enable_syslog
        cmake.configure(source_folder=self.source_dir_name)
        cmake.build()
        # no test phase
        cmake.install()

    def package(self):
        # relies on the install target to install headers and cmake pkgconfig-style files
        pass
