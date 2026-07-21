# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyPybigwig(PythonPackage):
    """A package for accessing bigWig files using libBigWig."""

    homepage = "https://github.com/deeptools/pyBigWig"
    git = "https://github.com/deeptools/pyBigWig.git"

    version("0.3.25", tag="0.3.25", commit="9c7d9d90331d821a3a4a48214e4bf9f3be6e5274")
    version("0.3.22", tag="0.3.22", commit="fb7c0cf889407f55a6c31eeb6fd5f6a0744ee70c")
    
    license("MIT")

    variant("numpy", default=True, description="Enable support for numpy integers and vectors")

    patch("python3_curl.patch", when="@:0.3.12 ^python@3:")

    depends_on("c", type="build")  # generated

    depends_on("curl", type=("build", "link", "run"))
    depends_on("py-setuptools", type="build")

    depends_on("py-numpy", type=("build", "run"), when="+numpy")
