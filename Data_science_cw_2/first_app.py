import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Set Streamlit option to disable the PyplotGlobalUseWarning
st.set_option('deprecation.showPyplotGlobalUse', False)

# Load data
data = pd.read_csv("enviroment.csv")

# Set the title of the Streamlit app
st.title("Environmental Damage")

# Filter out entries for the European Union
filtered_data = data[~data["COUNTRIES"].str.contains("European Union")]

# Define a sidebar for selecting the environmental variable
selected_variable = st.sidebar.selectbox("Select Environmental Variable", ["Water Pollution", "Soil Contamination", "Deforestation"])
variable_column_mapping = {
    "Water Pollution": "water_pollution",
    "Soil Contamination": "soil_contamination",
    "Deforestation": "deforestation"
}

# Sidebar for country selection
countries = filtered_data['COUNTRIES'].unique()
selected_countries = st.sidebar.multiselect("Select Countries", options=["All"] + list(countries), default=["All"])

# Display message if no country is selected
if not selected_countries:
    st.warning("Please choose a country.")
    st.stop()  # Stop execution of the script if no country is selected

# Check if both "All" and individual countries are selected
if "All" in selected_countries and len(selected_countries) > 1:
    st.warning("Please select either 'All' or individual countries, not both.")
    st.stop()  # Stop execution of the script if both "All" and individual countries are selected

# Sidebar for selecting year range
valid_years = [2010, 2012, 2014, 2016, 2018, 2020]
min_year = st.sidebar.slider("Select Min Year", min_value=min(valid_years), max_value=max(valid_years), value=min(valid_years))
max_year = st.sidebar.slider("Select Max Year", min_value=min(valid_years), max_value=max(valid_years), value=max(valid_years))

# Ensure max year is not less than min year
if max_year < min_year:
    st.warning("Max year cannot be less than min year.")
    st.stop()  # Stop execution of the script if max year is less than min year

# Display the selected variable as a subheader
st.subheader(f"Year with the Most {selected_variable}")

# Get the corresponding data column for the selected variable
selected_column = variable_column_mapping[selected_variable]

# Filter data based on selected year range
filtered_data = filtered_data[(filtered_data['year'] >= min_year) & (filtered_data['year'] <= max_year)]

# Create a figure for plotting
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Line plot
if "All" in selected_countries or not selected_countries:
    # Calculate the maximum value of the selected column across all years if "All" is selected
    max_damage_by_year = filtered_data.groupby("year")[selected_column].max()
    ax1.plot(max_damage_by_year, marker='o', linestyle='-', label='All Countries')
else:
    # Plot data for selected individual countries
    for country in selected_countries:
        country_data = filtered_data[filtered_data['COUNTRIES'] == country]
        max_damage_by_year = country_data.groupby("year")[selected_column].max()
        ax1.plot(max_damage_by_year, marker='o', linestyle='-', label=country)

ax1.set_title(f"Maximum {selected_variable} Over the Years by Country")
ax1.set_xlabel("Year")
ax1.set_ylabel(f"Maximum {selected_variable}")
ax1.legend()
ax1.grid(True)

# Display the box plot only if individual countries are selected
if "All" not in selected_countries:
    boxplot_data = [filtered_data[filtered_data['COUNTRIES'] == country][selected_column] for country in selected_countries]
    ax2.boxplot(boxplot_data, labels=selected_countries, widths=0.6)
    ax2.set_title(f"{selected_variable} Across Countries")
    ax2.set_ylabel(selected_variable)
    ax2.set_xticklabels(selected_countries, rotation=45, ha='right')
else:
    ax2.axis('off')  # Hide the box plot if "All" is selected

plt.tight_layout()
st.pyplot(fig)

# Display information about the year with the highest environmental damage
if "All" in selected_countries or not selected_countries:
    max_damage_row = filtered_data.loc[filtered_data[selected_column].idxmax()]
    st.subheader(f"Year with the most {selected_variable.lower()}:")
    st.markdown(f"**{max_damage_row['year']}** with **{max_damage_row[selected_column]:,.0f} tonnes**")
    st.markdown(f"Country with the most {selected_variable.lower()}: **{max_damage_row['COUNTRIES']}**")
else:
    for country in selected_countries:
        # Find the year with the highest damage for the selected country
        max_damage_row = filtered_data[filtered_data['COUNTRIES'] == country].loc[
            filtered_data[filtered_data['COUNTRIES'] == country][selected_column].idxmax()]
        st.subheader(f"Year with the most {selected_variable.lower()} in {country}:")
        st.markdown(f"**{max_damage_row['year']}** with **{max_damage_row[selected_column]:,.0f} tonnes**")
