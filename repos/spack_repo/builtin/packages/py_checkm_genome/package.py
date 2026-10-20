# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyCheckmGenome(PythonPackage):
    """Assess the quality of microbial genomes recovered from isolates, single
    cells, and metagenomes"""

    homepage = "https://ecogenomics.github.io/CheckM"
    pypi = "checkm-genome/checkm_genome-1.2.5.tar.gz"

    license("GPL-3.0-or-later")

    version("1.2.5", sha256="b91333fc6e1d86244895def447cdcffa918177e6cc839501ba2586052edaa5cf")
    # sdist was named checkm-genome-* before 1.2.3
    version(
        "1.2.1",
        sha256="33907aa7bbf029f8345e33df80d5c89b7a719041f55ece4f7470cd061c8eff76",
        url="https://files.pythonhosted.org/packages/source/c/checkm-genome/checkm-genome-1.2.1.tar.gz",
    )

    # pip silently replaces distutils with setuptools
    depends_on("python@3:", type=("build", "run"))
    depends_on("py-setuptools", type=("build", "run"))
    depends_on("hmmer@3.1b1:", type=("build", "run"))
    depends_on("pplacer", type=("build", "run"))
    depends_on("prodigal@2.6.1:", type=("build", "run"))
    depends_on("py-numpy@1.21.3:", type=("build", "run"))
    depends_on("py-scipy@1.7.3:", type=("build", "run"))
    depends_on("py-matplotlib@3.5.1:", type=("build", "run"))
    depends_on("py-pysam@0.19.0:", type=("build", "run"))
    depends_on("py-dendropy@4.5.2:", type=("build", "run"))

    # writes np.float64 reprs into bin_stats, which its own qa can't literal_eval under numpy 2
    depends_on("py-numpy@:1", type=("build", "run"), when="@:1.2.2")
    # imports pkg_resources unconditionally; setuptools 82 dropped it
    depends_on("py-setuptools@:81", type=("build", "run"), when="@:1.2.4")
