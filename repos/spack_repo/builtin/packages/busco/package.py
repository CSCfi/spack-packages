# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class Busco(PythonPackage):
    """Assesses genome assembly and annotation completeness with Benchmarking
    Universal Single-Copy Orthologs"""

    homepage = "https://busco.ezlab.org/"
    url = "https://gitlab.com/api/v4/projects/ezlab%2Fbusco/repository/archive.tar.gz?sha=2.0.1"
    git = "https://gitlab.com/ezlab/busco.git"
    maintainers("snehring")

    license("MIT")

    version("6.1.0", sha256="5adbbcfc048210f390faebd7cd4d33057531b9ee5608c46b18b94bd84d61bfdf")
    version("6.0.0", sha256="e0141e9a9fbec6916c0e76835c6227097f3c50c094deb555225a3f0ab98f709a")
    version("5.8.3", sha256="c995c315b5e923065fb7a9c46ceb6c5e291a96884dba4b013cb0ba7dda980fdd")
    version("5.8.2", sha256="b89b6db4ed3d3ad7c44d3123e3e32ee9413889e557bb44fe55fa34ae6ae726d2")
    version("5.8.1", sha256="b0132ac167fb8c9378c1f424bf3e13901932264ba7ef1407799672be7c694e90")
    version("5.8.0", sha256="83b5f75f122507cfff7ceffd01ab28eb0074db4aecae3d6affd10495335df437")
    version("5.7.1", sha256="0e5569f753ccd1a4e1d8e9ccc062432323fbeffd349a74153a4aa3e7210a4cf8")
    version("5.7.0", sha256="1ca3da0604849e3386c7ed14660be045aab95fafb9b071b15d74063fc9e7eb7b")
    version("5.4.3", sha256="8b92dcc32691f7c1629aaaa7bd54f96073273ba7de5a3a8586fe552c51a9d36a")
    version("4.1.3", sha256="08ded26aeb4f6aef791cd88524c3c00792a054c7672ea05219f468d495e7b072")

    # TODO: check the installation procedure for version 3.0.2
    # and uncomment the following line
    # version('3.0.2', sha256='dbea093315b766b0f7c4fe3cafbbdf51ade79ec84bde04f1f437b48333200f34')

    # There is no tag for version 3.0.1
    version("3.0.1", commit="078252e00399550d7b0e8941cd4d986c8e868a83")
    version("2.0.1", sha256="bd72a79b880370e9b61b8c722e171818c7c85d46cc1e2f80595df2738a7e220c")

    # https://busco.ezlab.org/busco_userguide.html#manual-installation
    depends_on("python@3.3:", when="@4:", type=("build", "run"))
    # pip silently replaces distutils with setuptools
    depends_on("py-setuptools", when="@3:", type="build")
    depends_on("blast-plus")
    depends_on("hmmer")
    depends_on("augustus")
    depends_on("py-biopython", when="@4.1.3:", type=("build", "run"))
    depends_on("py-pandas", when="@5:", type="run")
    depends_on("bbmap", when="@5:", type="run")
    depends_on("prodigal", when="@5:", type="run")
    depends_on("metaeuk", when="@5:", type="run")
    depends_on("sepp", when="@5:", type="run")
    # busco 6 replaced the external R plotting script with a built-in
    # matplotlib-based plotter
    depends_on("py-matplotlib", when="@6:", type="run")
    depends_on("py-numpy", when="@6:", type="run")

    def install(self, spec, prefix):
        if self.spec.satisfies("@4.1.3:"):
            install_tree("bin", prefix.bin)
            install_tree("config", prefix.config)
            super().install(spec, prefix)
        if self.spec.satisfies("@3.0.1"):
            with working_dir("scripts"):
                mkdirp(prefix.bin)
                install("generate_plot.py", prefix.bin)
                install("run_BUSCO.py", prefix.bin)
            install_tree("config", prefix.config)
            super().install(spec, prefix)
        if self.spec.satisfies("@2.0.1"):
            mkdirp(prefix.bin)
            install("BUSCO.py", prefix.bin)
            install("BUSCO_plot.py", prefix.bin)
