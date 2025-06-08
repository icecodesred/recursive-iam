import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def plot_results(results):
    years = list(results.keys())
    gdp_damaged = [results[year]['GDP'] for year in years]
    gdp_baseline = [results[year]['GDP_baseline'] for year in years]
    temp = [results[year]['Temp'] for year in years]
    emissions = [results[year]['Emissions'] for year in years]
    damages = [results[year]['Damages'] for year in years]

    fig, axs = plt.subplots(2, 2, figsize=(12, 8))

    axs[0, 0].plot(years, gdp_baseline, label="Baseline GDP", linestyle='--')
    axs[0, 0].plot(years, gdp_damaged, label="Damaged GDP")
    axs[0, 0].set_title("Global GDP")
    axs[0, 0].legend()

    axs[0, 1].plot(years, temp)
    axs[0, 1].set_title("Global Mean Temperature")

    axs[1, 0].plot(years, emissions)
    axs[1, 0].set_title("Annual CO2 Emissions (GtCO2)")

    axs[1, 1].plot(years, damages)
    axs[1, 1].set_title("Climate Damages")

    for ax in axs.flat:
        ax.set_xlabel("Year")
        ax.grid(True)

    plt.tight_layout()
    plt.show()


def plot_gdp_by_continent(df):
    df_grouped = df.groupby(['Year', 'Continent'])[['GDP_baseline', 'GDP_damaged']].sum().reset_index()

    fig = px.line(df_grouped, x='Year', y='GDP_baseline', color='Continent',
                  title='Baseline GDP by Continent (Billion USD)',
                  labels={'GDP_baseline': 'Baseline GDP'})
    fig.update_layout(template="plotly_white")
    fig.show()

    fig2 = px.line(df_grouped, x='Year', y='GDP_damaged', color='Continent',
                   title='Damaged GDP by Continent (Billion USD)',
                   labels={'GDP_damaged': 'Damaged GDP'})
    fig2.update_layout(template="plotly_white")
    fig2.show()


def plot_monte_carlo_summary(filepath="outputs/monte_carlo_results.csv", main_results=None):
    df = pd.read_csv(filepath)
    grouped = df.groupby("Year")
    years = grouped.size().index

    fig, axs = plt.subplots(2, 2, figsize=(12, 8))

    variables = ["GDP", "Temp", "Emissions", "Damages"]
    titles = ["GDP", "Temperature", "Emissions", "Damages"]

    for ax, var, title in zip(axs.flat, variables, titles):
        mean = grouped[var].mean()
        p5 = grouped[var].quantile(0.05)
        p95 = grouped[var].quantile(0.95)

        ax.plot(years, mean, label="Monte Carlo Mean")
        ax.fill_between(years, p5, p95, color="gray", alpha=0.3, label="5–95% CI")

       
        if main_results:
            main_vals = [main_results[year][var] for year in years if year in main_results]
            ax.plot(years, main_vals, linestyle="--", color="black", label="Main Run")

        ax.set_title(f"Monte Carlo: {title}")
        ax.set_xlabel("Year")
        ax.grid(True)
        ax.legend()

    plt.tight_layout()
    plt.show()


def plot_emissions_by_continent_interactive(df):
    df_continent = df.groupby(['Year', 'Continent'])['Emissions'].sum().reset_index()

    fig = px.line(df_continent, x='Year', y='Emissions', color='Continent',
                  title='Emissions by Continent (GtCO₂)',
                  labels={'Emissions': 'GtCO₂'})
    fig.update_layout(template="plotly_white")
    fig.show()

def export_gdp_combined_by_continent(df, output_path="outputs/gdp_combined_by_continent.html"):
    df_grouped = df.groupby(['Year', 'Continent'])[['GDP_baseline', 'GDP_damaged']].sum().reset_index()

    fig = go.Figure()

    for continent in df_grouped['Continent'].unique():
        sub = df_grouped[df_grouped['Continent'] == continent]

        # Damaged GDP: solid line
        fig.add_trace(go.Scatter(
            x=sub['Year'], y=sub['GDP_damaged'],
            mode='lines', name=f'{continent} - Damaged',
            line=dict(dash='solid')
        ))

        # Baseline GDP: dashed line
        fig.add_trace(go.Scatter(
            x=sub['Year'], y=sub['GDP_baseline'],
            mode='lines', name=f'{continent} - Baseline',
            line=dict(dash='dash')
        ))

    fig.update_layout(
        title="GDP by Continent: Damaged (Solid) vs Baseline (Dashed)",
        xaxis_title="Year",
        yaxis_title="GDP (Billion USD)",
        template="plotly_white",
        height=600
    )

    fig.write_html(output_path)

def plot_ssp_comparison(df):
    import matplotlib.pyplot as plt
    import seaborn as sns

    metrics = ['GDP', 'Temp', 'Emissions', 'Damages']
    titles = ['Global GDP', 'Global Temperature (°C)', 'Annual CO₂ Emissions (GtCO₂)', 'Climate Damages (B USD)']
    colors = sns.color_palette("tab10", 5)
    fig, axs = plt.subplots(2, 2, figsize=(14, 10))

    for ax, metric, title in zip(axs.flat, metrics, titles):
        for i, ssp in enumerate(sorted(df['SSP'].unique())):
            df_ssp = df[df['SSP'] == ssp]
            ax.plot(df_ssp['Year'], df_ssp[metric], label=ssp, color=colors[i])
        ax.set_title(title)
        ax.set_xlabel("Year")
        ax.grid(True)

    handles, labels = axs[0, 0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=5)
    plt.tight_layout(rect=[0, 0.05, 1, 1])
    plt.show()
