from spack import *

class MpiTests(CMakePackage):
    """mpi_tests: a collection of MPI tests"""

    homepage = "https://github.com/JiakunYan/mpi_tests.git"
    git      = "https://github.com/JiakunYan/mpi_tests.git"

    maintainers("JiakunYan")

    version('master', branch='master')

    depends_on("mpi")
    depends_on("lci")

    def cmake_args(self):
        return []
