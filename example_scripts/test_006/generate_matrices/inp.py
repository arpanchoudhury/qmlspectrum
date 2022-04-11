import qmlspectrum
import numpy as np

#== Inputs

# Geometry, geom_path contains xyz files named as 000001.xyz and so on
geom_path='/Users/raghurama/repos/qmlspectrum/datasets/dataset_melanin/DKI_geom'

# Spectra, spec_path contains csv files with wavelength (nm) and oscillator strength named as 000001.csv and so on
spec_path='/Users/raghurama/repos/qmlspectrum/datasets/dataset_melanin/DKI_spectra'

# FCHL settings
sigmas=[5]
cut_distance=10.0

# KRR settings
lamd=1e-4              # Regularization strength, lambda

# Binning
########
N_train=100 # N_train must be defined before binning part
spec_den=5.0
N_state=50

########
wavelength_max=800.0
wavelength_min=200.0

# Options to load data
read_X=True            # If true, descriptors will be loaded from 'file_X', if false will be calculated and stored in this file
file_X='FCHL_GAFF_MD_DKI.npy'

read_P=False            # If true, binned properties will be loaded from 'file_P', if false will be calculated and stored in this file
file_P='CAMB3LYP_631Gs_5.0spec_den_DKI.npy'

# Shuffling
load_indices=True
file_indices='shuffle_index.dat'

#=== End of General Inputs

#=== Generate FCHL representation
N_mol, max_size, X = qmlspectrum.qml_fchl_rep(geom_path, read_X, file_X, cut_distance)

#=== Bin spectra for all molecules
Int_lam, lambda_min, dlambda, N_bin=qmlspectrum.bin_spectra_nonuniform(spec_path, read_P, file_P, wavelength_min, wavelength_max, N_train, spec_den, N_state)

#=== Shuffle
indices=qmlspectrum.shuffle(False, load_indices, file_indices, N_mol)

#=== Training
# Generate the kernel matrix, and collect property of training molecules
load_K=True
file_kernel='Kernel_FCHL_GAFF_MD_DKI_0100.dat.npy'

K,P = qmlspectrum.prepare_trainingdata(N_train,load_K,file_kernel,indices,lamd,X,Int_lam,sigmas,cut_distance,max_size)

# solve KRR equations
alpha=qmlspectrum.linalg_solve(N_bin,K,P)

#=== prediction
iquery=100 
Int_pred=qmlspectrum.predict(X,alpha,indices,iquery,max_size,sigmas,cut_distance)
Int_TDDFT=Int_lam[iquery,:]

f=open('Int.dat','w')
for i in range(N_bin):
    f.write(str(lambda_min[i])+' '+str(dlambda[i])+' '+str(Int_pred[i])+ ' ' +str(Int_TDDFT[i])+'\n')
f.close()


#=== Other options for plotting
# Plot a bar spectrum with varying bin width
qmlspectrum.plot_bar_compare(lambda_min,Int_pred, Int_TDDFT,dlambda,['ML', 'TDDFT'],'compare_ML_TDDFT.png')

# Additional post-processing of the plot can be done in plot.ipynb
