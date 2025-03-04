import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pycountry_convert as pc
from flask import Flask, render_template

# Initialize Flask app
app = Flask(__name__)

# Define dataset path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "suicide_rates.csv")

# Function to map country to continent
def country_to_continent(country):
    try:
        country_code = pc.country_name_to_country_alpha2(country, cn_name_format="default")
        continent_code = pc.country_alpha2_to_continent_code(country_code)
        continent_name = {
            "AF": "Africa",
            "AS": "Asia",
            "EU": "Europe",
            "NA": "North America",
            "SA": "South America",
            "OC": "Oceania"
        }.get(continent_code, "Unknown")
        return continent_name
    except:
        return "Unknown"

# Load dataset
df = pd.read_csv(DATA_PATH)
df.columns = df.columns.str.strip().str.lower()

# Ensure 'continent' column exists
if "continent" not in df.columns:
    df["continent"] = df["countryname"].apply(country_to_continent)

# Ensure 'static/images' directory exists
STATIC_IMAGES_PATH = os.path.join(BASE_DIR, "static", "images")
os.makedirs(STATIC_IMAGES_PATH, exist_ok=True)

# Define color palette
color_palette = sns.color_palette("Set2")

# Adjust column mappings dynamically
column_mappings = {
    "year": "year",
    "suicide rate": "deathrateper100k",
    "country": "countryname",
    "age group": "agegroup",
    "gdp per capita": "gdppercapita",
    "population": "population",
    "continent": "continent"
}

graphs = []

if df is not None:
    try:
        plt.figure(figsize=(12, 6))
        avg_rate = df.groupby(column_mappings["year"])[column_mappings["suicide rate"]].mean()
        avg_rate.plot(kind="bar", color=color_palette[0])
        plt.title("Average Suicide Rate by Year")
        plt.ylabel("Death Rate per 100k")
        plt.xlabel("Year")
        plt.xticks(rotation=45)
        bar_chart_path = os.path.join(STATIC_IMAGES_PATH, "bar_chart.png")
        plt.savefig(bar_chart_path)
        plt.close()
        graphs.append(("bar_chart.png", "Average Suicide Rate by Year", "The average global suicide rate has been a critical metric for understanding mental health trends over time. A bar chart depicting the average suicide rate by year can provide a clear visual representation of how these rates have fluctuated."))

        plt.figure(figsize=(12, 6))
        countries = ["United States", "Japan", "India", "Germany"]
        subset = df[df[column_mappings["country"]].isin(countries)]
        sns.lineplot(data=subset, x=column_mappings["year"], y=column_mappings["suicide rate"], hue=column_mappings["country"], palette=sns.color_palette("Set2", n_colors=len(countries)))
        plt.title("Suicide Rates Over Time (Selected Countries)")
        plt.xlabel("Year")
        plt.ylabel("Suicide Rate per 100k")
        plt.xticks(rotation=45)
        line_chart_path = os.path.join(STATIC_IMAGES_PATH, "line_chart.png")
        plt.savefig(line_chart_path)
        plt.close()
        graphs.append(("line_chart.png", "Suicide Rates Over Time", "A line chart comparing suicide rates in select countries can offer insights into how different nations have managed mental health issues. For example, the Centers for Disease Control and Prevention (CDC) reports that suicide rates in the United States increased by 37% between 2000 and 2018, then decreased by 5% between 2018 and 2020, only to return to their peak in 2022."))

        latest_year = df[column_mappings["year"]].max()
        age_groups = df[df[column_mappings["year"]] == latest_year].groupby(column_mappings["age group"])[column_mappings["suicide rate"]].mean()
        plt.figure(figsize=(10, 10))
        age_groups.plot(kind="pie", autopct='%1.1f%%', colors=color_palette)
        plt.title(f"Suicide Rates by Age Group ({latest_year})")
        pie_chart_path = os.path.join(STATIC_IMAGES_PATH, "pie_chart.png")
        plt.savefig(pie_chart_path)
        plt.close()
        graphs.append(("pie_chart.png", f"Suicide Rates by Age Group ({latest_year})", f"Proportional suicide rates by age group in the latest year can be visualized using a pie chart. This chart can reveal which age groups are most at risk. "))

        plt.figure(figsize=(12, 6))
        continent_data = df.groupby([column_mappings["continent"], column_mappings["year"]])[column_mappings["suicide rate"]].mean().unstack()
        continent_data.T.plot(kind="bar", stacked=True, figsize=(12, 6), colormap="Set3")
        plt.title("Suicide Rate by Continent Over Time")
        plt.ylabel("Suicide Rate per 100k")
        plt.xlabel("Year")
        plt.xticks(rotation=45)
        stacked_bar_path = os.path.join(STATIC_IMAGES_PATH, "stacked_bar.png")
        plt.savefig(stacked_bar_path)
        plt.close()
        graphs.append(("stacked_bar.png", "Suicide Rate by Continent", "A stacked bar chart comparing suicide rates across continents can illustrate regional disparities. "))

        plt.figure(figsize=(12, 6))
        sns.scatterplot(data=df, x=column_mappings["gdp per capita"], y=column_mappings["suicide rate"], hue=column_mappings["continent"], palette="tab10")
        plt.title("GDP Per Capita vs. Suicide Rate")
        plt.xlabel("GDP Per Capita")
        plt.ylabel("Suicide Rate per 100k")
        scatter_plot_path = os.path.join(STATIC_IMAGES_PATH, "scatter_plot.png")
        plt.savefig(scatter_plot_path)
        plt.close()
        graphs.append(("scatter_plot.png", "Economic Impact on Suicide Rate", "A scatter plot showing GDP per capita vs. suicide rate can highlight the economic factors influencing suicide rates. Research indicates that economic downturns, such as the 2008 global financial crisis, have been associated with increased suicide rates, particularly among men in countries with significant job losses. "))

        plt.figure(figsize=(12, 6))
        sns.boxplot(data=df, x=column_mappings["age group"], y=column_mappings["suicide rate"], hue=column_mappings["age group"], palette="coolwarm")
        plt.title("Suicide Rate Distribution by Age Group")
        plt.xticks(rotation=45)
        box_plot_path = os.path.join(STATIC_IMAGES_PATH, "box_plot.png")
        plt.savefig(box_plot_path)
        plt.close()
        graphs.append(("box_plot.png", "Suicide Rate by Age", "A box plot showing the distribution of suicide rates by age group can provide a detailed view of the variability within each age group. "))

        plt.figure(figsize=(12, 6))
        plt.hist(df[column_mappings["suicide rate"]], bins=20, color=color_palette[0], edgecolor='black', alpha=0.7)
        plt.title("Distribution of Suicide Rates")
        plt.xlabel("Suicide Rate per 100k")
        histogram_path = os.path.join(STATIC_IMAGES_PATH, "histogram.png")
        plt.savefig(histogram_path)
        plt.close()
        graphs.append(("histogram.png", "Suicide Rate Distribution", "A histogram depicting the distribution of suicide rates can show how these rates are spread across different populations. This type of chart can reveal whether suicide rates are concentrated in specific demographics or more evenly distributed."))

        plt.figure(figsize=(12, 6))
        sns.scatterplot(data=df, x=column_mappings["gdp per capita"], y=column_mappings["suicide rate"], size=column_mappings["population"], hue=column_mappings["continent"], palette="viridis", sizes=(10, 1000), alpha=0.6)
        plt.title("Suicide Rate vs. GDP Per Capita (Bubble Size = Population)")
        plt.xlabel("GDP Per Capita")
        plt.ylabel("Suicide Rate per 100k")
        bubble_chart_path = os.path.join(STATIC_IMAGES_PATH, "bubble_chart.png")
        plt.savefig(bubble_chart_path)
        plt.close()
        graphs.append(("bubble_chart.png", "Bubble Chart Analysis", "Bubble chart showing suicide rate vs. GDP per capita, with bubble size representing population."))

    except KeyError as e:
        print(f"\n❌ Error: Missing column in dataset - {e}\n")


@app.route('/')
def index():
    return render_template("index.html", graphs=graphs)

if __name__ == "__main__":
    app.run(debug=True)
