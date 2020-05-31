#!/bin/bash


function main
{
  set -x

  export I_MPI_DEBUG=2

  build_and_run mpicc mpi_hello.c
  build_and_run mpicxx mpi_hello.cpp
  build_and_run mpif90 mpi_hello.f90
}


function build_and_run
{
  rm -f mpi_hello.bin
  "$@" -o mpi_hello.bin && (
    mpirun -n $SLURM_NTASKS mpi_hello.bin
    srun --mpi=pmi2 --ntasks=$SLURM_NTASKS mpi_hello.bin
  ) || echo "failed:" "$@"
}


main "$@"
