import pandas as pd

def load_and_melt(filepath, value_name):
    df = pd.read_csv(filepath)
    meta_cols = ['Scenario', 'Region']
    year_cols = [col for col in df.columns if col not in meta_cols]

    df_long = df.melt(id_vars=meta_cols, 
                      value_vars=year_cols, 
                      var_name="Year", 
                      value_name=value_name)
    df_long['Year'] = df_long['Year'].astype(int)
    return df_long

def load_scenario_data(ssp_id):
    gdp = load_and_melt(f"data/ssp{ssp_id}_gdp.csv", "GDP")
    pop = load_and_melt(f"data/ssp{ssp_id}_pop.csv", "Population")
    growth = load_and_melt(f"data/ssp{ssp_id}_growth.csv", "GrowthRate")

    state = gdp.merge(pop, on=["Scenario", "Region", "Year"])
    state = state.merge(growth, on=["Scenario", "Region", "Year"])
    state['GDP_per_capita'] = (state['GDP'] * 1e9) / (state['Population'] * 1e6)

    # Merge with continent data
    continent_map = pd.read_csv("data/country_continent_map.csv")
    state = state.merge(continent_map, left_on="Region", right_on="Country")
    return state