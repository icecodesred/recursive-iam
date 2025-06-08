import pandas as pd

class IAMSimulation:
    def __init__(self, scenario_df, emissions_model, climate_model, damage_function):
        self.data = scenario_df
        self.emissions_model = emissions_model
        self.climate_model = climate_model
        self.damage_function = damage_function
        self.results = {}
        self.country_trajectories = []

    def run(self, start_year, end_year):
        years = list(range(start_year, end_year + 1))
        countries = self.data['Region'].unique()
        df = self.data.copy()

        # Initialize GDP baseline for start year
        for country in countries:
            country_mask = df['Region'] == country
            df.loc[country_mask & (df['Year'] == start_year), 'GDP_baseline'] = \
                df.loc[country_mask & (df['Year'] == start_year), 'GDP']

        # Main simulation loop
        for year in years:
            temp = self.climate_model.temperature
            damage_frac = max(0.0, min(1.0, self.damage_function.damage_fraction(temp)))

            year_mask = df['Year'] == year
            df.loc[year_mask, 'DamageFrac'] = damage_frac
            df.loc[year_mask, 'GDP_damaged'] = df.loc[year_mask, 'GDP_baseline'] * (1 - damage_frac)

            world_gdp_baseline = df.loc[year_mask, 'GDP_baseline'].sum()
            world_gdp_damaged = df.loc[year_mask, 'GDP_damaged'].sum()
            emissions = max(0.0, self.emissions_model.compute_emissions(df.loc[year_mask]))
            temperature = self.climate_model.update_temperature(emissions)

            df.loc[year_mask, 'GlobalTemp'] = temperature
            df.loc[year_mask, 'Emissions'] = emissions

            self.results[year] = {
                'Year': year,
                'GDP_baseline': world_gdp_baseline,
                'GDP': world_gdp_damaged,
                'Temp': temperature,
                'Emissions': emissions,
                'Damages': world_gdp_baseline * damage_frac
            }

            # Advance GDP baseline for next year
            if year < end_year:
                next_year = year + 1
                for country in countries:
                    mask_current = (df['Region'] == country) & (df['Year'] == year)
                    mask_next = (df['Region'] == country) & (df['Year'] == next_year)
                    growth = df.loc[mask_next, 'GrowthRate'].values
                    gdp = df.loc[mask_current, 'GDP_damaged'].values
                    if len(growth) > 0 and len(gdp) > 0:
                        df.loc[mask_next, 'GDP_baseline'] = gdp[0] * (1 + growth[0])

        self.country_trajectories = df
        return self.results

    def export_country_data(self, filepath="outputs/country_trajectories.csv"):
        cols = ["Year", "Region", "GDP_baseline", "GDP_damaged", "DamageFrac", "GlobalTemp", "Emissions"]
        self.country_trajectories[cols].to_csv(filepath, index=False)

    def export_global_summary(self, filepath="outputs/global_summary.csv"):
        summary_df = pd.DataFrame.from_dict(self.results, orient='index')
        summary_df.to_csv(filepath, index=False)
