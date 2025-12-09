#!/bin/bash
#SBATCH -N 1
#SBATCH -n 10
#SBATCH --mem=50g
#SBATCH -J "CS547"
#SBATCH -p short
#SBATCH -t 12:00:00
#SBATCH --gres=gpu:1

# Load CUDA modules
module load cuda12.6/toolkit
module load cuda12.6/blas
module load cuda12.6/fft
/home/ostikar/.conda/envs/clashroyale/bin/python -u process_spanish_lyrics.py \
  --input /home/ostikar/MyProjects/CS547/project/data/genius/spanish_lyrics.csv \
  --output /home/ostikar/MyProjects/CS547/project/data/genius/spanish_lyrics_processed.csv \
  --lyrics-col lyrics