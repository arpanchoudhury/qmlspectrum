import os
from os import listdir
from os.path import isfile, join
import sys
import qml
import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt
import pandas as pd

def read_geom_files(geom_path):
    geom_files = [f for f in listdir(geom_path) if isfile(join(geom_path, f))]
    geom_files = sorted(geom_files)
    return geom_files

def read_spectra(spec_path):
    spec_files = [f for f in listdir(spec_path) if isfile(join(spec_path, f))]
    spec_files = sorted(spec_files)
    return spec_files

def bin_spectra(spec_path,spec_files, wavelength_min, wavelength_max, N_bin):
    dlambda = (wavelength_max - wavelength_min)/N_bin
    lambda_min=[]
    lambda_max=[]
    lam=[]
    for i_bin in range(N_bin):
        lambda_min.append( (i_bin)*dlambda )
        lambda_max.append( (i_bin+1)*dlambda )
        lam.append( (i_bin+1.0/2.0)*dlambda )
    Int_lam=[]
    N_file=len(spec_files)
    i_file=0
    for spec_csv in spec_files:
        if np.mod(i_file, 100) == 0:
            print(i_file,' out of ', N_file, ' done') 
        spec_data=pd.read_csv(spec_path+'/'+spec_csv, names=['wavelength_nm', 'osc_strength'])
        wavelength=spec_data['wavelength_nm']
        f=spec_data['osc_strength']
        sum_f=np.zeros(N_bin)
        for i_bin in range(N_bin):
            scr=f[(wavelength > lambda_min[i_bin] ) & (wavelength <= lambda_max[i_bin])]
            sum_f[i_bin]=np.sum( scr )
        i_file=i_file+1
        Int_lam.append(sum_f)

    return lam, Int_lam

def calc_qml_fchl_rep(geom_path, geom_files, max_size, cut_distance):
    N_file=len(geom_files)
    X_all=[]
    i_file=0
    for i_geom in range(N_file):
        if np.mod(i_file, 100) == 0:
            print(i_file,' out of ', N_file, ' done') 
        xyz_file=geom_path+'/'+geom_files[i_geom]
        mol=qml.Compound(xyz=xyz_file)
        representation=qml.fchl.generate_representation(mol.coordinates, mol.nuclear_charges, max_size=max_size, cut_distance=cut_distance)
        X_all.append(representation)
        i_file=i_file+1
    return representation

# Inputs

geom_path='/Users/raghurama/repos/qmlspectrum/datasets/dataset_bigQM7w/bigQM7w_UFF_geoms'
geom_files=read_geom_files(geom_path)

spec_path='/Users/raghurama/repos/qmlspectrum/datasets/dataset_bigQM7w/bigQM7w_wB97XD_def2SVPD_spectra'
spec_files=read_spectra(spec_path)

# FCHL
max_size=23
cut_distance=20.0

# Binning
N_bin=128
wavelength_max=120.0
wavelength_min=0.0

# I/O files
read_X=True
file_X='FCHL_UFF.npy'

read_P=True
file_P='def2SVP_spec_128bins.npy'
#===


if read_X:
    X = np.load(file_X)
else:
    print('calculating FCHL')
    X=calc_qml_fchl_rep(geom_path, geom_files, max_size, cut_distance)
    np.save(file_X, X)
    print('data saved in ', file_X)

if read_P:
    dlambda = (wavelength_max - wavelength_min)/N_bin
    lam=[]
    for i_bin in range(N_bin):
        lam.append( (i_bin+1.0/2.0)*dlambda )
    Int_lam = np.load(file_P)
else:
    print('binning spectra')
    lam,Int_lam=bin_spectra(spec_path, spec_files, wavelength_min, wavelength_max, N_bin)
    np.save(file_P, Int_lam)
    print('data saved in ', file_P)

print(Int_lam.shape)



plt.stem(lam, Int_lam[2], label=r'TDDFT',linewidth=1.0, linefmt='r-', markerfmt=' ')
plt.legend()

plt.xlabel('Wavelength (nm)', fontsize = 15)
plt.ylabel('Oscillator strength (au)', fontsize = 15)
plt.savefig("query_spec_reconstructed.png",bbox_inches='tight')





