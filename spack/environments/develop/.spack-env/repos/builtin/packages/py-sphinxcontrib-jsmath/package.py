# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PySphinxcontribJsmath(PythonPackage):
    """A sphinx extension which renders display math in HTML via JavaScript."""

    homepage = "http://sphinx-doc.org/"
    url      = "https://pypi.io/packages/source/s/sphinxcontrib-jsmath/sphinxcontrib-jsmath-1.0.1.tar.gz"

    version('1.0.1', sha256='a9925e4a4587247ed2191a22df5f6970656cb8ca2bd6284309578f2153e0c4b8')

    depends_on('python@3.5:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')

    def test(self):
        # Requires sphinx, creating a circular dependency
        pass
