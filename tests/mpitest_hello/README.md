source /curc/sw/views/develop/lmod/lmod/8.3/init/bash
export MODULEPATH=/curc/sw/modules/spack/develop/linux-rhel7-x86_64/Core
module load gcc openmpi
salloc --account=admin --qos=blanca-curc --ntasks=2 --tasks-per-node=1 --cpus-per-task=1
bash mpitest_hello.sh
