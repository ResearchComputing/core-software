# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

import os.path


class Glib(Package):
    """GLib provides the core application building blocks for
    libraries and applications written in C.

    The GLib package contains a low-level libraries useful for
    providing data structure handling for C, portability wrappers
    and interfaces for such runtime functionality as an event loop,
    threads, dynamic loading and an object system.
    """

    homepage = "https://developer.gnome.org/glib/"
    url      = "https://ftp.gnome.org/pub/gnome/sources/glib/2.53/glib-2.53.1.tar.xz"

    version('2.64.3', sha256='fe9cbc97925d14c804935f067a3ad77ef55c0bbe9befe68962318f5a767ceb22')
    version('2.64.2', sha256='9a2f21ed8f13b9303399de13a0252b7cbcede593d26971378ec6cb90e87f2277')
    version('2.64.1', sha256='17967603bcb44b6dbaac47988d80c29a3d28519210b28157c2bd10997595bbc7')
    version('2.62.6', sha256='104fa26fbefae8024ff898330c671ec23ad075c1c0bce45c325c6d5657d58b9c')
    version('2.60.7', sha256='8b12c0af569afd3b71200556ad751bad4cf4bf7bc4b5f880638459a42ca86310')
    version('2.58.3', sha256='8f43c31767e88a25da72b52a40f3301fefc49a665b56dc10ee7cc9565cbe7481')
    version('2.56.4', sha256='27f703d125efb07f8a743666b580df0b4095c59fc8750e8890132c91d437504c')
    version('2.56.3', sha256='a9a4c5b4c81b6c75bc140bdf5e32120ef3ce841b7413214ecf5f987acec74cb2')
    version('2.56.2', sha256='d64abd16813501c956c4e123ae79f47f1b58de573df9fdd3b0795f1e2c1aa789')
    version('2.56.1', sha256='40ef3f44f2c651c7a31aedee44259809b6f03d3d20be44545cd7d177221c0b8d')
    version('2.56.0', sha256='ecef6e17e97b8d9150d0e8a4b3edee1ac37331213b8a2a87a083deea408a0fc7')
    version('2.55.1', sha256='0cbb3d31c9d181bbcc97cba3d9dbe3250f75e2da25e5f7c8bf5a993fe54baf6a')
    version('2.53.1', sha256='c8740f1d1a138086eede889b596a511fddda180646ab2f1d98aed4fdb6be7f72')
    version('2.49.7', sha256='0fd13406ca31d6f654c3be620e0adaaa4f9fb788e164e265e33edf4b21e64ef6')
    version('2.49.4', sha256='9e914f9d7ebb88f99f234a7633368a7c1133ea21b5cac9db2a33bc25f7a0e0d1')
    version('2.48.1', sha256='74411bff489cb2a3527bac743a51018841a56a4d896cc1e0d0d54f8166a14612')
    version('2.42.1', sha256='8f3f0865280e45b8ce840e176ef83bcfd511148918cc8d39df2ee89b67dcf89a')

    variant('libmount', default=False, description='Build with libmount support')
    variant(
        'tracing', values=any_combination_of('dtrace', 'systemtap'),
        description='Enable tracing support'
    )

    depends_on('meson@0.49.2:', when='@2.61.2:', type='build')
    depends_on('meson@0.48.0:', when='@2.58.0:', type='build')
    depends_on('ninja', when='@2.58.0:', type='build')

    depends_on('pkgconfig', type='build')
    depends_on('libffi')
    depends_on('zlib')
    depends_on('gettext')
    depends_on('perl', type=('build', 'run'))
    depends_on('python', type=('build', 'run'), when='@2.53.4:')
    depends_on('pcre+utf', when='@2.48:')
    depends_on('util-linux', when='+libmount')
    depends_on('iconv')

    # The following patch is needed for gcc-6.1
    patch('g_date_strftime.patch', when='@2.42.1')
    # Clang doesn't seem to acknowledge the pragma lines to disable the -Werror
    # around a legitimate usage.
    patch('no-Werror=format-security.patch', when='@:2.57.99')
    # Patch to prevent compiler errors in kernels older than 2.6.35
    patch('old-kernels.patch', when='@2.56.0:2.56.1 os=rhel6')
    patch('old-kernels.patch', when='@2.56.0:2.56.1 os=centos6')
    patch('old-kernels.patch', when='@2.56.0:2.56.1 os=scientific6')

    # glib prefers the libc version of gettext, which breaks the build if the
    # external version is also found.
    patch('meson-gettext.patch', when='@2.58.0:')

    def url_for_version(self, version):
        """Handle glib's version-based custom URLs."""
        url = 'http://ftp.gnome.org/pub/gnome/sources/glib'
        return url + '/%s/glib-%s.tar.xz' % (version.up_to(2), version)

    def meson_args(self):
        args = ['-Dgettext=external']
        if self.spec.satisfies('@2.63.5:'):
            if '+libmount' in self.spec:
                args.append('-Dlibmount=enabled')
            else:
                args.append('-Dlibmount=disabled')
        else:
            if '+libmount' in self.spec:
                args.append('-Dlibmount=true')
            else:
                args.append('-Dlibmount=false')
        if 'libc' in self.spec:
            args.append('-Diconv=libc')
        else:
            if self.spec.satisfies('@2.61.0:'):
                args.append('-Diconv=external')
            else:
                args.append('-Diconv=gnu')
        if 'tracing=dtrace' in self.spec:
            args.append('-Ddtrace=true')
        else:
            args.append('-Ddtrace=false')
        if 'tracing=systemtap' in self.spec:
            args.append('-Dsystemtap=true')
        else:
            args.append('-Dsystemtap=false')
        if self.spec.satisfies('@2.59.0:'):
            args.append('-Dselinux=disabled')
        else:
            args.append('-Dselinux=false')
        args.append('-Dgtk_doc=false')
        return args

    def install(self, spec, prefix):
        with working_dir('spack-build', create=True):
            # We cannot simply do
            #   meson('..', *std_meson_args, *self.meson_args())
            # because that is not Python 2 compatible. Instead, collect
            # arguments into a temporary buffer first.
            args = []
            args.extend(std_meson_args)
            args.extend(self.meson_args())
            meson('..', *args)
            ninja('-v')
            if self.run_tests:
                ninja('test')
            ninja('install')

    def configure_args(self):
        args = []
        if '+libmount' in self.spec:
            args.append('--enable-libmount')
        else:
            args.append('--disable-libmount')
        if self.spec.satisfies('@2.53.4:'):
            args.append('--with-python={0}'.format(
                os.path.basename(self.spec['python'].command.path))
            )
        if 'libc' in self.spec:
            args.append('--with-libiconv=maybe')
        else:
            args.append('--with-libiconv=gnu')
        if 'tracing=dtrace' in self.spec or 'tracing=systemtap' in self.spec:
            args.append('--enable-tracing')
        else:
            args.append('--disable-tracing')
        # SELinux is not available in Spack, so glib should not use it.
        args.append('--disable-selinux')
        # glib should not use the globally installed gtk-doc. Otherwise,
        # gtk-doc can fail with Python errors such as "ImportError: No module
        # named site". This is due to the fact that Spack sets PYTHONHOME,
        # which can confuse the global Python installation used by gtk-doc.
        args.append('--disable-gtk-doc-html')
        # glib uses gtk-doc even though it should be disabled if it can find
        # its binaries. Override the checks to use the true binary.
        true = which('true')
        args.append('GTKDOC_CHECK={0}'.format(true))
        args.append('GTKDOC_CHECK_PATH={0}'.format(true))
        args.append('GTKDOC_MKPDF={0}'.format(true))
        args.append('GTKDOC_REBASE={0}'.format(true))
        return args

    def setup_build_environment(self, env):
        if self.spec.satisfies('platform=darwin'):
            # https://github.com/pybind/pybind11/issues/595
            env.set('STRIP', 'strip -x')

    @when('@:2.57.99')
    def install(self, spec, prefix):
        configure('--prefix={0}'.format(prefix), *self.configure_args())
        make()
        if self.run_tests:
            make('check')
        make('install')
        if self.run_tests:
            make('installcheck')

    @property
    def dtrace_copy_path(self):
        return join_path(self.stage.source_path, 'dtrace-copy')

    @run_before('install')
    def fix_python_path(self):
        if not self.spec.satisfies('@2.53.4:'):
            return

        files = ['gobject/glib-genmarshal.in', 'gobject/glib-mkenums.in']

        filter_file('^#!/usr/bin/env @PYTHON@',
                    '#!/usr/bin/env {0}'.format(
                        os.path.basename(self.spec['python'].command.path)),
                    *files)

    @run_before('install')
    def fix_dtrace_usr_bin_path(self):
        if 'tracing=dtrace' not in self.spec:
            return

        # dtrace may cause glib build to fail because it uses
        # '/usr/bin/python' in the shebang. To work around that
        # we copy the original script into a temporary folder, and
        # change the shebang to '/usr/bin/env python'
        dtrace = which('dtrace').path
        dtrace_copy = join_path(self.dtrace_copy_path, 'dtrace')

        with working_dir(self.dtrace_copy_path, create=True):
            copy(dtrace, dtrace_copy)
            filter_file(
                '^#!/usr/bin/python',
                '#!/usr/bin/env {0}'.format(
                    os.path.basename(self.spec['python'].command.path)),
                dtrace_copy
            )

        # To have our own copy of dtrace in PATH, we need to
        # prepend to PATH the temporary folder where it resides
        env['PATH'] = ':'.join(
            [self.dtrace_copy_path] + env['PATH'].split(':')
        )

    @run_after('install')
    def filter_sbang(self):
        # Revert sbang, so Spack's sbang hook can fix it up (we have to do
        # this after install because otherwise the install target will try
        # to rebuild files as filter_file updates the timestamps)
        if self.spec.satisfies('@2.53.4:'):
            pattern = '^#!/usr/bin/env {0}'.format(
                os.path.basename(self.spec['python'].command.path))
            repl = '#!{0}'.format(self.spec['python'].command.path)
            files = ['glib-genmarshal', 'glib-mkenums']
        else:
            pattern = '^#! /usr/bin/perl'
            repl = '#!{0}'.format(self.spec['perl'].command.path)
            files = ['glib-mkenums']

        files = [join_path(self.prefix.bin, file) for file in files]
        filter_file(pattern, repl, *files, backup=False)

    @run_after('install')
    def gettext_libdir(self):
        # Packages that link to glib were also picking up -lintl from glib's
        # glib-2.0.pc file. However, packages such as py-pygobject were
        # bypassing spack's compiler wrapper for linking and thus not finding
        # the gettext library directory. The patch below explitly adds the
        # appropriate -L path.
        spec = self.spec
        if spec.satisfies('@2:2.99'):
            pattern = 'Libs:'
            repl = 'Libs: -L{0} -Wl,-rpath={0} '.format(
                   spec['gettext'].prefix.lib)
            myfile = join_path(self.prefix.lib.pkgconfig, 'glib-2.0.pc')
            filter_file(pattern, repl, myfile, backup=False)
