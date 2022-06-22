# HolograPy

This is a relatively simple tool for fitting theoretical models of diffractive optical elements to measured data. It has been developed as part of the LIGHTSCAPE project at the Centre for Industrial Engineering Optics (IEO), funded by Science Foundation Ireland (SFI) at the Technological University Dublin (TUD).  In its current state it fits the Kogelnik Coupled Wave Analysis (KCWA) model of diffraction efficiency of transmissive volume phase gratings to measured diffraction efficiencies, measured as a function of Bragg detuning angle. It finds the optimal fit of the model to the data by varying two model parameters:

  1. Grating thickness (T)
  2. Refractive index modulation (RIM or  Δ n)

## Required software libraries

1. Python 3
2. matplotlib
3. scipy
4. numpy
5. pandas
6. argparse

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

## How to use this tool 

Simply clone the repository and run `python3 curve_fit_Bragg.py --file=<path to CSV file>`. In the program's present state, you will have to provide a CSV file of Bragg Curve data which fulfills a specific format as shown below:

![alt text](https://github.com/m-murray52/HolograPy/blob/main/csv_format.png)

The CSV file can be easily formatted and edited in Excel:

![alt text](https://github.com/m-murray52/HolograPy/blob/main/csv_format_excel.png)

If the spreadsheet in which the data is stored is not formatted correctly, reorganise it as shown below and save with a .csv extension:

https://user-images.githubusercontent.com/87316384/174852804-885207cc-09b1-4fe5-82b5-8568f8fde1e0.mp4

A demo of the code being ran from a terminal/commadline is shown below:



https://user-images.githubusercontent.com/87316384/174856211-bcbdc024-8d33-4bf7-af13-d6799a9e913a.mp4

Note that the above example is demonstrated on Linux, on Mac the syntax is the same. On Windows, in the commandline or PowerShell, replace the forward slashes, "/", with back slashes, "\\". In all cases make sure to be in the working directory of `curve_fit_Bragg.py` and make sure that the `file` commandline argument points to the location of the CSV file you wish to analyse. So simply run the code as shown from the correct directory, point to the file to be analysed, and press `Enter` on your keyboard.

### Refining Best-fits

To obtain the best results the user has to modify some parameters in the code. Currently, this has to be done by opening the `curve_fit_Bragg.py` code in a text editor and changing some variables. However, in the future it is hoped that this can be done through a graphical user interface (GUI). There are two sets of parameters the user must modify to their needs:

1. Grating parameters
2. Initial estimates of optimal values for T and Δ n.

How to adapt these is discussed below.

#### Defining grating parameters
A grating class is defined below:

![grating_class](https://user-images.githubusercontent.com/87316384/175011529-b24bdf54-ede9-47bf-a2f8-642ddf468245.png)

Note, that the line numbers do not correspond to the numbers in the code, the numbers are only for illustrative purposes. As can be seen on line 3 `def __init__()` may take the following arguments for the following parameters when ever and instance of the class is defined (i.e., whenever a grating is defined):

1. spatial frequency, `spatial_frequency`
2. probe wavelength (in air), `wavelength_air` 
3. `RIM` (Δ n), an estimated RIM
4. average refractive index of the recording medium (`n_film')
5. The refractive index of the substrate on which the recording medium is placed, `n_substrate`- currently this is not in use 
6. Grating or film (medium) thickness, `film_thickness`

These arguments are then used to define attributes of the class instance in lines 8-14, including an initial estimate of the phase parameter. 

The following code creates an instance of the grating class with specific grating parameters, in other words it creates a specific version of the class following the blueprints set out in the class definition:

![grating_class_instance](https://user-images.githubusercontent.com/87316384/175013469-39d11b19-d262-4efc-b9cd-ae257ebd7994.png)

Here, a grating called `grating1` has be defined as `Grating` (or class instance). As attributes (or grating charateristics), it has the follow characteristics:

| Characteristics/class attribute  | Value |
| ------------- | ------------- |
| `spatial_frequency`  | 0.8  |
| `wavelength_air`  | 0.532  |
| `RIM`  | 0.002  |
| `n_film`  | 1.5 |
| `n_substrate`  | 0 |
| `film_thickness`  | 50 |

where units for `spatial_frequency`, `wavelengt_air`, and `film_thickness` are all in microns. `n_subtrate` is 0 for no particular reason other than that this attribute is currently used nowhere else in the code. This may change in the future and this document will be updated accordingly. 

## Optimising Best-fit

The workhorse of this code is shown below:
![optimisation_params](https://user-images.githubusercontent.com/87316384/175016042-65f7a878-0f0c-4219-a5e0-2c9f72c3f6de.png)

The code on line one is what executes the curve-fitting algorithm. The arguments provides are as follows (note that the order of appearance is crucial):

| Argument | Value |
| ------------- | ------------- |
| Function to be fit  | Kogelnik equation, `diffraction_efficiency`  |
| measured xdata | measured off-Bragg angles, `angles`  |
| measured ydata  | measured diffraction efficiencies, `diff_efficiencies`  |
| Initial guess of values of RIM and T, respectively, in arra form  | `p0 = [0.01, 10]`, where 0.01 is an initial guess for RIM and 10 is an initial guess for T in microns |
| bounds, lower and upper bounds on possible parameters  | Lower bound for both parameters set at 0 and array defining upper bounds of both parameters as follows: `bounds = (0.000, [0.05, 50])`|

The output optimised parameters are then stored in the array `popt`. The corresponding covariance matrix is stored in the array `pcov`. The square root of the diagonal values of `pcov` provide estimates of the standard deviations of the optimised parameters. Line 4 outputs an array containing the standard deviations of the optimised RIM and T respectively. These are accessed an stored as variables `perr_RIM` and `perr_T` on lines 5 and 6. Thus, providing a method of quantifiying the precision of best-fit estimates.  

Improved accuracy of optimisation will be obtained by choosing the best initial guess for the parameters and the appropriate bounds. The user also has the option of using no bounds or initial guesses. 
I have only discussed some of the arguments available with the `curve_fit()`, method. For more information please visit the[SciPy documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html).


## Future Work

I hope to eventually develop a graphical user interface GUI for running the code, either locally, on a user's desktop, or in a web browser as a web app.

## Want to learn more about general curve fitting in Python?

For a general introduction to curve fitting equations to data using Python, I suggest looking at this excellent [article](https://towardsdatascience.com/basic-curve-fitting-of-scientific-data-with-python-9592244a2509) by Naveen Venkatesan on Towards Data Science. There you will learn the basic principles and how to adapt the code to your specific equation and needs. Also take a look at the [official documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html) on the SciPy website, this is especially important if you wish to see how the code works 'under the hood' as it provides links to source code. There are also plenty of other free tutorials available in the form of blog posts and videos. 
