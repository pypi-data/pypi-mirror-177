#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import math
import numpy as np
import itertools



###for 2 GPU and 1 node

import itertools
import pandas as pd


# In[ ]:


def Benchmark_1gpu():
    list_one = list((range(1, 19)))
    list_two =list((range(1, 19)))
    result = itertools.product(list_one, list_two)
    df=pd.DataFrame(result, columns=['ntasks', 'cpu'])
    df['cores'] = df['ntasks'] * df['cpu']
    df = df.drop(df[df.cores >= 18].index)
    df = df.drop(df[df.cpu == 1].index)

    x=len(df.index)
    run = range(0,int(x))
    df['run'] = run


    for index, row in df.iterrows():
        with open("job_script_1_" + (str(row["run"])), "w") as f:
            f.write(
                    "#!/bin/bash -l" +  "\n"
                    "# Standard output and error:" +  "\n"
                    "#SBATCH -o ./bench.out.%j"+  "\n"
                    "#SBATCH -e ./bench.err.%j"+  "\n"
                    "# Initial working directory:"+  "\n"
                    "#SBATCH -D ./"+  "\n"
                    "#"+  "\n"
                    "#SBATCH -J bingo"+  "\n"
                    "#"+  "\n"
                    "# Queue:" +  "\n"
                    "#SBATCH --partition=s.phys" + "\n"
                    "#SBATCH --gres=gpu:1"+  "\n"
                    "# Request 10 nodes"+  "\n"
                    "#SBATCH --nodes=1"+  "\n"
                    "# Set the number of tasks per node (=MPI ranks)"+  "\n"
                    "#SBATCH --ntasks-per-node=" + str(row["ntasks"]) + "\n"
                    "# Set the number of threads per rank (=OpenMP threads)"+  "\n"
                    "#SBATCH --cpus-per-task="+ str(row["cpu"]) + "\n"
                    "# Explicitly disable hyperthreading"+  "\n"
                    "#SBATCH --ntasks-per-core=1" + "\n"
                    "#SBATCH --mem=62000" + "\n"
                    "#SBATCH --time=01:00:00" + "\n"
                    "" + "\n"
                    "module purge" + "\n"
                    "module load intel/19.1.3"+  "\n"
                    "module load impi/2019.9"+  "\n"
                    "module load cuda/11.4"+  "\n"
                    "module load anaconda" + "\n"
                    "module load gcc/10" + "\n"
                    "module load gromacs/2021.5"+  "\n"
                    ""+  "\n"
                    "export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK"+  "\n"
                    "export OMP_PLACES=cores"+  "\n"
                    ""+  "\n"
                    "srun gmx_mpi mdrun -v -s *.tpr -ntomp $OMP_NUM_THREADS -maxh 0.25"+  "\n"

        )
        f.close()

