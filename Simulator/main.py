from loaders.scenario_loader import load_scenario_data
from loaders.intensity_loader import load_intensities
from models.damage_functions import NordhausQuadratic
from models.emissions import EmissionsEstimator
from models.climate_feedback import TCREClimateModel
from models.simulation import IAMSimulation
from utils.plotting import (
    plot_results,
    plot_monte_carlo_summary,
    plot_emissions_by_continent_interactive,
    plot_gdp_by_continent,
    export_gdp_combined_by_continent,
    plot_ssp_comparison
)
from monte_carlo import run_monte_carlo
import pandas as pd

intensity_df = load_intensities()
ssp_results = []
run_monte_for_ssp = 3 #Adjust Monte Carlo runs for desired scenario here 

# iterating through all selected SSP scenarios 
for ssp_id in range(1, 6):
    print(f"\nRunning simulation for SSP{ssp_id}")
    scenario_df = load_scenario_data(ssp_id)

    damage_function = NordhausQuadratic()
    emissions_model = EmissionsEstimator(intensity_df)
    climate_model = TCREClimateModel()

    sim = IAMSimulation(scenario_df, emissions_model, climate_model, damage_function)
    results = sim.run(2020, 2100)

    #result storage
    for year, data in results.items():
        data['Year'] = year
        data['SSP'] = f'SSP{ssp_id}'
        ssp_results.append(data)

    #comparison
    if ssp_id == run_monte_for_ssp:
        print(f"\nPlotting and exporting results for SSP{ssp_id}")
        plot_results(results)
        plot_gdp_by_continent(sim.country_trajectories)
        export_gdp_combined_by_continent(sim.country_trajectories)
        export_emissions_charts(sim.country_trajectories)

        sim.export_country_data(f"outputs/country_trajectories_ssp{ssp_id}.csv")
        sim.export_global_summary(f"outputs/global_summary_ssp{ssp_id}.csv")

#plotting results
df_ssps = pd.DataFrame(ssp_results)
plot_ssp_comparison(df_ssps)

#Monte Carlo run 
print(f"\nRunning Monte Carlo for SSP{run_monte_for_ssp}")
run_monte_carlo(n_runs=50, ssp_id=run_monte_for_ssp)

print("\nPlotting Monte Carlo summary...")
example_results = df_ssps[df_ssps['SSP'] == f'SSP{run_monte_for_ssp}'].set_index('Year').to_dict(orient='index')
plot_monte_carlo_summary(main_results=example_results)
