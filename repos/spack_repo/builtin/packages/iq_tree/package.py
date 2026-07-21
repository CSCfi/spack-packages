# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class IqTree(CMakePackage):
    """IQ-TREE Efficient software for phylogenomic inference"""

    homepage = "http://www.iqtree.org"
    git = "https://github.com/iqtree/iqtree2.git"
    url = "https://github.com/Cibiv/IQ-TREE/archive/v1.6.12.tar.gz"

    license("GPL-2.0-or-later")

    version(
        "2.4.0", tag="v2.4.0", commit="977cc4324234b36fbfb80b326b8e43b73952e365", submodules=True
    )
    version(
        "2.3.2", tag="v2.3.1", commit="60f1aa68646ab84cc96b55a7548707adde15f47a", submodules=True
    )
    version(
        "2.3.1", tag="v2.3.1", commit="2914a2f7aac0a1a3c4fadde42c83e5dee315186d", submodules=True
    )
    version(
        "2.2.2.7",
        tag="v2.2.2.7",
        commit="bd3468c7af6572ea29002dfdba377804f8f56c26",
        submodules=True,
    )
    version(
        "2.1.3", tag="v2.1.3", commit="3d31be9e56b05ffbc5f8488fc8285597b433c99f", submodules=True
    )
    version(
        "2.0.6", tag="v2.0.6", commit="219e88407ac915a209a29808a81084bf0d5f1a84", submodules=True
    )
    version("1.6.12", sha256="9614092de7a157de82c9cc402b19cc8bfa0cb0ffc93b91817875c2b4bb46a284")

    variant("openmp", default=True, description="Enable OpenMP support.")
    variant("mpi", default=False, description="Enable MPI support.")
    variant("lsd2", default=True, description="Activate Least Squares Dating.")

    maintainers("ilbiondo")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    # Depends on Eigen3 and zlib
    depends_on("boost+container+math+exception")
    depends_on("eigen@3")
    depends_on("zlib-api")

    depends_on("mpi", when="+mpi")

    def cmake_args(self):
        spec = self.spec

        args = []

        # IQ-TREE's CMakeLists.txt runs a bare `find_package(Eigen3)` before it
        # extends CMAKE_MODULE_PATH, so it relies solely on Eigen3Config.cmake
        # being discovered in config mode. Under Spack this is unreliable and
        # fails with "Eigen3 library not found". The CMake logic is guarded by
        # `if (NOT EIGEN3_INCLUDE_DIR)`, so setting EIGEN3_INCLUDE_DIR directly
        # skips the fragile find_package call and points the build straight at
        # the headers (Spack installs Eigen headers under <prefix>/include/eigen3).
        args.append(self.define("EIGEN3_INCLUDE_DIR", spec["eigen"].prefix.include.eigen3))

        iqflags = []

        if spec.satisfies("+lsd2"):
            args.append("-DUSE_LSD2=ON")

        if spec.satisfies("+openmp"):
            iqflags.append("omp")

        if spec.satisfies("+mpi"):
            iqflags.append("mpi")

        if not iqflags:
            iqflags.append("single")

        args.append("-DIQTREE_FLAGS=" + ",".join(iqflags))

        return args
