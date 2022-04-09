import numpy as np
import qmlspectrum
import pandas as pd
'''
A module containing functions for various types of binning.
'''
def bin_spectra_uniform(spec_path, read_P, file_P, wavelength_min, wavelength_max, N_bin):
    '''
    A function for binning spectra using a uniform bin width
    '''
    spec_files=qmlspectrum.read_files(spec_path)
    if read_P:
        dlambda = (wavelength_max - wavelength_min)/N_bin
        lam=[]
        for i_bin in range(N_bin):
            lam.append( (i_bin+1.0/2.0)*dlambda )
        Int_lam = np.load(file_P)

    else:
        print('binning spectra')

        dlambda = (wavelength_max - wavelength_min)/N_bin
        lambda_min=[]
        lambda_max=[]
        lam=[]
        for i_bin in range(N_bin):
            lambda_min.append( (i_bin)*dlambda )
            lambda_max.append( (i_bin+1)*dlambda )
            lam.append( (i_bin+1.0/2.0)*dlambda )
        N_file=len(spec_files)
        i_file=0
        Int_lam=np.zeros([N_file,N_bin])
        for spec_csv in spec_files:
            if np.mod(i_file, 100) == 0:
                print(i_file,' out of ', N_file, ' done')
            spec_data=pd.read_csv(spec_path+'/'+spec_csv, names=['wavelength_nm', 'osc_strength'])
            wavelength=np.array(spec_data['wavelength_nm'])
            f=np.array(spec_data['osc_strength'])
            for i_bin in range(N_bin):
                sum_f=0.0
                for i_state in range(f.shape[0]):
                    if wavelength[i_state] > lambda_min[i_bin] and wavelength[i_state] <= lambda_max[i_bin]:
                        sum_f=sum_f+f[i_state]
                Int_lam[i_file,i_bin]=sum_f
            i_file=i_file+1
        np.save(file_P, Int_lam)
        print('data saved in ', file_P)

    return lam, Int_lam

def bin_spectra_nonuniform(spec_path, file_P, wavelength_min, wavelength_max, N_train, spec_den, N_state):
    '''
    A function for binning spectra using non-uniform bin widths
    '''
    spec_files = qmlspectrum.read_files(spec_path)
    print('binning spectra')
    
    N_bin = int(N_state/spec_den)
    all_wavelength = []
    for i in range(N_train):
        spec_data = pd.read_csv(spec_path+'/'+spec_files[i], names=['wavelength_nm', 'osc_strength'])
        wavelength = spec_data['wavelength_nm'].tolist()
        all_wavelength = all_wavelength + wavelength
    all_wavelength = pd.DataFrame(all_wavelength, columns=['wavelength_nm'])
    all_wavelength['bins'], bins = pd.qcut(all_wavelength['wavelength_nm'], q=N_bin, retbins=True, precision=6)
    dlambda = [bins[i + 1] - bins[i] for i in range(len(bins)-1)]
    lambda_min = []
    lambda_max = []
    lam = []
    for i in range(N_bin):
        lambda_min.append(bins[i])
        lambda_max.append(bins[i+1])
        lam.append((bins[i] + bins[i+1])/2.0)
    N_file=len(spec_files)
    i_file=0
    Int_lam=np.zeros([N_file,N_bin])
    for spec_csv in spec_files:
        if np.mod(i_file, 100) == 0:
            print(i_file,' out of ', N_file, ' done')
        spec_data=pd.read_csv(spec_path+'/'+spec_csv, names=['wavelength_nm', 'osc_strength'])
        wavelength=np.array(spec_data['wavelength_nm'])
        f=np.array(spec_data['osc_strength'])
        for i_bin in range(N_bin):
            sum_f=0.0
            for i_state in range(f.shape[0]):
                if wavelength[i_state] > lambda_min[i_bin] and wavelength[i_state] <= lambda_max[i_bin]:
                    sum_f=sum_f+f[i_state]
            Int_lam[i_file,i_bin]=sum_f
        i_file=i_file+1
    np.save(file_P, Int_lam)
    print('data saved in ', file_P)

    return lambda_min, lam, Int_lam, dlambda 
