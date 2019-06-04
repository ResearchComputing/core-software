#!/bin/bash

set -e


# See packages.yaml for additional specifications

# starting over
# spack uninstall --all --dependents $(spack find | grep -o '^[a-z][^@]*' | sort -u | grep -vE '^(intel-mkl|intel-mpi|intel|intel-parallel-studio|gcc|pgi)$')


function main
{
    install_core

    install_simple

    install_mkl

    install_impi
    install_openmpi

    # mpi-dependent packages
    install_hdf5
    install_netcdf
    install_parallel_netcdf

    spack module lmod refresh -y
}


function install_core
{
    local core_compiler='gcc@4.8.5'
    local core_packages=(
        lmod@7.8
        gcc@8.2.0
        intel-parallel-studio@cluster.2018.3
        intel@18.0.3
        pgi@18.4
        git@2.19.1
        singularity@2.6.0
        cmake@3.12.3
        mercurial@4.4.1
        cuda@10.0.130
        parallel@20170322
        perl@5.26.2
        gdb@8.2
        libtool@2.4.6
        autoconf@2.69
        automake@1.16.1
    )

    for package in "${core_packages[@]}"
    do
        spack install "${package}" "%${core_compiler}"
    done
}


function install_simple
{
    spack install m4%gcc@8.2.0

    spack install libpng%gcc@8.2.0
    spack install libpng%intel@18.0.3

    spack install libgeotiff%gcc@8.2.0
    spack install libgeotiff%intel@18.0.3
}


function install_mkl
{
    for compiler in gcc@8.2.0 intel@18.0.3 pgi@18.4
    do
        spack install "intel-mkl@2018.3.222 %${compiler}"
    done
}


function install_impi
{
    for compiler in gcc@8.2.0 intel@18.0.3 pgi@18.4
    do
        spack install "intel-mpi@2018.3.222 %${compiler}"
    done
}


function install_openmpi
{
    spack install openmpi%gcc@8.2.0
    for compiler in intel@18.0.3 pgi@18.4
    do
        spack install "openmpi%${compiler}" \
              ^/$(gethash hwloc%gcc@8.2.0) \
              ^/$(gethash ucx%gcc@8.2.0) \
              ^/$(gethash slurm%gcc@8.2.0) \
              ^/$(gethash libfabric%gcc@8.2.0)
    done
}


function install_hdf5
{
    spack install hdf5%gcc@8.2.0
    spack install hdf5%intel@18.0.3 ^/$(gethash openmpi %intel)
    spack install hdf5%intel@18.0.3 ^/$(gethash intel-mpi %intel)
    spack install hdf5%pgi@18.4 ^/$(gethash openmpi %pgi)
}


function install_netcdf
{
    spack install netcdf%gcc@8.2.0 ^/$(gethash hdf5%gcc ^openmpi) ^/$(gethash m4%gcc@8.2.0)
    spack install netcdf-fortran%gcc@8.2.0 ^/$(gethash netcdf%gcc)

    spack install netcdf%intel@18.0.3 ^/$(gethash hdf5%intel ^openmpi) ^/$(gethash m4%gcc@8.2.0)
    spack install netcdf-fortran%intel@18.0.3 ^/$(gethash netcdf%intel ^openmpi)

    spack install netcdf%intel@18.0.3 ^/$(gethash hdf5%intel ^intel-mpi) ^/$(gethash m4%gcc@8.2.0)
    spack install netcdf-fortran%intel@18.0.3 ^/$(gethash netcdf%intel ^intel-mpi)

    spack install netcdf%pgi@18.4 ^/$(gethash hdf5%pgi@18.4 ^openmpi%pgi@18.4) ^/$(gethash m4%gcc@8.2.0)
    spack install netcdf-fortran%pgi@18.4 ^/$(gethash netcdf%pgi)
}


function install_parallel_netcdf
{
    spack install parallel-netcdf%gcc@8.2.0 ^/$(gethash openmpi%gcc) ^/$(gethash m4%gcc@8.2.0)
    spack install parallel-netcdf%intel@18.0.3 ^/$(gethash openmpi%intel) ^/$(gethash m4%gcc@8.2.0)
    spack install parallel-netcdf%intel@18.0.3 ^/$(gethash intel-mpi%intel) ^/$(gethash m4%gcc@8.2.0)
    spack install parallel-netcdf%pgi@18.4 ^/$(gethash openmpi%pgi) ^/$(gethash m4%gcc@8.2.0)
}


function gethash
{
    basename $(spack location -i "$@") | grep -o '[^-]*$' | head -n 1
}


main "$@"
