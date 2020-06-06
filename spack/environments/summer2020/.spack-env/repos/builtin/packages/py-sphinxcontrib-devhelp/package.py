# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PySphinxcontribDevhelp(PythonPackage):
    """sphinxcontrib-devhelp is a sphinx extension which outputs
    Devhelp document."""

    homepage = "http://sphinx-doc.org/"
    url      = "https://pypi.io/packages/source/s/sphinxcontrib-devhelp/sphinxcontrib-devhelp-1.0.1.tar.gz"

    version('1.0.1', sha256='6c64b077937330a9128a4da74586e8c2130262f014689b4b89e2d08ee7294a34')

    depends_on('python@3.5:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')

    def test(self):
        # Requires sphinx, creating a circular dependency
        pass
