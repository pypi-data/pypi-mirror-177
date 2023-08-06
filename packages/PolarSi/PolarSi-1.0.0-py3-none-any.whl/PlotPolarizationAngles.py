from aplpy import FITSFigure  
import matplotlib.pyplot as plt 
import astropy.io.fits as fits
import astropy.units as u 
import numpy as np 
import os as os
import six

def PlotPolarizationAngles(Pol,PolAng,stokesI,stokesIerr,PolInten,background,vmin,vmax,colorbar_label,plot_title,steps=2,vector_color = 'cyan',vector_shadow = 'k',vector_length = 2,linewidth = 2,cmap='gray'):
	"""StructureFunctionAnalysis

	This function plots polarization angles on a given background
	The input needs to be an astropy.io.fits.PrimaryHDU

	Args:
		Pol (astropy.io.fits.PrimaryHDU): The Polarization fraction in astropy.io.fits.PrimaryHDU format.
		PolAng (astropy.io.fits.PrimaryHDU): The Polarization angles in astropy.io.fits.PrimaryHDU format.
		stokesI (astropy.io.fits.PrimaryHDU): The Stokes I file in astropy.io.fits.PrimaryHDU.
		stokesIerr (astropy.io.fits.PrimaryHDU): The error in Stokes I file in astropy.io.fits.PrimaryHDU.
		PolInten (astropy.io.fits.PrimaryHDU): The Polarization intensity in astropy.io.fits.PrimaryHDU format.
		background (astropy.io.fits.PrimaryHDU): The background on which the polarization angles needs to plotted in astropy.io.fits.PrimaryHDU format.
		vmin (float): The vmin value for the background in aplpy.show_colorscale
		vmax (float): The vmax value for the background in aplpy.show_colorscale
		colorbar_label (string): The label for colorbar
		plot_title (string): The title for the figure
		steps (int): Steps of the vectors plotted. Default is 2 plotting every 2nd vector, choosing 1 means plotting every vector
		vector_color (string): Color of the vectors. Default is cyan.
		vector_shadow (string): Color of the vectors. Default is black
		vector_length (float): The length of the vector. Default is 2
		linewidth (float): The width of the vector. Default is 2
		cmap (string): Color scheme for the plot	
	Returns:
		Plots the vectors on the background.
	"""
	p    = Pol
	pa   = PolAng
	stkI = stokesI
	stkIerr = stokesIerr
	pi = PolInten
	title = plot_title
	pxscale = stkI.header['CDELT2']*3600
	stkI.data /= pxscale**2
	pi.data /= pxscale**2 
	stkIerr.data /= pxscale**2
	title_size = 16
	tick_colorbar = 15
	scalevec = vector_length #1px = scalevec * 1% pol 
	vec_legend = 5.0

	#### SCRIPT
	fig = plt.figure(figsize=(13,10))
	scuba = FITSFigure(background,figure=fig)

	#colorscale
	scuba.show_colorscale(cmap=cmap,vmin = vmin,vmax = vmax)



	#colorbar
	scuba.add_colorbar(location='right', width=0.2, pad=0.15, ticks=None,axis_label_text= colorbar_label)
	scuba.colorbar.set_font(size=tick_colorbar)
	scuba.set_title(title,fontsize=title_size)

	scuba.show_vectors(p,pa,scale=scalevec,step=steps,color=vector_shadow,linewidth=linewidth*1.5)
	scuba.show_vectors(p,pa,scale=scalevec,step=steps,color=vector_color,linewidth=linewidth)

	vecscale = scalevec * pxscale/3600
	scuba.add_scalebar(vec_legend*vecscale,r'$p_{frac}$ ='+np.str(vec_legend),corner='bottom right',frame=True,color='black')
	plt.show()

