from conans import ConanFile, CMake, tools

class NotcursesConan(ConanFile):
    name = "notcurses"
    version = "2.1.4"
    description = "a blingful TUI/character graphics library"
    topics = ("graphics", "curses", "tui", "console", "ncurses")
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://nick-black.com/dankwiki/index.php/Notcurses"
    license = "Apache-2.0"
    exports_sources = ["CMakeLists.txt"]
    settings = "os", "compiler", "build_type", "arch"
    requires = "openimageio/2.2.7.0", "libunistring/0.9.10"
    options = {"shared": [True, False]}
    default_options = {"shared": True}
    generators = "cmake", "pkg_config"

    _cmake = None

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()

    def _configure_cmake(self):
        if self._cmake:
            return self._cmake
        self._cmake = CMake(self)
        self._cmake.definitions["BUILD_TESTING"] = False
        self._cmake.definitions["USE_MULTIMEDIA"] = "oiio"
        self._cmake.definitions["USE_PANDOC"] = False
        self._cmake.definitions["USE_POC"] = False
        self._cmake.definitions["USE_QRCODEGEN"] = False
        self._cmake.definitions["USE_STATIC"] = False if self.options.shared else True
        self._cmake.configure(source_folder="notcurses-" + self.version)
        return self._cmake

    def package_info(self):
        self.cpp_info.libs = ["notcurses", "notcurses++"]
