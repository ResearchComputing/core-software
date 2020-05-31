# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libffi(AutotoolsPackage, SourcewarePackage):
    """The libffi library provides a portable, high level programming
    interface to various calling conventions. This allows a programmer
    to call any function specified by a call interface description at
    run time."""
    homepage = "https://sourceware.org/libffi/"
    sourceware_mirror_path = "libffi/libffi-3.2.1.tar.gz"

    version('3.3',   sha256='72fba7922703ddfa7a028d513ac15a85c8d54c8d67f55fa5a4802885dc652056')
    version('3.2.1', sha256='d06ebb8e1d9a22d19e38d63fdb83954253f39bedc5d46232a05645685722ca37')

    @property
    def headers(self):
        # The headers are probably in self.prefix.lib but we search everywhere
        return find_headers('ffi', self.prefix, recursive=True)
