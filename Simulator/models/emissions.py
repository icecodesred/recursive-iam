class EmissionsEstimator:
    def __init__(self, intensity_df):
        self.intensity_df = intensity_df

    def compute_emissions(self, df_year):
        # Merge year-country data with year-continent intensity projections
        df = df_year.merge(self.intensity_df,
                           on=['Year', 'Continent'],
                           how='left')

        # Rename for clarity
        df = df.rename(columns={
            'Primary energy consumption per GDP (kWh/$)': 'energy_intensity',
            'Annual CO₂ emissions per unit energy (kg per kilowatt-hour)': 'carbon_intensity'
        })

        # Check for missing intensity data
        if df[['energy_intensity', 'carbon_intensity']].isnull().any().any():
            missing = df[df[['energy_intensity', 'carbon_intensity']].isnull().any(axis=1)]
            raise ValueError(f"Missing intensity data for:\n{missing[['Region', 'Year', 'Continent']]}")

        # Compute emissions per country
        df['Emissions'] = df['GDP_damaged'] * df['energy_intensity'] * df['carbon_intensity']/1000
        return df['Emissions'].sum()
