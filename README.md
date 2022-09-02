[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://m-murray52-holograpy-curve-fit-bragg-c6o0kn.streamlitapp.com)

# HolograPy


This is a relatively simple tool for fitting theoretical models of diffractive optical elements to measured Bragg angular selevtivity data. It has been developed as part of the LIGHTSCAPE project at the Centre for Industrial Engineering Optics (IEO), funded by Science Foundation Ireland (SFI) at the Technological University Dublin (TUD).  In its current state it fits the Kogelnik Coupled Wave Analysis (KCWA) model of diffraction efficiency of transmissive volume phase gratings to measured diffraction efficiencies, measured as a function of Bragg detuning angle. It finds the optimal fit of the model to the data by varying two model parameters:

  1. Grating thickness (T)
  2. Refractive index modulation (RIM or  Δ n)

Before explaining how to use the tool, let's briefly review some theory.

## Theory 

The KCWA model describes the diffraction efficiency (η) of a beam of light, usually a single wavelength laser beam, transmitted through a holographic diffraction gration. It is the ratio of the output beam intensity to the input beam intensity. It is written below as:

![equation](https://latex.codecogs.com/svg.latex?%5Ceta%20=%20%5Cfrac%7B%5Csin%5E%7B2%7D(%5Csqrt%7B%5Cnu%5E%7B2%7D+%20%5Cxi%5E%7B2%7D%7D)%7D%7B1+%5Cfrac%7B%5Cxi%5E%7B2%7D%7D%7B%5Cnu%5E%7B2%7D%7D%7D)

where ν is the phase parameter, which determines the maximum efficiency of the grating, and ξ is the off-Bragg parameter, describing the deviation from Bragg conditions. These are described, respectively, as follows: 

![equation](https://latex.codecogs.com/svg.latex?%5Cnu%20=%20%5Cfrac%7B%5Cpi%20%5CDelta%20n%20T%7D%7B%5Clambda_%7Bair%7D%20%5Ccos(%5Ctheta_%7BBragg%7D)%7D)
 
 and 
 
 ![equation](https://latex.codecogs.com/svg.latex?%5Cxi%20=%20%5Cfrac%7B2%20%5Cpi%20%5CDelta%20%5Ctheta_%7BBragg%7D%20n_%7Bfilm%7D%20T%20%5Csin(%5Ctheta_%7BBragg%7D)%7D%7B%5Clambda_%7Bair%7D%20%7D)
 
 where ![symbol](https://latex.codecogs.com/svg.latex?%5Ctheta_%7BBragg%7D) is the Bragg angle of the probing beam, ![symbol](https://latex.codecogs.com/svg.latex?%5CDelta%20%5Ctheta_%7BBragg%7D) is the angular deviation or detuning from the Bragg angle, ![symbol](https://latex.codecogs.com/svg.latex?%5Clambda_%7Bair%7D) is the wavelength of the probing beam in air, and ![symbol](https://latex.codecogs.com/svg.latex?n_%7Bfilm%7D) is the average refractive index of the grating material. 
 
For an ideal grating ν= 2/π and η = 100% when ![symbol](https://latex.codecogs.com/svg.latex?%5CDelta%20%5Ctheta_%7BBragg%7D) = 0. An example Bragg curve of an ideal grating is shown below, this is for a specific thickness and average refractive index.

![alt text](https://github.com/m-murray52/HolograPy/blob/main/example_bragg_curve_for_README.png)

In the real world however, the peak is usually less than 100% and the shape of the curve can vary. In addition, during the recording process, the thickness of the material may shrink. So any models which do not account for this change of thickness, and assume that the thickness is the designed thickness, will always show a significant deviation from the modelled data. 

By curve fitting, the optimal parameters of the KWCA model are determined such that the KWCA fits the modelled data as closely as possible. How this is implemented is described below. 

# How to use the app

Simply click on the streamlit badge, upload a .xlsx file formatted as shown below, enter grating parameters (including estimates for thickness and refractive index modulate), and click the 'Curve fit' button. 

![grating_class_instance](https://user-images.githubusercontent.com/87316384/175013469-39d11b19-d262-4efc-b9cd-ae257ebd7994.png)



