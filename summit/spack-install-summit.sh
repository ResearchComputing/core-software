#!/bin/bash

set -e
set -v


# See packages.yaml for additional specifications


spack clean


#
# core

CORE_COMPILER='gcc@4.8.5'
CORE_PACKAGES=(
    lmod
)
for package in "${CORE_PACKAGES[@]}"
do
    spack install "${package}" "%${CORE_COMPILER}"
done


#
# compilers

COMPILERS=(
    gcc@8.2.0
    pgi@18.4
    intel@18.0.3
    intel-parallel-studio@cluster.2018.3
)

for compiler in "${COMPILERS[@]}"
do
    spack install "${compiler}" "%${CORE_COMPILER}"
done


#
# mpi

GCC_OPENMPI_DEPS=(
    ^hwloc%gcc@8.2.0
    ^libfabric%gcc@8.2.0
    ^numactl%gcc@8.2.0
    ^pkgconf@1.4.2%gcc@8.2.0
    ^ucx%gcc@8.2.0
    ^zlib%gcc@8.2.0
)

LOCAL_OPENMPI_DEPS=(
    ^slurm@17.11.7
)

spack install openmpi %gcc@8.2.0 "${LOCAL_OPENMPI_DEPS[@]}"
spack install openmpi %pgi@18.4 "${LOCAL_OPENMPI_DEPS[@]}" "${GCC_OPENMPI_DEPS[@]}"
spack install openmpi %intel@18.0.3 "${LOCAL_OPENMPI_DEPS[@]}" "${GCC_OPENMPI_DEPS[@]}"


#
# libraries and applications

spack install parallel-netcdf %gcc@8.2.0 "${LOCAL_OPENMPI_DEPS[@]}"
spack install parallel-netcdf %intel@18.0.3 "${LOCAL_OPENMPI_DEPS[@]}" "${GCC_OPENMPI_DEPS[@]}" ^m4%gcc@8.2.0
spack install parallel-netcdf %pgi@18.4 "${LOCAL_OPENMPI_DEPS[@]}" "${GCC_OPENMPI_DEPS[@]}" ^m4%gcc@8.2.0

spack install hdf5 %gcc@8.2.0 "${LOCAL_OPENMPI_DEPS[@]}"
spack install hdf5 %intel@18.0.3 "${LOCAL_OPENMPI_DEPS[@]}" "${GCC_OPENMPI_DEPS[@]}"
spack install hdf5 %pgi@18.4 "${LOCAL_OPENMPI_DEPS[@]}" "${GCC_OPENMPI_DEPS[@]}"

spack install netcdf %gcc@8.2.0 "${LOCAL_OPENMPI_DEPS[@]}"
spack install netcdf %intel@18.0.3 "${LOCAL_OPENMPI_DEPS[@]}" "${GCC_OPENMPI_DEPS[@]}" ^m4%gcc@8.2.0
spack install netcdf %pgi@18.4 "${LOCAL_OPENMPI_DEPS[@]}" "${GCC_OPENMPI_DEPS[@]}" ^m4%gcc@8.2.0


#
# lmod sync

spack module lmod refresh -y
