import qmlspectrum
import numpy as np

#== Inputs

# Geometry, geom_path contains xyz files named as 000001.xyz and so on
geom_path='/Users/raghurama/repos/qmlspectrum/datasets/dataset_bigQM7w/bigQM7w_UFF_geoms'

# Spectra, spec_path contains csv files with wavelength (nm) and oscillator strength named as 000001.csv and so on
spec_path='/Users/raghurama/repos/qmlspectrum/datasets/dataset_bigQM7w/bigQM7w_wB97XD_def2SVPD_spectra'

# FCHL settings
sigmas=[5]
cut_distance=10.0

# KRR settings
lamd=1e-4              # Regularization strength, lambda

# Binning
N_bin=128
wavelength_max=120.0
wavelength_min=0.0

# Options to load data
read_X=True            # If true, descriptors will be loaded from 'file_X', if false will be calculated and stored in this file
file_X='FCHL_UFF.npy'

read_P=True            # If true, binned properties will be loaded from 'file_P', if false will be calculated and stored in this file
file_P='def2SVP_spec_128bins.npy'

# Shuffling
load_indices=True
file_indices='shuffle_index.dat'

#=== End of General Inputs

#=== Generate FCHL representation
N_mol, max_size, X = qmlspectrum.qml_fchl_rep(geom_path, read_X, file_X, cut_distance)

#=== Bin spectra for all molecules
lam,Int_lam=qmlspectrum.bin_spectra_uniform(spec_path, read_P, file_P, wavelength_min, wavelength_max, N_bin)

for i_mol in range(N_mol):
    Int_lam[i_mol,:]=Int_lam[i_mol,:]/np.sum(Int_lam[i_mol,:])

#=== Shuffle
indices=qmlspectrum.shuffle(load_indices, file_indices, N_mol)

#=== Training
# Generate the kernel matrix, and collect property of training molecules
N_train=100
load_K=True
file_kernel='Kernel_00100.dat.npy'

K,P = qmlspectrum.prepare_trainingdata(N_train,load_K,file_kernel,indices,lamd,X,Int_lam,sigmas,cut_distance,max_size)

# solve KRR equations
alpha=qmlspectrum.linalg_solve(N_bin,K,P,'train_spec_00100.txt','coeffs_00100.txt')

#=== prediction

iquery=0
Int_pred=qmlspectrum.predict(X,alpha,indices,iquery,max_size,sigmas,cut_distance)
Int_TDDFT=Int_lam[indices[iquery],:]
phi=qmlspectrum.confidence_score(Int_pred, Int_TDDFT)
print('Confidence score for entry ', iquery,'= ',phi, ' %')

iquery=5000
Int_pred=qmlspectrum.predict(X,alpha,indices,iquery,max_size,sigmas,cut_distance)
Int_TDDFT=Int_lam[indices[iquery],:]
phi=qmlspectrum.confidence_score(Int_pred, Int_TDDFT)
print('Confidence score for entry ', iquery,'= ',phi, ' %')

