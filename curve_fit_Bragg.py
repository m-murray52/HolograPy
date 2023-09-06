import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np
import pandas as pd
from scipy.interpolate import UnivariateSpline

import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


class Grating:

    def __init__(self, spatial_frequency, wavelength_air, RIM, n_film, film_thickness) -> None:
        """A class object that describes the key characteristics of a transmissive holographic diffraction grating. You may think of this as creating a virtual representation of a physical grating."""
        # use microns for distance unit
        # from given parameters work out parameters for plotting DE
        # bragg angle
        self.spatial_frequency = spatial_frequency
        # probe wavelength
        self.wavelength_air = wavelength_air
        self.RIM = RIM
        self.n_film = n_film
        self.film_thickness = film_thickness
        self.bragg_angle = np.arcsin((spatial_frequency*wavelength_air)/(2*n_film))
        self.phase_par = (np.pi*RIM*film_thickness)/(wavelength_air*np.cos(self.bragg_angle))




# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Curve Fit", page_icon=":bar_chart:", layout="wide")

# ---- READ EXCEL ----
@st.cache(allow_output_mutation=True)
def get_data_from_csv(data):
    df = pd.read_csv(data)
    return df

def period(spatial_frequency):
    if spatial_frequency > 0:
        return 1/spatial_frequency
    else:
        pass

def main():
    st.title('Best-fit Kogelnik Equation to Bragg Diffraction Efficiency Data')    

    st.header('Data Uploader')
    data = st.file_uploader("Upload a .csv file")


    st.header('Input grating parameters')
    # spatial frequency
    sf = st.number_input('Enter recorded spatial frequency (l/um):', step= 0.001)
    

    # probe wavelength
    wavelength_air = st.number_input('Enter probe laser beam wavelength in air (nm):')
    wavelength_air_um = wavelength_air*0.001
    # n_flm
    n_film = st.number_input('Enter film refractive index:')

    # n_flm
    absorption_film = st.number_input('Enter film absorption:')

    # RIM
    absorption_modulation_guess = st.number_input('Enter an initial estimate of the refractive index modulation:')

    absorption_mod_upper_bound = st.number_input('Define upper limit for the refractive index modulation:')

    # Thickness estimate
    thickness = st.number_input('Enter an initial estimate of the grating thickness (um):')

    thickness_upper_bound = st.number_input('Define upper limit for the film thickness (um):')

    if sf and wavelength_air and n_film and absorption_modulation_guess  and thickness:

        if st.button('Curve fit'):
            #wavelength_air = wavelength_air/100
            bragg_angle = np.arcsin((sf*wavelength_air_um)/(2*n_film))
        # Load experimental data
            pd.set_option("display.max_rows", None, "display.max_columns", None)
            #df = get_data_from_excel(data)
            df = get_data_from_csv(data)
            angles = df.Angle

    # Invert measured 0-order DE
            max_DE = max(df.DE)
            #diff_efficiencies = list((max_DE - df.DE)*0.01)
            #df['1st-order DE'] = diff_efficiencies
            
    #fig = px.scatter(df, x="Angle", y="DE")
            fig1 = go.Figure()

    # Correct 0 order 
            df['0th-order DE'] = list((df.DE-(max_DE-100))*0.01)

            # Invert corrected 0-order DE to get 1st order
            max_DE = max(df['0th-order DE'])
            diff_efficiencies = list((1 - df['0th-order DE']))
            df['1st-order DE'] = diff_efficiencies
            
            st.dataframe(df)
            fig1.add_trace(go.Scatter(
            x=df['Angle'], y= df['0th-order DE'],
            name='0-th Order Diffraction Efficiency',
            mode='markers',
            marker_color='rgba(255, 0, 0, 1)'
            ))

            fig1.add_trace(go.Scatter(
            x=df['Angle'], y=df['1st-order DE'],
            name='1-st Order Diffraction Efficiency',
            marker_color='rgba(0, 255, 0, 1)'
            ))
    
    # Set options common to all traces with fig.update_traces
            fig1.update_traces(mode='markers', marker_line_width=1, marker_size=10)
            fig1.update_layout(title='Bragg curves: DE vs Bragg detuning angle',
                  yaxis_zeroline=False, xaxis_zeroline=False)

            st.header('Plot measured data')
            fig1.show()

    #fig = px.scatter(df, x="Angle", y=diff_efficiencies)
    #fig.show()
            st.plotly_chart(fig1)
    # Shift Bragg curve axis such that peak is at 0 degrees detuning angle
    # Find max DE
            max_DE = max(diff_efficiencies)

    # Find index of max DE
            index_maxDE = diff_efficiencies.index(max_DE)

    # Find measured angle of max DE
            max_DE_angle = angles[index_maxDE]

    # Correct measured angles by displacing by angle of max DE
            angles = [angle-max_DE_angle for angle in angles]
    #print(angles)

    # Define grating parameters (SF, probe wavelength, guessed RIM, material refractive index, designed thickness)
    #grating1 = Grating(0.8, 0.633, 0.01, 1.5, 16) 


   
    

    # Define function to be fitted to measured data. Takes corrected angles as independent variable.
            def diffraction_efficiency(bragg_deviation, absorption_modulation, thickness):
                """The function to be optimised using curve fitting by varying absorption modulation (RIM) and thickness (T), it is the Kogelnik equation for transmitted diffraction 
                efficiency of unlsanted absorption gratings"""
                bragg_deviation = np.arcsin((np.sin(np.deg2rad(bragg_deviation)))/n_film)
                E = (bragg_deviation*2*np.pi*n_film*thickness*np.sin(bragg_angle))/(wavelength_air_um)
                v = (absorption_modulation*thickness)/(2*np.cos(bragg_angle))
                return ( (np.cos(E))**2 + (np.sin(E)**2) )*( np.exp(-2*absorption_film*thickness/(np.cos(bragg_angle))) )*( np.sinh((v**2 + E**2))/(1-(E**2)/(v**2)) )

        
    
            def theoretical_diffraction_efficiency(bragg_deviation, v):
                """The function to be determined analytically using phase parameter based on peak DE. Assumes that actual thickness is the designed thickness."""
                bragg_deviation = np.arcsin((np.sin(np.deg2rad(bragg_deviation)))/n_film)
                E = (bragg_deviation*2*np.pi*n_film*thickness*np.sin(bragg_angle))/(wavelength_air_um)
                return ( (np.cos(E))**2 + (np.sin(E)**2) )*(np.sin(np.sqrt((v)**2 + E**2)))**2/(1+(E**2/(v)**2))
       
    
            def cook_klein(thickness):
                """Estimated Cook-Klein (Q) parameter, to be printed to commandline/terminal. Serves as a 'reality check'."""
                return (2*np.pi*wavelength_air_um*thickness)/(n_film*(period(sf))**2)

            def moharam_young(rim):
                """Estimated Moharam-Young (ro) parameter, to be printed to commandline/terminal. Serves as a 'reality check'."""
                return (wavelength_air_um**2)/((n_film*rim)*(period(sf))**2)
        
    #fig, ax = plt.subplots()

    # Create plot o
    #ax.plot(angles, diff_efficiencies, label='measured data')
    #st.pyplot(fig)
           # fig2 = go.Figure()

            #fig2.add_trace(go.Scatter(
            #x=angles, y= df['DE'],
            #name='0-th Order Diffraction Efficiency',
            #mode='markers',
            #marker_color='rgba(0, 0, 255, 1)'
            #))

    
        # Set options common to all traces with fig.update_traces
            #fig2.update_traces(mode='markers', marker_line_width=1, marker_size=10)
            #fig2.update_layout(title='Styled Scatter',
             #     yaxis_zeroline=False, xaxis_zeroline=False)


            #fig2.show()
            #st.plotly_chart(fig2)



    # Curve fitting: popt is a list containing the optimised parameters, in this case, RIM and thickness; pcov is the covariance matrix
    # pcov can be used to measure the standard deviation in the estimates of optimal parameters. 
            popt, pcov = curve_fit(diffraction_efficiency, angles, diff_efficiencies, p0= [absorption_modulation_guess, thickness], bounds=(0, [absorption_mod_upper_bound, thickness_upper_bound]))
            #popt
            
    #print(popt)

    # find square root of covariance matrix
            perr = np.sqrt(np.diag(pcov))
            #perr
    # assign standard deviations of RIM and thickness to variables
            perr_absorption_mod = float(perr[0])
            perr_T = float(perr[1])
            absorption_modulation = float(popt[0])
            curve_fit_thickness = float(popt[1])

            
#RIM = {0:.3g},'.format(RIM) + '+/- {0:.3g}'.format(perr_RIM) 
    # RIM and thickness determined by curve fitting
            

            fig2 = go.Figure()
            df['Best fit'] = diffraction_efficiency(angles, *popt)
            fig2.add_trace(go.Scatter(
            x=angles, y= df['Best fit'],
            name='Best fit',
            mode='markers',
            marker_color='rgba(0, 100, 255, 1)'
            ))

            fig2.add_trace(go.Scatter(
            x=angles, y=df['1st-order DE'],
            name='1-st Order Diffraction Efficiency',
            marker_color='rgba(0, 255, 0, 1)'
            ))
    # Set options common to all traces with fig.update_traces
            fig2.update_traces(mode='markers', marker_line_width=1, marker_size=10)
            fig2.update_layout(title='Diffraction efficiency vs Bragg Detuning Angle',
                  yaxis_zeroline=False, xaxis_zeroline=False)

            st.header('Plot Best fit')
            fig2.show()
            st.plotly_chart(fig2)
    # estimated phase parameter based on optimal RIM and T
            v = (absorption_modulation*thickness)/(2*np.cos(bragg_angle))

    # Print Q and ro parameters
            #print(cook_klein())
            #print(moharam_young())

            st.header('Best fit parameters')
            col1, col2 = st.columns(2)
            col1.metric("Absorption modulation", "{0:.3g}".format(absorption_modulation) + "+/- {0:.3g}".format(perr_absorption_mod))
            col2.metric("Thickness", "{0:.3g}".format(curve_fit_thickness) + "+/- {0:.3g}".format(perr_T) + ' um')
    #print(r2 - r1)
            st.header('Other parameters')
            col1, col2, col3 = st.columns(3)
            col1.metric("Phase parameter", '{0:.3g}'.format(v))
            


    #v = (np.pi*popt[0]*thickness)/(wavelength_air*np.cos(bragg_angle))  
    #print(diff_efficiencies)
    
    

if __name__ == '__main__':
    print(__doc__)
    main()
