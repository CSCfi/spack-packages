# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.generic import Package

from spack.package import *


class LpSolve(Package):
    """lp_solve is a Mixed Integer Linear Programming (MILP) solver."""

    homepage = "https://sourceforge.net/projects/lpsolve/"
    url = "https://sourceforge.net/projects/lpsolve/files/lpsolve/5.5.2.11/lp_solve_5.5.2.11_source.tar.gz"

    version("5.5.2.11", sha256="6d4abff5cc6aaa933ae8e6c17a226df0fc0b671c438f69715d41d09fe81f902f")

    depends_on("c", type="build")  # generated

    def patch(self):
        # GCC >= 14 turns C's implicit `int` into a hard error, so the two
        # tiny probe programs that the `ccc` build scripts compile and run
        # (platform and isnan detection) fail to build. $PLATFORM then
        # expands to the empty string, the build output lands in bin/
        # instead of bin/ux64, and the install fails with
        #   OSError: No such file or directory: 'bin/ux64'
        # Fixed upstream in 5.5.2.13; these edits are no-ops there.
        for ccc in ("lpsolve55/ccc", "lp_solve/ccc"):
            filter_file("'main(){", "'int main(){", ccc, string=True)
            # honor the compiler provided by Spack instead of bare `cc`
            filter_file("^c=cc$", 'c="${CC:-cc}"', ccc)

    def install(self, spec, prefix):
        with working_dir("lpsolve55"):
            mkdir(prefix.lib)
            sh = which("sh", required=True)
            sh("-x", "ccc")
            install_tree("bin/ux64", prefix.lib)

        with working_dir("lp_solve"):
            mkdir(prefix.bin)
            sh = which("sh", required=True)
            sh("-x", "ccc")
            install_tree("bin/ux64", prefix.bin)

        mkdirp(prefix.include.lpsolve)
        headers = find(".", "*.h", recursive=False)
        for header in headers:
            install(header, prefix.include.lpsolve)
