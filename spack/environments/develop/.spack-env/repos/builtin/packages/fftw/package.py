# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import os.path

import llnl.util.lang

from spack import *


class Fftw(AutotoolsPackage):
    """FFTW is a C subroutine library for computing the discrete Fourier
       transform (DFT) in one or more dimensions, of arbitrary input
       size, and of both real and complex data (as well as of even/odd
       data, i.e. the discrete cosine/sine transforms or DCT/DST). We
       believe that FFTW, which is free software, should become the FFT
       library of choice for most applications."""

    homepage = "http://www.fftw.org"
    url = "http://www.fftw.org/fftw-3.3.4.tar.gz"
    list_url = "http://www.fftw.org/download.html"

    version('3.3.8', sha256='6113262f6e92c5bd474f2875fa1b01054c4ad5040f6b0da7c03c98821d9ae303')
    version('3.3.7', sha256='3b609b7feba5230e8f6dd8d245ddbefac324c5a6ae4186947670d9ac2cd25573')
    version('3.3.6-pl2', sha256='a5de35c5c824a78a058ca54278c706cdf3d4abba1c56b63531c2cb05f5d57da2')
    version('3.3.5', sha256='8ecfe1b04732ec3f5b7d279fdb8efcad536d555f9d1e8fabd027037d45ea8bcf')
    version('3.3.4', sha256='8f0cde90929bc05587c3368d2f15cd0530a60b8a9912a8e2979a72dbe5af0982')
    version('2.1.5', sha256='f8057fae1c7df8b99116783ef3e94a6a44518d49c72e2e630c24b689c6022630')

    patch('pfft-3.3.5.patch', when="@3.3.5:+pfft_patches", level=0)
    patch('pfft-3.3.4.patch', when="@3.3.4+pfft_patches", level=0)
    patch('pgi-3.3.6-pl2.patch', when="@3.3.6-pl2%pgi", level=0)

    variant(
        'precision', values=any_combination_of(
            'float', 'double', 'long_double', 'quad'
        ).prohibit_empty_set().with_default('float,double'),
        description='Build the selected floating-point precision libraries'
    )
    variant('openmp', default=False, description="Enable OpenMP support.")
    variant('mpi', default=True, description='Activate MPI support')
    variant(
        'pfft_patches', default=False,
        description='Add extra transpose functions for PFFT compatibility')

    depends_on('mpi', when='+mpi')
    depends_on('automake', type='build', when='+pfft_patches')
    depends_on('autoconf', type='build', when='+pfft_patches')
    depends_on('libtool', type='build', when='+pfft_patches')

    # https://github.com/FFTW/fftw3/commit/902d0982522cdf6f0acd60f01f59203824e8e6f3
    conflicts('%gcc@8:8.9999', when="@3.3.7")
    conflicts('precision=long_double', when='@2.1.5',
              msg='Long double precision is not supported in FFTW 2')
    conflicts('precision=quad', when='@2.1.5',
              msg='Quad precision is not supported in FFTW 2')

    provides('fftw-api@2', when='@2.1.5')
    provides('fftw-api@3', when='@3:')

    @property
    def libs(self):

        # Reduce repetitions of entries
        query_parameters = list(llnl.util.lang.dedupe(
            self.spec.last_query.extra_parameters
        ))

        # List of all the suffixes associated with float precisions
        precisions = [
            ('float', 'f'),
            ('double', ''),
            ('long_double', 'l'),
            ('quad', 'q')
        ]

        # Retrieve the correct suffixes, or use double as a default
        suffixes = [v for k, v in precisions if k in query_parameters] or ['']

        # Construct the list of libraries that needs to be found
        libraries = []
        for sfx in suffixes:
            if 'mpi' in query_parameters and '+mpi' in self.spec:
                libraries.append('libfftw3' + sfx + '_mpi')

            if 'openmp' in query_parameters and '+openmp' in self.spec:
                libraries.append('libfftw3' + sfx + '_omp')

            libraries.append('libfftw3' + sfx)

        return find_libraries(libraries, root=self.prefix, recursive=True)

    def patch(self):
        # If fftw/config.h exists in the source tree, it will take precedence
        # over the copy in build dir.  As only the latter has proper config
        # for our build, this is a problem.  See e.g. issue #7372 on github
        if os.path.isfile('fftw/config.h'):
            os.rename('fftw/config.h', 'fftw/config.h.SPACK_RENAMED')

    def autoreconf(self, spec, prefix):
        if '+pfft_patches' in spec:
            autoreconf = which('autoreconf')
            autoreconf('-ifv')

    @property
    def selected_precisions(self):
        """Precisions that have been selected in this build"""
        return self.spec.variants['precision'].value

    def configure(self, spec, prefix):
        # Base options
        options = [
            '--prefix={0}'.format(prefix),
            '--enable-shared',
            '--enable-threads'
        ]
        if not self.compiler.f77 or not self.compiler.fc:
            options.append("--disable-fortran")
        if spec.satisfies('@:2'):
            options.append('--enable-type-prefix')

        # Variants that affect every precision
        if '+openmp' in spec:
            # Note: Apple's Clang does not support OpenMP.
            if spec.satisfies('%clang'):
                ver = str(self.compiler.version)
                if ver.endswith('-apple'):
                    raise InstallError("Apple's clang does not support OpenMP")
            options.append('--enable-openmp')
            if spec.satisfies('@:2'):
                # TODO: libtool strips CFLAGS, so 2.x libxfftw_threads
                #       isn't linked to the openmp library. Patch Makefile?
                options.insert(0, 'CFLAGS=' + self.compiler.openmp_flag)
        if '+mpi' in spec:
            options.append('--enable-mpi')

        # Specific SIMD support.
        # all precisions
        simd_features = ['sse2', 'avx', 'avx2', 'avx512', 'avx-128-fma',
                         'kcvi', 'vsx', 'neon']
        # float only
        float_simd_features = ['altivec', 'sse']

        simd_options = []
        for feature in simd_features:
            msg = '--enable-{0}' if feature in spec.target else '--disable-{0}'
            simd_options.append(msg.format(feature))

        # If no features are found, enable the generic ones
        if not any(f in spec.target for f in
                   simd_features + float_simd_features):
            simd_options += [
                '--enable-generic-simd128',
                '--enable-generic-simd256'
            ]

        simd_options += [
            '--enable-fma' if 'fma' in spec.target else '--disable-fma'
        ]

        # Double is the default precision, for all the others we need
        # to enable the corresponding option.
        enable_precision = {
            'float': ['--enable-float'],
            'double': None,
            'long_double': ['--enable-long-double'],
            'quad': ['--enable-quad-precision']
        }

        # Different precisions must be configured and compiled one at a time
        configure = Executable('../configure')
        for precision in self.selected_precisions:
            opts = (enable_precision[precision] or []) + options[:]

            # SIMD optimizations are available only for float and double
            # starting from FFTW 3
            if precision in ('float', 'double') and spec.satisfies('@3:'):
                opts += simd_options

            # float-only acceleration
            if precision == 'float':
                for feature in float_simd_features:
                    if feature in spec.target:
                        msg = '--enable-{0}'
                    else:
                        msg = '--disable-{0}'
                    opts.append(msg.format(feature))

            with working_dir(precision, create=True):
                configure(*opts)

    def for_each_precision_make(self, *targets):
        for precision in self.selected_precisions:
            with working_dir(precision):
                make(*targets)

    def build(self, spec, prefix):
        self.for_each_precision_make()

    def check(self):
        self.for_each_precision_make('check')

    def install(self, spec, prefix):
        self.for_each_precision_make('install')
