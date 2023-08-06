from aplpy import FITSFigure  
import matplotlib.pyplot as plt 
import astropy.io.fits as fits
import astropy.units as u 
import numpy as np 
import os as os
import six
import pandas as pd
plt.rcParams.update({'font.size': 18})

def PlanckPolarization(path_to_stokesI,path_to_stokesQ,path_to_stokesU,path_to_background,angle_offset,vmin,vmax,line_width,vector_scale,steps = 2,vector_color= 'cyan',cmap = 'gray'):
    """PlanckPolarization

    This function plots the magnetic fields from Planck Polarization vecotrs. The function requires the Planck polarization stokes I,Q and U map in celestial coordiantes (fk5).
    The function also requires a variable angle_offset which is the angle between the galactic and celestial north at the position of the target
    
    Args:
        path_to_stokesI (string): relative path to the fits file of the Planck stokes I file in celestial coordinates.
        path_to_stokesQ (string): relative path to the fits file of the Planck stokes Q file in celestial coordinates.
        path_to_stokesU (string): relative path to the fits file of the Planck stokes U file in celestial coordinates.
        path_to_background (string): relative path to the fits file of the background in celestial coordinates.
        angle_offset (float): The angle between the between the galactic and celestial north at the position of the target
        vmin = This parameter controls the minimum cutoff of the background for plotting
        vmax = This parameter controls the minimum cutoff of the background for plotting
        line_width (float): This parameter controls the width of the vector
        steps (integer): This paramter controls the vectors skipped. If steps is 1 it plots every vector, default is 2 which plots every second vector
        vector_scale (flaot): This parameter controls the length of the vector
        vector_color (string): Color of the vectors. Default cyan
        cmap (string): Colormap of the background. Default gray

    Returns:
        Plots the magnetic fields from Planck Polarization vectors
    """

    def get_data(stokesI,stokesQ,stokesU,angle_offset):
        stokesIfile = fits.open(stokesI)
        stokesQfile = fits.open(stokesQ)
        stokesUfile = fits.open(stokesU)
        plank_polarization = stokesIfile[0].copy()
        plank_theta_mod = stokesIfile[0].copy()
        plank_polarization.data = np.sqrt(stokesQfile[0].data*stokesQfile[0].data + stokesUfile[0].data*stokesUfile[0].data)/stokesIfile[0].data
        plank_theta_mod.data = (180/np.pi)*0.5*np.arctan2(-1*stokesUfile[0].data,stokesQfile[0].data) + 90 + angle_offset

        return plank_polarization,plank_theta_mod
    p,pa = get_data(path_to_stokesI,path_to_stokesQ,path_to_stokesU,angle_offset)
    Background = fits.open(path_to_background)[0]

    ###Figure
    scalevec = vector_scale #1px = scalevec * 1% pol 
    p.data = p.data/p.data
    fig = plt.figure(figsize=(13,10))
    gc = FITSFigure(Background,figure=fig)
    gc.show_colorscale(cmap=cmap,vmin=vmin,vmax =vmax)
    gc.show_vectors(p,pa,scale=scalevec,step=steps,color=vector_color,linewidth=line_width)
    gc.show_vectors(p,pa,scale=scalevec,step=steps,color='k',linewidth=line_width*1.1)
    plt.show()


