#!/bin/bash

set -e


# See packages.yaml for additional specifications


function main
{
    spack clean

    # core packages

    CORE_COMPILER='gcc@4.8.5'
    CORE_PACKAGES=(
        lmod
        gcc@8.2.0
        intel@18.0.3
        intel-parallel-studio@cluster.2018.3
        pgi@18.4
    )

    for package in "${CORE_PACKAGES[@]}"
    do
        spack install "${package}" "%${CORE_COMPILER}"
    done

    # simple packages

    spack install libpng%gcc@8.2.0
    spack install libpng%intel@18.0.3

    spack install libgeotiff%gcc@8.2.0
    spack install libgeotiff%intel@18.0.3

    # openmpi

    spack install openmpi%gcc@8.2.0
    for compiler in intel@18.0.3 pgi@18.4
    do
        spack install "openmpi%${compiler}" \
              ^/$(gethash hwloc%gcc@8.2.0) \
              ^/$(gethash ucx%gcc@8.2.0) \
              ^/$(gethash slurm%gcc@8.2.0) \
              ^/$(gethash libfabric%gcc@8.2.0)
    done

    # mpi-dependent packages

    spack install hdf5%gcc@8.2.0
    spack install hdf5%intel@18.0.3 ^/$(gethash openmpi%intel@18.0.3)
    spack install hdf5%intel@18.0.3 ^/$(gethash intel-parallel-studio%gcc@4.8.5)
    spack install hdf5%pgi@18.4 ^/$(gethash openmpi%pgi@18.4)

    spack install netcdf%gcc@8.2.0
    spack install netcdf-fortran%gcc@8.2.0 ^/$(gethash netcdf%gcc@8.2.0)
    spack install netcdf%intel@18.0.3 ^/$(gethash hdf5%intel@18.0.3 ^openmpi%intel@18.0.3) ^/$(gethash m4%gcc@8.2.0)
    spack install netcdf-fortran%intel@18.0.3 ^/$(gethash netcdf%intel@18.0.3 ^openmpi)
    spack install netcdf%intel@18.0.3 ^/$(gethash hdf5%intel@18.0.3 ^intel-parallel-studio%gcc@4.8.5) ^/$(gethash m4%gcc@8.2.0)
    spack install netcdf-fortran%intel@18.0.3 ^/$(gethash netcdf%intel@18.0.3 ^intel-parallel-studio)
    spack install netcdf%pgi@18.4 ^/$(gethash hdf5%pgi@18.4 ^openmpi%pgi@18.4) ^/$(gethash m4%gcc@8.2.0)
    spack install netcdf-fortran%pgi@18.4 ^/$(gethash netcdf%pgi@18.4)

    spack install parallel-netcdf%gcc@8.2.0
    spack install parallel-netcdf%intel@18.0.3 ^/$(gethash openmpi%intel@18.0.3) ^/$(gethash m4%gcc@8.2.0)
    spack install parallel-netcdf%intel@18.0.3 ^/$(gethash intel-parallel-studio%gcc@4.8.5) ^/$(gethash m4%gcc@8.2.0)
    spack install parallel-netcdf%pgi@18.4 ^/$(gethash openmpi%pgi@18.4) ^/$(gethash m4%gcc@8.2.0)

    spack module lmod refresh -y
}


function gethash
{
    basename $(spack location -i "$@") | grep -o '[^-]*$' | head -n 1
}


main "$@"
