from math import degrees
from tkinter import font
import numpy as np
import pandas as pd
from astropy import units as u
from astropy.coordinates import SkyCoord
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
plt.rcParams.update({'font.size': 22})

def StructureFunctionAnalysis(path_to_datafile, bin_size,ColumnDensity,VelocityDispersion,SNR_limit=2):
    """StructureFunctionAnalysis

    This function implements Hildebrand's 2009 method to calculates the plane of the sky magnetic field using modified Davis-Chandrashekhar method. 
    The polarimetry data needs to be provied in a csv file with the following columns 'ra','dec','PA','ePA'
    The function also fits the line structure_function = np.sqrt(b**2 + l**2m**2)
    
    Args:
        path_to_datafile (string): relative path to the csv datafile with polarimetry data.
        bin_size (float): bin size to be used for calculating the structure function.
        ColumnDensity (float): column density of the target in number/cc units.
        VelocityDispersion (float): velocity dispersion value of the target in km/s
        SNR_limit (flaot): SNR ratio to be used to clean the data.
    Returns:
        b (float): b parameter from the strucutre function in radians
        structure_function (2D list): The 2D array consists of the strucutre fucntion and its corresponding (l parameter)
    """


    datafile = path_to_datafile
    l_bins_length = bin_size 
    ColDen = ColumnDensity
    VelDis = VelocityDispersion

    ####### importing the data
    data = pd.read_csv(datafile,delimiter=',')
    data = data[(data['P']/data['eP']) > SNR_limit]
    data = data[0<data['distance_parallax']/1000]
    ra = np.array(data['ra'])
    dec = np.array(data['dec'])
    PolAng = np.array(data['PA'])
    ePolAng = np.array(data['ePA'])

    ###### calculating the distance between two points on the celestial plane
    def Calc_l(ra1,dec1,ra2,dec2):
        c1 = SkyCoord(ra1,dec1,unit = 'deg')
        c2 = SkyCoord(ra2,dec2,unit = 'deg')
        sep = c1.separation(c2)
        return sep.arcminute

    distance_mat = np.ones((ra.shape[0],ra.shape[0]))*np.nan
    PolAngleSqr_diff = np.ones((ra.shape[0],ra.shape[0]))*np.nan
    ePolAngleSqr = np.ones((ra.shape[0],ra.shape[0]))*np.nan

    for i in range(ra.shape[0]):
        for j in range(i):
            if ((PolAng[i] - PolAng[j])>90):
                PolAngleSqr_diff[i,j] = (PolAng[i] - PolAng[j]-180)**2
                ePolAngleSqr[i,j] = ePolAng[i]**2+ePolAng[j]**2
                distance_mat[i,j] = Calc_l(ra[i],dec[i],ra[j],dec[j])

            elif ((PolAng[i] - PolAng[j])<-90):
                PolAngleSqr_diff[i,j] = (PolAng[i] - PolAng[j] + 180)**2
                ePolAngleSqr[i,j] = ePolAng[i]**2+ePolAng[j]**2
                distance_mat[i,j] = Calc_l(ra[i],dec[i],ra[j],dec[j])
            else:
                PolAngleSqr_diff[i,j] = (PolAng[i] - PolAng[j])**2
                ePolAngleSqr[i,j] = ePolAng[i]**2+ePolAng[j]**2
                distance_mat[i,j] = Calc_l(ra[i],dec[i],ra[j],dec[j])

    l_bins = np.arange(0,10,l_bins_length)
    l_bins_centre = (l_bins[:-1] + l_bins[1:])/2

    struc_func = []
    error_func = []
    error1_func = []
    count_array = []

    for k in range(l_bins.shape[0]-1):
        count = 0
        temp_PolAngle = []
        temp_ePolAngle = []
        temp_dist = []
        for i in range(PolAngleSqr_diff.shape[0]):
            for j in range(i):
                if l_bins[k]< distance_mat[i,j]<=l_bins[k+1]:
                    count += 1
                    temp_PolAngle.append(PolAngleSqr_diff[i,j])
                    temp_ePolAngle.append(ePolAngleSqr[i,j])
                    temp_dist.append(distance_mat[i,j])
                else:
                    pass
        if count != 0:
            temp_PolAngle = np.array(temp_PolAngle)
            temp_ePolAngle = np.array(temp_ePolAngle)
            std_PA = np.mean(temp_PolAngle) - np.mean(temp_ePolAngle)
            mean_PA = np.sqrt(std_PA)
            a = np.sqrt(temp_ePolAngle)
            err_PA1 = np.std(a)
            err_PA = err_PA1/np.sqrt(count)
            struc_func.append(mean_PA)
            error1_func.append(err_PA1)
            error_func.append(err_PA)
            count_array.append(count)
        else:
            struc_func.append(np.nan)
            error1_func.append(np.nan)
            error_func.append(np.nan)

    struc_func = np.array(struc_func)
    error_func = np.array(error_func)
    struc_func = np.sqrt(struc_func**2 - error_func**2)

    def fitfun(l, m, b):
        y = np.sqrt(b**2 + (m**2) * (l**2))
        return y

    df = pd.DataFrame({'l_bins': l_bins_centre,'SF':struc_func})
    df = df.dropna()
    popt, pcov = curve_fit(fitfun, df['l_bins'][0:3], df['SF'][0:3])
    line = np.linspace(0,10,100)
    fitted_line = fitfun(line,popt[0],popt[1])

    b = popt[1]
    b1 = popt[1]*np.pi/180
    perr = np.sqrt(np.diag(pcov))
    perr1 = perr*np.pi/180
    ratio = b1/(np.sqrt(2-(b1**2)))

    column_density = ColDen
    velocity_dispersion_FWHM = 2.35*VelDis
    Bmag_modCF = 9.3*(np.sqrt(2*column_density))*velocity_dispersion_FWHM*(1/b)

    print('perr',perr)
    print('Bmag',Bmag_modCF)
    print('ratio',ratio)
    print('Error in ratio', abs(b1/(np.sqrt(2-(b1**2))) - (b1 + perr1[1])/(np.sqrt(2-((b1+perr1[1])**2)))))
    print('b',b)
    print('Error in b',perr[1])
    print('b in radian',b1)
    print('Error in radian b',perr1[1])
    print('Error in ratio', abs(b1/(np.sqrt(2-(b1**2))) - (b1 - perr1[1])/(np.sqrt(2-((b1+perr1[1])**2)))))
    print('Error in ratio', abs(b1/(np.sqrt(2-(b1**2))) - (b1 + perr1[1])/(np.sqrt(2-((b1-perr1[1])**2)))))
    print('Error in ratio', abs(b1/(np.sqrt(2-(b1**2))) - (b1 - perr1[1])/(np.sqrt(2-((b1-perr1[1])**2)))))

    return b,[l_bins_centre ,struc_func]

