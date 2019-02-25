from conans import ConanFile, CMake, tools
import os


class SpdlogsetupConan(ConanFile):
    name = "spdlog_setup"
    version = "0.4.0"
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
    exports = "CMakeLists.txt", "src/*", "cmake/*"

    requires = (
        "spdlog/1.3.1@bincrafters/stable",
        "Catch2/2.6.1@catchorg/stable"
    )

    def source(self):
#        source_url = "https://github.com/LighthouseJ/spdlog_setup"
#        tools.get("{0}/archive/{1}.tar.gz".format(source_url, self.version))
#        extracted_dir = self.name + "-" + self.version
#        os.rename(extracted_dir, self.source_subfolder)
        git = tools.Git(folder=self.source_folder)
        git.clone("https://github.com/LighthouseJ/spdlog_setup.git", "spdlog_upgrade_and_conanization")

    def build(self):
        cmake = None
        if self.settings.os == 'Linux':
            cmake_eclipse_version = None

            try:
                cmake_eclipse_version = os.environ['CMAKE_ECLIPSE_VERSION']
            except KeyError:
                self.output.info('If developing on Linux and using Eclise CDT, define \\$CMAKE_ECLIPSE_VERSION to generate Eclipse project files')

            if cmake_eclipse_version != None:
                self.output.info('Configuring for Eclipse project generation using Eclipse Version %s' % ( cmake_eclipse_version ) )
                # Generates regular makefiles, but also Eclipse CDT4 project files
                cmake = CMake(self, generator='Eclipse CDT4 - Unix Makefiles')
                # Defines a recent and sufficient Eclipse version to include preprocessor defines, etc...
                cmake.definitions['CMAKE_ECLIPSE_VERSION'] = cmake_eclipse_version
            else: # assume default construction
                cmake = CMake(self)
        else: # assume default construction
            cmake = CMake(self)

        cmake.definitions['THREADS_PREFER_PTHREAD_FLAG'] = self.options.threads_prefer_pthread_flag
        cmake.definitions['SPDLOG_ENABLE_SYSLOG'] = self.options.enable_syslog
        cmake.configure()
        cmake.build()
        cmake.test()

        # Explicit way:
        # self.run('cmake %s/hello %s'
        #          % (self.source_folder, cmake.command_line))
        # self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("*.h", dst="include", src="hello")
        self.copy("*hello.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

