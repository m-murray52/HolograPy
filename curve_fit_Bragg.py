import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np
import pandas as pd
from scipy.interpolate import UnivariateSpline
import argparse 

# load video and select frame averaging method
parser = argparse.ArgumentParser(description='Code for plotting measured Bragg Curve Data and plottng best fit')
parser.add_argument("--file", type=str, required= True, help='path to CSV file')
args = parser.parse_args()

# Set the default text font size
plt.rc('font', size=18)
# Set the axes title font size
plt.rc('axes', titlesize=22)
# Set the axes labels font size
plt.rc('axes', labelsize=22)
# Set the font size for x tick labels
plt.rc('xtick', labelsize=18)
# Set the font size for y tick labels
plt.rc('ytick', labelsize=18)
# Set the legend font size
plt.rc('legend', fontsize=18)
# Set the font size of the figure title
plt.rc('figure', titlesize=24)


class Grating:

    def __init__(self, spatial_frequency, wavelength_air, RIM, n_film, n_substrate, film_thickness) -> None:
        # use microns for distance unit
        # from given parameters work out parameters for plotting DE
        # bragg angle
        self.spatial_frequency = spatial_frequency
        self.wavelength_air = wavelength_air
        self.RIM = RIM
        self.n_film = n_film
        self.film_thickness = film_thickness
        self.bragg_angle = np.arcsin((spatial_frequency*wavelength_air)/(2*n_film))
        self.phase_par = (np.pi*RIM*film_thickness)/(wavelength_air*np.cos(self.bragg_angle))



def main():
    
    # Load experimental data
    file = args.file
    df = pd.read_csv(file)
    angles = df.Angle
    diff_efficiencies = list((np.max(df.DE) - df.DE)*0.01)
    max_DE = max(diff_efficiencies)
    print(type(max_DE))
    index_maxDE = diff_efficiencies.index(max_DE)

    max_DE_angle = angles[index_maxDE]

    angles = [angle-max_DE_angle for angle in angles]


    grating1 = Grating(0.8, 0.532, 0.002, 1.5, 0, 50) 

    n_film =grating1.n_film
    wavelength_air = grating1.wavelength_air
    bragg_angle = grating1.bragg_angle
    #thickness = grating1.film_thickness

    def diffraction_efficiency(bragg_deviation, RIM, thickness):
        bragg_deviation = np.arcsin((np.sin(np.deg2rad(bragg_deviation)))/n_film)
        E = (bragg_deviation*2*np.pi*n_film*thickness*np.sin(bragg_angle))/(wavelength_air)
        v = (np.pi*RIM*thickness)/(wavelength_air*np.cos(bragg_angle))
        return (np.sin(np.sqrt((v)**2 + E**2)))**2/(1+(E**2/(v)**2))

        
    thickness = grating1.film_thickness
    def theoretical_diffraction_efficiency(bragg_deviation, v):
        bragg_deviation = np.arcsin((np.sin(np.deg2rad(bragg_deviation)))/n_film)
        E = (bragg_deviation*2*np.pi*n_film*thickness*np.sin(bragg_angle))/(wavelength_air)
        return (np.sin(np.sqrt((v)**2 + E**2)))**2/(1+(E**2/(v)**2))
       

    plt.scatter(angles, diff_efficiencies, s= 20, label='measured data')

    
    popt, pcov = curve_fit(diffraction_efficiency, angles, diff_efficiencies, p0= [0.01, 10], bounds=(0.000, [0.05, 50]))
    popt

    perr = np.sqrt(np.diag(pcov))
    perr_RIM = float(perr[0])
    perr_T = float(perr[1])

    # phase parameter determined by curve fitting
    RIM = float(popt[0])
    curve_fit_thickness = float(popt[1])
    v = (np.pi*popt*curve_fit_thickness)/(wavelength_air*np.cos(bragg_angle))  
    

    
    # , RIM = {0:.3g}'.format(RIM)
    DE_max = np.max(diff_efficiencies)

    # Analytically derived phase parameter
    v = np.arcsin(np.sqrt(DE_max))
    RIM = float((v*wavelength_air*np.cos(bragg_angle))/(np.pi*thickness))
    DE = [theoretical_diffraction_efficiency(angle, v) for angle in angles]
    print(len(angles))
    print(len(DE))


    #plt.plot(angles, diffraction_efficiency(angles, *popt), 'r-', label='Best-fit, RIM = {0:.3g},'.format(RIM) + ' T = {0:.3g}'.format(curve_fit_thickness)  + r'$\mu m$')
    plt.plot(angles, diffraction_efficiency(angles, *popt), 'r-', label='Best-fit, RIM = {0:.3g},'.format(RIM) + '+/- {0:.3g}'.format(perr_RIM) + ' T = {0:.3g}'.format(curve_fit_thickness) + '+/- {0:.3g}'.format(perr_T) + r'$\mu m$')
    # Plot DE vs delta_theta
    plt.plot(angles, DE, 'g-', label='Analytical, RIM = {0:.3g},'.format(RIM) + ' T = {0:.3g}'.format(thickness) + r'$\mu m$')
 
    #angles = np.arange(0,len(angles),1)
    #DE = np.arange(0,len(DE),1)
    spline = UnivariateSpline(angles, DE-np.max(DE)/2, s=0)
    r1, r2 = spline.roots() # find the roots
    #plt.hlines(np.max(DE)/2, r1, r2, alpha = 0.75)

    plt.title(r'DE vs $\Delta \theta$, Thickness $= 50 \mu m$')
    plt.xlabel(r'$\Delta \theta_{air} (\circ)$')
    plt.ylabel('DE (au)')

    plt.legend(loc='upper right')
    plt.show()
    print(r2 - r1)


    v = (np.pi*popt*thickness)/(wavelength_air*np.cos(bragg_angle))  
    print('Phase parameter', v)
    print('Bragg angle', bragg_angle)
    print('Wavelength air', wavelength_air)
    print('Thickness', thickness)
    RIM = (v*wavelength_air*np.cos(bragg_angle))/(np.pi*thickness)
    print('RIM', RIM)
    print('Delta theta', grating1.spatial_frequency*thickness)

    #print(perr_RIM)
    print(np.shape(pcov))
    print(pcov)
    print(perr)

if __name__ == '__main__':
    print(__doc__)
    main()
