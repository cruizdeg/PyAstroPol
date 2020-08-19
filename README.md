# PyAstroPol
Instrumental Polarization Analysis of Astronomical Optics

## Overview
The package has one simple goal : compute 4x4 Mueller matrix for the given optical system, and it is developed keeping astronomical optics in view.
It uses geomatric optics approach i.e., all the analysis uses strictly ray treatment. Users should keep in mind that this is NOT for optical design i.e., it is presumed that the user already knows the optical system that is to be analyzed.

The package imports following libraries, all of which are ubiquitous. They accompany any decent Python distribution hence this package should function with virtually no dependency issues __however__ it should be noted that it is developed with `Python3.6`.
```python
numpy
copy
random
matplotlib
mpl_toolkits
datetime
```

## Getting Started
The package need not be installed as the installation scheme is not final yet. Follow these steps to start using the package.  
1. Download the package and extract it to a directory of liking - `<User directory>/PyAstroPol.git`.  
2. Add `<User directory>/PyAstroPol.git` to the `PYTHONPATH`.  

[PyAstroPol/Examples/](https://github.com/hemanthpruthvi/PyAstroPol/tree/master/Examples) contains reveral examples files to demonstrate the applications of the package. They are provided in the form of `iPython` notebook and it is a good way to quick-start using the package. __They also function as the test cases__. 

As previously mentioned this is not a design software. Hence, one needs to know the optical system they wish to analyze. As per the framework of the optical system, there are thee types of objects :
1. Source  
2. Components  
3. Detector   

To devise a simple optical system, follow these steps.  
1. import the required package.
```python
from PyAstroPol import * 
```  
2. Create source, and optinally create a source for display. For analysis one can define a source with a lot of rays (say 10000), and for display one can define a source with fewer rays (say 10).  
```python
S_analysis = Source(10000, Clear=20)
S_display = Source(10, Clear=20)
```  
3. Create a component such as surface, lens etc., and position it. 
```python
L = UncoatedLens(50, Thick=10, R1=200, R2=-200)
L.translateOrigin(z=100.0)
```  
4. Create a detector and position it.
```python
D = Detector(50)
D.translateOrigin(z=200.0)
```  
5. Put them together to create the optical system.
```python
O_system = System(S_analysis, [L], D, dRays = S_display)
O_system.propagateRays()
```  
6. Display the optical system using matplotlib 3d axis.
```python
Fig = plt.figure()
Ax = Fig.add_subplot(111, projection='3d')
O_system.draw(Ax)
plt.show()
```  
7. Compute Mueller matrix and print it.
```python
MM, T = O_system.getSystemMuellerMatrix()
print(MM)
```  
## Directories

[PyAstroPol/PyAstroPol/](https://github.com/hemanthpruthvi/PyAstroPol/tree/master/PyAstroPol)  
It is the main directory containing all the source files. For more information on the classes check the documentation at `PyAstroPol/Docs/_build/html/PyAstroPol.html`.

[PyAstroPol/Materials/](https://github.com/hemanthpruthvi/PyAstroPol/tree/master/Materials)  
It has the refractive index data for different materials in a formatted manner. These files are loaded by the code to look-up the refractive index information of the given material. Users cas easily create such files using following easy steps.
1. Download wavelength vs refractive index file as `.csv` from popular refractive index database [RefractiveIndexInfo](https://refractiveindex.info/).
2. Rename the file to a material name which you can call e.g., for Aluminium the file name is `Al.csv`.
3. Copy the `.csv` file into `./Materials/` directory.
4. Format the material file using provided function i.e., `formatMaterialFile(MaterialName)` (without file extensions).

[PyAstroPol/Docs/](https://github.com/hemanthpruthvi/PyAstroPol/tree/master/Docs)  
It contains documentation related codes and files.  

## Conventions used in this package  
The most important aspect to remember while using the package is __the convention__, which is described below. 
### For astronomy : 
Positive X-axis : West  
Positive Y-axis : Zenith  
Positive Z-axis : North  
Positive Latitude : North  
Positive Hour Angle : West  
Positive Declination : North  
### For optics : 
Complex refractive index is __n-__*i*__k__ where __n__ and __k__ are positive real numbers.    
Jones vectors corresponding to positive Stokes-V are <img src="https://render.githubusercontent.com/render/math?math=\frac{1}{\sqrt 2} \begin{bmatrix} 1 \\ 0 \end{bmatrix}"> and <img src="https://render.githubusercontent.com/render/math?math=\frac{1}{\sqrt 2} \begin{bmatrix} 0 \\ -i \end{bmatrix}">. 

## TODO
1. Add polarizing elements such as birefringent elements, waveplates and polarizers.
2. Add feature to create and save coatings as files.
3. Add rectandular and elliptical apertures.