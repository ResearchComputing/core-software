# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PySphinxcontribSerializinghtml(PythonPackage):
    """sphinxcontrib-serializinghtml is a sphinx extension which outputs
    "serialized" HTML files (json and pickle)."""

    homepage = "http://sphinx-doc.org/"
    url      = "https://pypi.io/packages/source/s/sphinxcontrib-serializinghtml/sphinxcontrib-serializinghtml-1.1.3.tar.gz"

    version('1.1.3', sha256='c0efb33f8052c04fd7a26c0a07f1678e8512e0faec19f4aa8f2473a8b81d5227')

    depends_on('python@3.5:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')

    def test(self):
        # Requires sphinx, creating a circular dependency
        pass
