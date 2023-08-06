import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import aplpy
from astropy.wcs import WCS
from astroquery.gaia import Gaia 
import pandas as pd
from astropy import units as u
from astropy.io import fits
from astropy.table import Table
from astropy.coordinates import SkyCoord
from scipy.optimize import curve_fit
from astropy.stats import bootstrap
import matplotlib.ticker as ticker
plt.rcParams.update({'font.size': 18})
plt.rcParams['xtick.labelsize']=16
plt.rcParams['ytick.labelsize']=16

def paramters_search(ra_coord,dec_coord):
    """parameters_search

    Given RA and DEC coordinates this program finds the parallax and distance using GAIA data release 3
    
    Args:
        ra_coord (float): RA coordinate at which to search 
        dec_coord (float): DEC coordinate at which to search 
    Returns:
        parallax: (float): Gaia parallax of the object at the given RA and DEC
        dist: (float): Hipparcos distance to the object at the given RA and DEC
        search_width (float): Search area in which object was found
    """
    Gaia.MAIN_GAIA_TABLE = "gaiadr3.gaia_source" # select Gaia release 

    search_width = 0 #initialising the search width
    flag = 0 
    while flag == 0: # initialize the while loop till we find an object within search width
        search_width += 0.25
        coord = SkyCoord(ra=ra_coord, dec=dec_coord, unit=(u.degree, u.degree),frame='icrs')
        width = u.Quantity(search_width, u.arcsecond)
        height = u.Quantity(search_width, u.arcsecond)
        results = Gaia.query_object(coordinate=coord, width=width, height=height)
        flag  = results['parallax'].shape[0]
        if abs(search_width - 30*0.25)< 0.2:  # condition so that the search width doesn't increase 0.25 degrees
            return -1,-1,-1 # returns -1 values as parallax and distances can't be negative 
    print(search_width) 
    return results['parallax'][0],results['dist'][0],search_width



def generate_RA_DEC_mesh(hdu):
    """generate_RA_DEC_mesh

    Given the fits file HDU the function generates the RA and DEC grids
    
    Args:
        hdu (astropy fits): RA coordinate at which to search 
    Returns:
        DEC_grid (2D array): DEC grid for the given fits file
        RA_grid (2D array): RA grid for the given fits file
    """
    if 'CDELT1' in hdu.header:
        RA_delt = hdu.header['CDELT1']
        DEC_delt = hdu.header['CDELT2']

    if 'CD1_1' in hdu.header:
        RA_delt = hdu.header['CD1_1']
        DEC_delt = hdu.header['CD2_2']

    RA_ref = (hdu.header['CRPIX1'])
    DEC_ref = (hdu.header['CRPIX2'])
    RA_ref_value = hdu.header['CRVAL1']
    DEC_ref_value = hdu.header['CRVAL2']
    RA_axis_len = hdu.header['NAXIS1']
    DEC_axis_len = hdu.header['NAXIS2']

    RA_axis = np.arange(1,RA_axis_len+1)
    DEC_axis = np.arange(1,DEC_axis_len+1)
    DEC_axis_modified = np.arange(1,RA_axis_len+1)
    
    DEC_array = (DEC_axis - DEC_axis_len/2)*DEC_delt + DEC_ref_value
    DEC_array_modified = (DEC_axis_modified - RA_axis_len/2)*DEC_delt + DEC_ref_value
    RA_array = RA_ref_value-(RA_axis - RA_axis_len/2)*(RA_delt*(-1)/np.cos(DEC_array_modified*0.01745))

    # #making a meshgrid from the arrays
    DEC_grid,RA_grid = np.meshgrid(DEC_array,RA_array , sparse=False, indexing='ij')
    return DEC_grid,RA_grid



def Calc_l(ra1,dec1,ra2,dec2):
    """Calc_l

    The function calculates the distance between two points on the celestial plane
    
    Args:
        ra1 (float): RA coordinate of first position in degrees
        dec1 (float): DEC coordinate of first position in degrees
        ra2 (float): RA coordinate of second position in degrees
        dec2 (float): DEC coordinate of second position in degrees
    Returns:
        seperation (float): returns the seperation in arcminutes between the two points on the celestial sphere

    """
    c1 = SkyCoord(ra1,dec1,unit = 'deg')
    c2 = SkyCoord(ra2,dec2,unit = 'deg')
    sep = c1.separation(c2)
    return sep.arcminute


def wrapper(Angle_grid):
    """wrapper

    The function keeps the polarization angles in a array between -90 and 90
    
    Args:
        Angle_grid (N-D numpy array): N dimensional array consisting of polarization angles
    Returns:
        Angle_grid (N-D numpy array): N dimensional array consisting of modified polarization angles
    """
    while ((np.nanmax(Angle_grid)>90) or (np.nanmin(Angle_grid)<-90)):
        Angle_selector =Angle_grid>90
        Angle_grid[Angle_selector] = Angle_grid[Angle_selector] - 180
        Angle_selector = Angle_grid<-90
        Angle_grid[Angle_selector] = Angle_grid[Angle_selector] + 180
    return Angle_grid

    
def remove_nan(array1,array2):
    """remove_nan

    The function removes the NAN values in two arrays to create modified arrays of same size. Useful for removing NAN values 
    in two arrays with one being the function of other
    
    Args:
        array1 (numpy array): first array to be filtered
        array2 (numpy array): Second array to be filtered
    Returns:
        array1_fil (numpy array): first array filtered
        array2_fil (numpy array): Second array filtered
    """
    selector = ~np.isnan(array1)
    array1_fil = array1[selector]
    array2_fil = array2[selector]

    selector = ~np.isnan(array2_fil)
    array1_fil = array1_fil[selector]
    array2_fil = array2_fil[selector]
    return array1_fil,array2_fil

def quality_cuts(stokesI,stokesIerr,Pol,Polerr,SNRp_cut,p_cut,SNRi_cut):
    """quality_cuts

    The function does the signal to noise ratio qualtity cuts for polarizaiton fraction.

    Args:
		stokesI (astropy.io.fits.PrimaryHDU): The Stokes I file in astropy.io.fits.PrimaryHDU.
		stokesIerr (astropy.io.fits.PrimaryHDU): The error in Stokes I file in astropy.io.fits.PrimaryHDU.
		Pol (astropy.io.fits.PrimaryHDU): The Polarization fraction in astropy.io.fits.PrimaryHDU format.
		Polerr (astropy.io.fits.PrimaryHDU): The error in Polarization fraction in astropy.io.fits.PrimaryHDU format.
		SNRp_cut (float): Signal to noise ratio cutoff for Polarizaiton fraction.
		p_cut (float): Maximum value cutoff for Polarizaiton fraction.
        SNRi_cut (float): Signal to noise ratio cutoff for Intensity.
    Returns:
	    Pol (astropy.io.fits.PrimaryHDU): The filtered Polarization fraction in astropy.io.fits.PrimaryHDU format.
    """
	#snr in P
    SNRp = Pol.data/Polerr.data
    mask_snrp = np.where(SNRp < SNRp_cut)
    Pol.data[mask_snrp] = np.nan
    #p_cut
    maskp = np.where(Pol.data > p_cut)
    Pol.data[maskp] = np.nan
    #snr in P
    SNRi = stokesI.data/stokesIerr.data
    mask_snri = np.where(SNRi < SNRi_cut)
    Pol.data[mask_snri] = np.nan
    return Pol