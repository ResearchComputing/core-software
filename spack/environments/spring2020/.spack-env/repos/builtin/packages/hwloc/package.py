# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import sys


class Hwloc(AutotoolsPackage):
    """The Hardware Locality (hwloc) software project.

    The Portable Hardware Locality (hwloc) software package
    provides a portable abstraction (across OS, versions,
    architectures, ...) of the hierarchical topology of modern
    architectures, including NUMA memory nodes, sockets, shared
    caches, cores and simultaneous multithreading. It also gathers
    various system attributes such as cache and memory information
    as well as the locality of I/O devices such as network
    interfaces, InfiniBand HCAs or GPUs. It primarily aims at
    helping applications with gathering information about modern
    computing hardware so as to exploit it accordingly and
    efficiently.
    """

    homepage = "http://www.open-mpi.org/projects/hwloc/"
    url      = "https://download.open-mpi.org/release/hwloc/v2.0/hwloc-2.0.2.tar.gz"
    list_url = "http://www.open-mpi.org/software/hwloc/"
    list_depth = 2
    git = 'https://github.com/open-mpi/hwloc.git'

    version('master', branch='master')
    version('2.1.0',  sha256='1fb8cc1438de548e16ec3bb9e4b2abb9f7ce5656f71c0906583819fcfa8c2031')
    version('2.0.2',  sha256='27dcfe42e3fb3422b72ce48b48bf601c0a3e46e850ee72d9bdd17b5863b6e42c')
    version('2.0.1',  sha256='f1156df22fc2365a31a3dc5f752c53aad49e34a5e22d75ed231cd97eaa437f9d')
    version('2.0.0',  sha256='a0d425a0fc7c7e3f2c92a272ffaffbd913005556b4443e1887d2e1718d902887')
    version('1.11.11', sha256='74329da3be1b25de8e98a712adb28b14e561889244bf3a8138afe91ab18e0b3a')
    version('1.11.10', sha256='0a2530b739d9ebf60c4c1e86adb5451a20d9e78f7798cf78d0147cc6df328aac')
    version('1.11.9', sha256='85b978995b67db0b1a12dd1a73b09ef3d39f8e3cb09f8b9c60cf04633acce46c')
    version('1.11.8', sha256='8af89b1164a330e36d18210360ea9bb305e19f9773d1c882855d261a13054ea8')
    version('1.11.7', sha256='ac16bed9cdd3c63bca1fe1ac3de522a1376b1487c4fc85b7b19592e28fd98e26')
    version('1.11.6', sha256='67963f15197e6b551539c4ed95a4f8882be9a16cf336300902004361cf89bdee')
    version('1.11.5', sha256='da2c780fce9b5440a1a7d1caf78f637feff9181a9d1ca090278cae4bea71b3df')
    version('1.11.4', sha256='1b6a58049c31ce36aff162cf4332998fd468486bd08fdfe0249a47437311512d')
    version('1.11.3', sha256='03a1cc63f23fed7e17e4d4369a75dc77d5c145111b8578b70e0964a12712dea0')
    version('1.11.2', sha256='d11f091ed54c56c325ffca1083113a405fcd8a25d5888af64f5cd6cf587b7b0a')
    version('1.11.1', sha256='b41f877d79b6026640943d57ef25311299378450f2995d507a5e633da711be61')
    version('1.9',    sha256='9fb572daef35a1c8608d1a6232a4a9f56846bab2854c50562dfb9a7be294f4e8')

    variant('nvml', default=False, description="Support NVML device discovery")
    variant('gl', default=False, description="Support GL device discovery")
    variant('cuda', default=False, description="Support CUDA devices")
    variant('libxml2', default=True, description="Build with libxml2")
    variant('pci', default=(sys.platform != 'darwin'),
            description="Support analyzing devices on PCI bus")
    variant('shared', default=True, description="Build shared libraries")
    variant(
        'cairo',
        default=False,
        description='Enable the Cairo back-end of hwloc\'s lstopo command'
    )

    depends_on('pkgconfig', type='build')
    depends_on('m4', type='build', when='@master')
    depends_on('autoconf', type='build', when='@master')
    depends_on('automake', type='build', when='@master')
    depends_on('libtool', type='build', when='@master')
    depends_on('cuda', when='+nvml')
    depends_on('cuda', when='+cuda')
    depends_on('gl', when='+gl')
    depends_on('libpciaccess', when='+pci')
    depends_on('libxml2', when='+libxml2')
    depends_on('cairo', when='+cairo')
    depends_on('numactl', when='@:1.11.11 platform=linux')

    def url_for_version(self, version):
        return "http://www.open-mpi.org/software/hwloc/v%s/downloads/hwloc-%s.tar.gz" % (version.up_to(2), version)

    def configure_args(self):
        args = [
            # Disable OpenCL, since hwloc might pick up an OpenCL
            # library at build time that is then not found at run time
            # (Alternatively, we could require OpenCL as dependency.)
            "--disable-opencl",
        ]
        if '@2.0.0:' in self.spec:
            args.append('--enable-netloc')

        args.extend(self.enable_or_disable('cairo'))
        args.extend(self.enable_or_disable('nvml'))
        args.extend(self.enable_or_disable('gl'))
        args.extend(self.enable_or_disable('cuda'))
        args.extend(self.enable_or_disable('libxml2'))
        args.extend(self.enable_or_disable('pci'))
        args.extend(self.enable_or_disable('shared'))

        return args
