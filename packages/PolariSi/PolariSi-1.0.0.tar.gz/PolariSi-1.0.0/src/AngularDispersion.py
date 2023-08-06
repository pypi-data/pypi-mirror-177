import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import aplpy
import pandas as pd
from astropy.io import fits
from astropy.table import Table
from astropy.coordinates import SkyCoord
from scipy.optimize import curve_fit
from astropy.stats import bootstrap
import matplotlib.ticker as ticker
plt.rcParams.update({'font.size': 18})
plt.rcParams['xtick.labelsize']=16
plt.rcParams['ytick.labelsize']=16
from Utilities import generate_RA_DEC_mesh
from Utilities import Calc_l
from Utilities import wrapper


def AngularDispersion(stokesQ,stokesU,PolAngerr,lag = 0.5):    
    """StructureFunctionAnalysis

    This function implements Planck Collaboration 2016 method to calculates the angular dispersion of the region
    The input needs to be an astropy.io.fits.PrimaryHDU
    
    Args:
        stokesQ (astropy.io.fits.PrimaryHDU): The Stokes Q file in astropy.io.fits.PrimaryHDU.
        stokesU (astropy.io.fits.PrimaryHDU): The Stokes U file in astropy.io.fits.PrimaryHDU.
        PolAngerr (astropy.io.fits.PrimaryHDU): The error in Polarization angles in astropy.io.fits.PrimaryHDU format.
        lag (float): The lag also referred to as delta is specifies the area under which the angular dispersion is calculated, For more information please refer to the paper mentioned above.
        
    Returns:
        S_map_deb (2D numpy array): returns the debiased angular dispersion map of the region.
    """

    ############## generating the RA and DEC mesh
    DEC_grid,RA_grid = generate_RA_DEC_mesh(stokesQ)
    seperation = stokesQ.copy()
    set_delta = lag   # in arcminute
    S_map = stokesQ.copy()
    sigma_S_map = stokesQ.copy()

    for i in range(RA_grid.shape[0]):
        for j in range(RA_grid.shape[1]):
            ##### seperation filter
            seperation.data = Calc_l(RA_grid[i,j],DEC_grid[i,j],RA_grid,DEC_grid)
            seperation_selector = (seperation.data<0.5*set_delta)
            seperation.data[seperation_selector] = np.nan
            seperation_selector = (seperation.data>1.5*set_delta)
            seperation.data[seperation_selector] = np.nan
            seperation_selector = (seperation.data >0)

            ##### making the dispersion map
            tempa = stokesQ.data*stokesU.data[i,j] - stokesQ.data[i,j]*stokesU.data
            tempb = stokesQ.data*stokesQ.data[i,j] + stokesU.data*stokesU.data[i,j]
            AngleDiff_v2 = 0.5 * (180/np.pi)*np.arctan2(tempa,tempb)
            S = np.nanmean(AngleDiff_v2[seperation_selector]**2)**0.5
            S_map.data[i,j] = S

            ##### making the dispersion error map
            sigma_S = np.nanmean(PolAngerr.data[seperation_selector]**2)**0.5
            sigma_S_map.data[i,j] = sigma_S
    S_map_deb = S_map.copy()
    S_map_deb.data = np.sqrt(S_map.data**2 - sigma_S_map.data**2)
    return S_map_deb