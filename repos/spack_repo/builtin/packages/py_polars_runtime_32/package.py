# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyPolarsRuntime32(PythonPackage):
    """Compiled Rust runtime of Polars, split out of py-polars from 1.34."""

    homepage = "https://www.pola.rs/"
    pypi = "polars-runtime-32/polars_runtime_32-1.34.0.tar.gz"

    license("MIT")

    version("1.34.0", sha256="ebe6f865128a0d833f53a3f6828360761ad86d1698bceb22bef9fd999500dc1c")

    variant(
        "nightly", default=False, description="Enable nightly SIMD paths. Requires nightly rust"
    )

    depends_on("c", type="build")
    # bundled jemalloc is built with its shipped configure and make
    depends_on("gmake", type="build")

    depends_on("python@3.9:", type=("build", "run"))

    # pyproject.toml
    depends_on("py-maturin@1.3.2:", type="build")

    # rust-toolchain.toml pins nightly-2025-08-29 (1.91.0-nightly); newer rust fails:
    # 1.96 rejects ambiguous glob imports in polars-sql, 1.97 breaks the locked ethnum 1.5.2
    depends_on("rust@1.91:1.92", type="build", when="~nightly")
    # see py-polars for how to build rust@nightly
    depends_on("rust@nightly", type="build", when="+nightly")

    @when("~nightly")
    def setup_build_environment(self, env):
        # https://github.com/pola-rs/polars/issues/22708#issuecomment-2872555300
        env.set("MATURIN_PEP517_ARGS", "--no-default-features --features full")
