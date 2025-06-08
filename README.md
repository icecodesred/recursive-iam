Title: Recursive IAM – Climate-Economic Simulation Tool


Description:
This project is an integrated assessment model (IAM) that simulates the interaction between economic growth, CO₂ emissions, global temperature, and climate damages. It uses scenario-based GDP and population projections (SSP1–SSP5) and applies Monte Carlo methods to capture uncertainty in climate and economic responses.

Main Features:
Modular design for emissions, temperature, and damage estimation
Scenario support for all five SSPs (Shared Socioeconomic Pathways)
Monte Carlo simulation with stochastic sampling of TCRE, damages, and intensity
Visualizations of global and continental GDP, emissions, temperature, and damages

How to Run:

Install required packages using pip install -r requirements.txt
Run the two preprocessing jupyter notebooks 
Run the main simulation with python main.py
Results will be saved in the outputs folder and visualized automatically

Data Requirements:

intensities.csv: Carbon and energy intensity data (can be generated via provided Jupyter notebook)
SSP GDP and population CSVs are required for full functionality; preprocessing scripts are provided

Reproducibility:
All code and data processing notebooks are included. SSP scenario data has to be downloaded manually, due to the site requirin log-in. Sample of SSP data is included, and is processed via the jupyter notebooks mentioned above for transparency.
