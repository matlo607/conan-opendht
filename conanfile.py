#!/usr/bin/env python3

import os
import shutil
from conans import ConanFile, CMake, tools

class OpenDHTConan(ConanFile):
    name = "opendht"
    version = "master"
    description = """A C++11 Distributed Hash Table implementation"""
    url = "https://github.com/savoirfairelinux/opendht"
    license = "GNU GPLv3"
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    sources = "https://github.com/matlo607/opendht.git"
    source_dir = "{name}-{version}".format(name=name, version=version)
    scm = {
        "type": "git",
        "subfolder": source_dir,
        "url": sources,
        "revision": "conan-fix-build-cmake"
    }
    exports_sources = "CMakeLists.txt"

    def requirements(self):
        self.requires("argon2/master@matthieu/testing")
        self.requires("gnutls/3.6.2@mlongo/testing")
        self.requires("msgpack-c/3.0.1@mlongo/testing")
        self.requires("nettle/3.4@DEGoodmanWilson/stable")

    def source(self):
        with tools.chdir(self.source_dir):
            os.rename("CMakeLists.txt", "CMakeListsOriginal.cmake")
        shutil.move("CMakeLists.txt", self.source_dir)

    def build(self):
        cmake = CMake(self)
        cmake.verbose = True
        cmake.definitions["OPENDHT_SHARED"] = "OFF"
        cmake.definitions["OPENDHT_PYTHON"] = "ON"
        cmake.definitions["OPENDHT_BUILD_TOOLS"] = "ON"
        cmake.definitions["OPENDHT_PROXY_SERVER"] = "OFF"
        cmake.definitions["OPENDHT_PROXY_SERVER_IDENTITY"] = "ON"
        cmake.definitions["OPENDHT_PROXY_CLIENT"] = "OFF"
        cmake.definitions["OPENDHT_PUSH_NOTIFICATIONS"] = "OFF"
        cmake.definitions["OPENDHT_ARGON2"] = "OFF"
        #cmake.definitions["OPENDHT_TEST"] = "ON"
        cmake.configure(source_folder=self.source_dir)
        cmake.build()
        #cmake.test()
        cmake.install()

    def package(self):
        # already done by 'make install'
        pass

    def package_info(self):
        pass
        #self.cpp_info.includedirs = ['include']
        #self.cpp_info.libdirs = ['lib']
        #self.cpp_info.bindirs = ['bin']
        #self.env_info.path.append(path.join(self.package_folder, "bin"))
