 
from conans import ConanFile, tools, AutoToolsBuildEnvironment
import shutil
import os

class LibODBSqliteConan( ConanFile ):
    name = "libodb-sqlite"
    version = "2.4.0"
    license = "GPL"
    url = "https://github.com/barcharcraz/conan-packages"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = "shared=False", "fPIC=True"

    requires = ( "libodb/2.4.0@terborg/testing",
                 "sqlite3/3.21.0@bincrafters/stable" )

    def source(self):
        tools.get( "https://www.codesynthesis.com/download/odb/2.4/libodb-sqlite-2.4.0.tar.bz2", sha1="3be07e7702abf8adcbe7736f372ef9980cec1003" )

    def source_path( self ):
        return os.path.join( self.source_folder, self.name + '-' + self.version )

    def build( self ):

        #
        # Here, we remove the stdlib c++, because it can not be found by the configure script
        # for Android. If not removed, configure does not pass the part where it is checking
        # which thread model to use
        #
        if tools.cross_building( self.settings ):
            del self.settings.compiler.libcxx
        
        env_build = AutoToolsBuildEnvironment(self)
        env_build.fpic = self.options.fPIC

        configure_args = []
        if not self.options.shared:
            configure_args.extend( [ '--enable-static', '--disable-shared', '--enable-static-boost' ] )
        
        env_build.configure( configure_dir = self.source_path(), args=configure_args )
        env_build.make()

    def package(self):
        
        self.copy( "*.hxx", dst="include/odb", src= os.path.join( self.source_path(), "odb" )  )

        self.copy( "*.a", dst="lib", keep_path=False )
        self.copy( "*.h", dst="include", keep_path=True )

    def package_info(self):
        self.cpp_info.libs = ["odb-sqlite"]

