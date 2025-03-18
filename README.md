# Slip/No-Slip Estimator

**Version:** 1.01  
**Author:** Le Lu ([lulelaboratory@gmail.com](mailto:lulelaboratory@gmail.com)) 

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.15045269.svg)](https://doi.org/10.5281/zenodo.15045269)

## Overview

Slip/No-Slip Estimator is a Python-based GUI tool designed to help users determine the appropriate boundary condition (slip or no-slip) for CFD simulations based on molecular-scale friction parameters. Using inputs such as gap height, sliding speed, water viscosity, interfacial friction coefficient, critical shear rate, and an exponent, the tool calculates key parameters like shear rate, shear stress, baseline and effective slip lengths, and provides a recommendation along with suggested CFD boundary condition settings.

## Features

- **User-Friendly GUI:** Built with Tkinter for an intuitive experience.
- **Detailed Calculations:** Computes shear rate, shear stress, baseline slip length ![baseline](https://latex.codecogs.com/svg.latex?b_0=\frac{\mu}{\lambda), and effective slip length ![effective](https://latex.codecogs.com/svg.latex?b_{\text{eff}}=b_0\left[1+\left(\frac{\gamma}{\gamma_c}\right)^m\right]).
- **Decision Criterion:** Evaluates the slip ratio ![Slip Ratio](https://latex.codecogs.com/svg.latex?\frac{b_{\text{eff}}}{h}) to recommend either a no-slip or slip boundary condition.
- **CFD Boundary Condition Suggestion:** Provides a practical suggestion for setting up CFD simulations based on the computed values.
- **Methodology Display:** Shows formal mathematical equations and detailed methodology (using MathJax) in a browser window.
- **Export Functionality:** Allows exporting of calculation results to a text file.
- **About Dialog:** Displays version, author, and license information.

## Requirements

- **Python 3.x**
- **Tkinter:** Typically included with Python.
- **Standard Libraries:** `datetime`, `os`, `tempfile`, `webbrowser`, etc.
- **Internet Connection:** Required for loading MathJax when viewing the methodology page.

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/slip-noslip-estimator.git

2. **Navigate to the Project Directory:**

   ```bash
   python cd slip-noslip-estimator.py


3. **Run the Application:**

   ```bash
   python slip_no_slip_estimator.py

## Usage
Launch the Application.
Enter Input Parameters:
- Gap Height (nm)
- Sliding Speed (m/s)
- Water Viscosity (Pa·s)
- Interfacial Friction (Pa·s/m)
- Critical Shear Rate (1/s)
- Exponent (m)

Click "Calculate": The tool computes the shear rate, shear stress, baseline and effective slip lengths, and the slip ratio.

View Recommendation:
- No-slip Condition: (Displayed in blue) if ![No-slip](https://latex.codecogs.com/svg.latex?b_{\text{eff}}/h%20<%200.01).
- Slip Condition: (Displayed in red) if ![Slip](https://latex.codecogs.com/svg.latex?b_{\text{eff}}/h%20\ge%200.01).

CFD Suggestion: A suggested boundary condition for your CFD simulation is provided.

View Methodology: Use the Help > Methodology menu option to see detailed mathematical formulations and references.

Export Results: Use the File > Export Results menu option to save the results as a text file.

Methodology
The tool is based on the following key equations:

**Shear Rate:**

<p align="center">
  <img src="https://latex.codecogs.com/svg.latex?\gamma=\frac{U}{h}" alt="Shear Rate">
</p>

**Shear Stress:**

<p align="center">
  <img src="https://latex.codecogs.com/svg.latex?\tau=\mu\cdot\gamma" alt="Shear Stress">
</p>

**Baseline Slip Length:**

<p align="center">
  <img src="https://latex.codecogs.com/svg.latex?b_0=\frac{\mu}{\lambda}" alt="Baseline Slip Length">
</p>

**Effective Slip Length:**

<p align="center">
  <img src="https://latex.codecogs.com/svg.latex?b_{\text{eff}}=b_0\left[1+\left(\frac{\gamma}{\gamma_c}\right)^m\right]" alt="Effective Slip Length">
</p>

**Slip Ratio (Decision Criterion):**

![Slip Ratio](https://latex.codecogs.com/svg.latex?\text{Slip%20Ratio}=\frac{b_{\text{eff}}}{h})

- If ![No-slip condition](https://latex.codecogs.com/svg.latex?\frac{b_{\text{eff}}}{h}%20<%200.01), assume a no-slip boundary condition.
- If ![Slip condition](https://latex.codecogs.com/svg.latex?\frac{b_{\text{eff}}}{h}%20\ge%200.01), a slip condition is recommended.

For a detailed explanation with formatted equations and references, open the Methodology page from the Help menu.

## References
1. Thompson, P. A., and S. M. Troian. "A General Boundary Condition for Liquid Flow at Solid Surfaces." *Nature*, vol. 389, no. 6649, 1997, pp. 360–362.
2. Neto, C., D. R. Evans, E. Bonaccurso, H.-J. Butt, and V. S. J. Craig. "Fluid Slip in Diverse Regimes: A Review of Experimental Studies." *Reports on Progress in Physics*, vol. 68, no. 12, 2005, pp. 2859–2897.
3. Bocquet, L., and J.-L. Barrat. "Hydrodynamic Boundary Conditions, Correlation between Friction and Slip at a Fluid/Solid Interface." *Soft Matter*, vol. 3, no. 4, 2007, pp. 685–693.


