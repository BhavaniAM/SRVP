# -*- coding: utf-8 -*-
"""Video_Prediction_SRVP_MMNIST.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1LgcdZjqm2pv5c0kzV66GENzAOfAgygmb

Mount Google Drive
---
"""

from google.colab import drive
drive.mount('/gdrive', force_remount=True)

# Commented out IPython magic to ensure Python compatibility.
# %cd /gdrive/MyDrive/Colab/Notebooks/Video_Prediction/SRVP/MMNIST

"""Install dependencies
---
"""

# ! mkdir det_test_set
! python3 -m pip install configargparse

"""Create the testset
---

Generate the testset and run the testing code on the dataset (for total 25 frames)
---
"""

!python -m preprocessing.mmnist.make_test_set --data_dir datasets/work_det_mmnist --deterministic --seq_len 25

! mkdir '/content/predicted'
! mkdir '/content/target'
! mkdir '/content/conditional'

! pip install 'tensorflow>=1.15, <2'
! pip install tensorflow-gan==1.0.0.dev0

!python test.py --data_dir datasets/work_det_mmnist --xp_dir pretrained_models/mmnist/deterministic --lpips_dir weights --n_samples 1 --nt_gen 25 --fvd

"""Generate metrics.csv
---
"""

from zipfile import ZipFile
with ZipFile('pretrained_models/mmnist/full_results_mmnist_srvp.zip', 'r') as z:
  z.extractall('pretrained_models/mmnist/')

!pwd

import numpy as np
full_results = np.load('pretrained_models/mmnist/full_results_mmnist_det_srvp/results.npz')

import pandas as pd

ssim_best = full_results['ssim']
psnr_best = full_results['psnr']
lpips_best = full_results['lpips']

num_vid = [i for i in range(1,5001)]
dict = {'num_vid': num_vid, 'ssim_best': ssim_best,'psnr_best': psnr_best,'lpips_best': lpips_best} 
df = pd.DataFrame(dict) 
df.to_csv('full_metrics_srvp.csv', index = False)

import numpy as np
results_best = np.load('pretrained_models/mmnist/deterministic/results.npz')
results_worst = np.load('pretrained_models/mmnist/deterministic/results_worst.npz')

import pandas as pd

ssim_best = results_best['ssim']
psnr_best = results_best['psnr']
lpips_best = results_best['lpips']

ssim_worst = results_worst['ssim']
psnr_worst = results_worst['psnr']
lpips_worst = results_worst['lpips']

print(ssim_best)
print(ssim_worst)

# num_vid = [i for i in range(1,opt.batch_size+1)]
num_vid = [i for i in range(1,16+1)]
dict = {'num_vid': num_vid, 'ssim_best': ssim_best, 'ssim_worst': ssim_worst, 'psnr_best': psnr_best, 'psnr_worst': psnr_worst, 'lpips_best': lpips_best, 'lpips_worst': lpips_worst} 
df = pd.DataFrame(dict) 
df.to_csv('metrics.csv', index = False)

"""# Best and worst frames from the full metrics"""

import numpy as np
import torch
from google.colab import files
import matplotlib.pyplot as plt

# Commented out IPython magic to ensure Python compatibility.
# To remove a directory (can be empty or can have data)
# %rm -rf /content/ssim_best
# %rm -rf /content/ssim_worst
# %rm -rf /content/psnr_best
# %rm -rf /content/psnr_worst

import pandas as pd
df = pd.read_csv('./full_metrics_srvp.csv')

df

df.sort_values('ssim_best',inplace = True)
df

df.sort_values('psnr_best',inplace = True)
df

df.sort_values('lpips_best',inplace = True)
df

full_results = np.load('pretrained_models/mmnist/full_results_mmnist_det_srvp/ssim_best.npz')
print(full_results['samples'].shape)

!mkdir '/content/ssim_best'
full_results = np.load('pretrained_models/mmnist/full_results_mmnist_det_srvp/ssim_best.npz')
new_video = full_results['samples'].reshape(5000, 20, 1, 64, 64)
num_frames = 20
batch = 5000
new_save_number = 1
for i in range(batch):
  if(i == 4618 or i == 3349):
    for j in range(num_frames):
      plt.imsave('/content/ssim_best/x_ssim_best_' + str(i) + "_" + str(new_save_number) + '.png', new_video[i][j].reshape(64,64), cmap='gray')
      new_save_number = new_save_number + 1

!mkdir /content/ssim_worst
full_results = np.load('pretrained_models/mmnist/full_results_mmnist_det_srvp/ssim_worst.npz')
new_video = full_results['samples'].reshape(5000, 20, 1, 64, 64)
num_frames = 20
batch = 5000
new_save_number = 1
for i in range(batch):
  if(i == 931 or i == 3173):
    for j in range(num_frames):
      plt.imsave('/content/ssim_worst/x_ssim_worst_' + str(i) + "_" + str(new_save_number) + '.png', new_video[i][j].reshape(64,64), cmap='gray')
      new_save_number = new_save_number + 1

# Commented out IPython magic to ensure Python compatibility.
# %rm -rf /content/psnr_best
!mkdir '/content/psnr_best'
full_results = np.load('pretrained_models/mmnist/full_results_mmnist_det_srvp/psnr_best.npz')
new_video = full_results['samples'].reshape(5000, 20, 1, 64, 64)
num_frames = 20
batch = 5000
new_save_number = 1
for i in range(batch):
  if(i == 4618 or i == 3283):
    for j in range(num_frames):
      plt.imsave('/content/psnr_best/x_psnr_best_' + str(i) + "_" + str(new_save_number) + '.png', new_video[i][j].reshape(64,64), cmap='gray')
      new_save_number = new_save_number + 1

!mkdir /content/psnr_worst
full_results = np.load('pretrained_models/mmnist/full_results_mmnist_det_srvp/psnr_worst.npz')
new_video = full_results['samples'].reshape(5000, 20, 1, 64, 64)
num_frames = 20
batch = 5000
new_save_number = 1
for i in range(batch):
  if(i == 931 or i == 3173):
    for j in range(num_frames):
      plt.imsave('/content/psnr_worst/x_psnr_worst' + str(i) + "_" + str(new_save_number) + '.png', new_video[i][j].reshape(64,64), cmap='gray')
      new_save_number = new_save_number + 1

# Commented out IPython magic to ensure Python compatibility.
# %rm -rf /content/lpips_best
!mkdir '/content/lpips_best'
full_results = np.load('pretrained_models/mmnist/full_results_mmnist_det_srvp/lpips_best.npz')
new_video = full_results['samples'].reshape(5000, 20, 1, 64, 64)
num_frames = 20
batch = 5000
new_save_number = 1
for i in range(batch):
  if(i == 4932 or i == 4246):
    for j in range(num_frames):
      plt.imsave('/content/lpips_best/x_lpips_best_' + str(i) + "_" + str(new_save_number) + '.png', new_video[i][j].reshape(64,64), cmap='gray')
      new_save_number = new_save_number + 1

# Commented out IPython magic to ensure Python compatibility.
# %rm -rf /content/lpips_worst
!mkdir /content/lpips_worst
full_results = np.load('pretrained_models/mmnist/full_results_mmnist_det_srvp/lpips_worst.npz')
new_video = full_results['samples'].reshape(5000, 20, 1, 64, 64)
num_frames = 20
batch = 5000
new_save_number = 1
for i in range(batch):
  if(i == 257 or i == 3373):
    for j in range(num_frames):
      plt.imsave('/content/lpips_worst/x_lpips_worst' + str(bhav) + "_" + str(new_save_number) + '.png', new_video[i][j].reshape(64,64), cmap='gray')
      new_save_number = new_save_number + 1