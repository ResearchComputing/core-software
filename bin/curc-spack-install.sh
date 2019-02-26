#!/bin/bash

set -e


# See packages.yaml for additional specifications


function main
{
    spack clean

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

    spack install openmpi%gcc@8.2.0
    for compiler in intel@18.0.3 pgi@18.4
    do
        spack install "openmpi%${compiler}" \
              ^/$(gethash hwloc%gcc@8.2.0) \
              ^/$(gethash ucx%gcc@8.2.0) \
              ^/$(gethash slurm%gcc@8.2.0) \
              ^/$(gethash libfabric%gcc@8.2.0)
    done

    for compiler in gcc@8.2.0 intel@18.0.3 pgi@18.4
    do
        spack install libpng%${compiler}
    done

    spack install hdf5%gcc@8.2.0
    for compiler in intel@18.0.3 pgi@18.4
    do
        spack install "hdf5%${compiler}" ^/$(gethash "openmpi%${compiler}")
    done
    spack install hdf5%intel@18.0.3 ^/$(gethash intel-parallel-studio%gcc@4.8.5)

    spack install netcdf%gcc@8.2.0
    for compiler in intel@18.0.3 pgi@18.4
    do
        spack install netcdf%${compiler} ^/$(gethash hdf5%${compiler} ^openmpi%${compiler}) ^/$(gethash m4%gcc@8.2.0)
    done
    spack install netcdf%intel@18.0.3 ^/$(gethash hdf5%intel@18.0.3 ^intel-parallel-studio%gcc@4.8.5) ^/$(gethash m4%gcc@8.2.0)

    spack install parallel-netcdf%gcc@8.2.0
    for compiler in intel@18.0.3 pgi@18.4
    do
        spack install parallel-netcdf%${compiler} ^/$(gethash openmpi%${compiler}) ^/$(gethash m4%gcc@8.2.0)
    done
    spack install parallel-netcdf%intel@18.0.3 ^/$(gethash intel-parallel-studio%gcc@4.8.5) ^/$(gethash m4%gcc@8.2.0)

    # libgeotiff

    spack module lmod refresh -y
}


function gethash
{
    basename $(spack location -i "$@") | grep -o '[^-]*$' | head -n 1
}


main "$@"
