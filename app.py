import os
import pandas as pd
import plotly.express as px
import plotly.io as pio
from flask import Flask, render_template

app = Flask(__name__)

# Define base directory and data path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data")

# Load datasets
suicide_rates_df = pd.read_csv(os.path.join(DATA_PATH, "suicide_rates.csv")).dropna()
age_std_suicide_rates_df = pd.read_csv(os.path.join(DATA_PATH, "age_std_suicide_rates.csv")).dropna()

# Sample data if too large
if len(suicide_rates_df) > 500:
    suicide_rates_df = suicide_rates_df.sample(n=500, random_state=42)

if len(age_std_suicide_rates_df) > 500:
    age_std_suicide_rates_df = age_std_suicide_rates_df.sample(n=500, random_state=42)

@app.route("/")
def index():
    graphs = []

    # 1. First Bar Chart: Global Suicide Rates
    if "CountryName" in suicide_rates_df.columns:
        country_avg = suicide_rates_df.groupby("CountryName")["DeathRatePer100K"].mean().reset_index()
        country_avg = country_avg.sort_values(by="DeathRatePer100K", ascending=False).head(15)
        
        fig1 = px.bar(
            country_avg, x="CountryName", y="DeathRatePer100K",
            title="Top 15 Countries with Highest Suicide Rates",
            labels={"DeathRatePer100K": "Suicide Rate per 100K"},
            color="CountryName",
            text_auto=True,
            color_discrete_sequence=px.colors.qualitative.Vivid
        )
        graphs.append(("Global Suicide Trends", "Top countries with highest suicide rates", pio.to_html(fig1, full_html=False)))

    # 2. Second Bar Graph: Top 10 Countries
    avg_suicide_by_country = suicide_rates_df.groupby("CountryName")["DeathRatePer100K"].mean().reset_index()
    fig2 = px.bar(
        avg_suicide_by_country.sort_values("DeathRatePer100K", ascending=False).head(10),
        x="CountryName", y="DeathRatePer100K", color="CountryName",
        title="Top 10 Countries by Suicide Rate",
        labels={"DeathRatePer100K": "Average Suicide Rate per 100K"}
    )
    graphs.append(("Top Countries Suicide Rate", "Top 10 countries with the highest suicide rates", pio.to_html(fig2, full_html=False)))

    # 3. Pie Chart: Suicide Rates by Continent
    if "RegionName" in suicide_rates_df.columns:
        region_avg = suicide_rates_df.groupby("RegionName")["DeathRatePer100K"].mean().reset_index()
        fig3 = px.pie(
            region_avg, names="RegionName", values="DeathRatePer100K",
            title="Suicide Rates by Continent",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        graphs.append(("Suicide Rates by Continent", "Percentage of suicide rates by continent", pio.to_html(fig3, full_html=False)))

    # 4. Line Graph: Suicide Trends by Age Group
    if "Generation" in age_std_suicide_rates_df.columns:
        fig4 = px.line(
            age_std_suicide_rates_df, x="Year", y="DeathRatePer100K", color="Generation",
            title="Suicide Rates by Age Group Over Time",
            labels={"DeathRatePer100K": "Suicide Rate per 100K"}
        )
        graphs.append(("Suicide by Age Group", "Trends of suicide rates for different age groups", pio.to_html(fig4, full_html=False)))

    # 5. Bar Graph: Suicide Rates by Gender and Region
    if "Sex" in age_std_suicide_rates_df.columns and "RegionName" in age_std_suicide_rates_df.columns:
        fig5 = px.bar(
            age_std_suicide_rates_df, x="Sex", y="DeathRatePer100K", color="RegionName",
            title="Suicide Rates by Gender and Region",
            barmode="group",
            labels={"DeathRatePer100K": "Suicide Rate per 100K"}
        )
        graphs.append(("Suicide by Gender & Region", "Comparison of suicide rates by gender and region", pio.to_html(fig5, full_html=False)))

    # 6. Pie Chart: Suicide Rates by Gender (Last Graph)
    if "Sex" in age_std_suicide_rates_df.columns:
        gender_avg = age_std_suicide_rates_df.groupby("Sex")["DeathRatePer100K"].mean().reset_index()
        fig6 = px.pie(
            gender_avg, names="Sex", values="DeathRatePer100K",
            title="Suicide Rates by Gender",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        graphs.append(("Suicide Rates by Gender", "Distribution of suicide rates between males and females", pio.to_html(fig6, full_html=False)))

    return render_template("index.html", graphs=graphs)

if __name__ == "__main__":
    app.run(debug=True)