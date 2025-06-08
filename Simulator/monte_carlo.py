import numpy as np
import pandas as pd
from loaders.scenario_loader import load_scenario_data
from loaders.intensity_loader import load_intensities
from models.damage_functions import NordhausQuadratic
from models.emissions import EmissionsEstimator
from models.climate_feedback import TCREClimateModel
from models.simulation import IAMSimulation
from scipy.stats import lognorm

#select TCRE distribution and energy and carbon intensity multipliers
def run_monte_carlo(n_runs=10, ssp_id=5, start_year=2020, end_year=2100, 
                    tcre_mean=1.5, tcre_upper=3.0, tcre_lower=1.0, 
                    ei_multiplier=1, ci_multiplier=1):
    results_list = []

    #computing lognormal distribution parameters for TCRE
    tcre_sigma = (np.log(tcre_upper) - np.log(tcre_lower)) / (2 * 1.645)
    tcre_mu = np.log(tcre_mean) - 0.5 * tcre_sigma**2

    scenario_df = load_scenario_data(ssp_id)
    intensity_df = load_intensities()

    for i in range(n_runs):
        tcre_sample = np.random.lognormal(mean=tcre_mu, sigma=tcre_sigma) / 1000  #convert to gigatons

        if i == 0:
            print(f"Example TCRE samples: {[np.random.lognormal(tcre_mu, tcre_sigma) for _ in range(5)]}")

        damage_coeff = np.random.normal(loc=0.00267, scale=0.0003) #dice damage calibration

        intensity_df_perturbed = intensity_df.copy()
        intensity_df_perturbed['energy_intensity'] *= np.random.normal(loc=ei_multiplier, scale=0.01, size=len(intensity_df))
        intensity_df_perturbed['carbon_intensity'] *= np.random.normal(loc=ci_multiplier, scale=0.01, size=len(intensity_df))

        damage_function = NordhausQuadratic(coefficient=damage_coeff)
        emissions_model = EmissionsEstimator(intensity_df_perturbed)
        climate_model = TCREClimateModel(tcre=tcre_sample)

        sim = IAMSimulation(scenario_df, emissions_model, climate_model, damage_function)
        result = sim.run(start_year, end_year)

        for year, data in result.items():
            row = {"Run": i, "Year": year}
            row.update(data)
            results_list.append(row)

    df_results = pd.DataFrame(results_list)
    df_results.to_csv("outputs/monte_carlo_results.csv", index=False) #export to csv
    return df_results
