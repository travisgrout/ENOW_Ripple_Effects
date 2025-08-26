import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import squarify # <-- IMPORT THE NEW LIBRARY

# --- Page Configuration (using config.toml is recommended) ---
st.set_page_config(layout="centered")

# --- Data Loading and Processing ---
try:
    national_totals_df = pd.read_csv("ica_nationalTotals.csv")
except FileNotFoundError:
    st.error("The file 'ica_nationalTotals.csv' was not found. Please make sure it is in the root of your GitHub repository.")
    st.stop()

# --- Calculations for Variables (same as before) ---
direct_impact = national_totals_df[national_totals_df['ImpactType'] == 'Direct'].iloc[0]
total_impact = national_totals_df.sum(numeric_only=True)

var_1_formatted = f"{(direct_impact['WageAndSalaryEmployment'] / 1_000_000):.1f}"
var_2_formatted = f"${(direct_impact['Wages_and_Salary'] / 1_000_000_000):.0f}"
var_3_formatted = f"${(direct_impact['Value_Added'] / 1_000_000_000):.0f}"
var_4_formatted = f"{(total_impact['WageAndSalaryEmployment'] / 1_000_000):.1f}"
var_5_formatted = f"${(total_impact['Wages_and_Salary'] / 1_000_000_000):.0f}"
var_6_formatted = f"${(total_impact['Value_Added'] / 1_000_000_000):.0f}"
var_7_formatted = f"${(total_impact['Output'] / 1_000_000_000):.0f}"

avg_wages_per_worker = (total_impact['Wages_and_Salary'] / total_impact['WageAndSalaryEmployment'])
avg_wages_per_worker_formatted = f"${avg_wages_per_worker:,.0f}"
avg_gdp_per_worker = (total_impact['Value_Added'] / total_impact['WageAndSalaryEmployment'])
avg_gdp_per_worker_formatted = f"${avg_gdp_per_worker:,.0f}"

# --- Page Navigation ---
if 'page' not in st.session_state:
    st.session_state.page = 'main'

def set_page(page_name):
    st.session_state.page = page_name

# --- Main Page ---
def main_page():
    st.title("U.S. Ocean Economy")
    try:
        st.image("https://cdn.star.nesdis.noaa.gov/GOES19/ABI/CONUS/GEOCOLOR/1250x750.jpg", use_container_width=True)
    except FileNotFoundError:
        st.warning("Could not find the map image.")

    st.markdown(f"""
    <div style="font-size: 22px;">
    About <b>{var_1_formatted} million</b> Americans are directly employed in the six ocean economy sectors tracked by NOAA.
    These workers earned over <b>{var_2_formatted} billion</b> in wages in 2023, and the United States ocean economy
    contributed about <b>{var_3_formatted} billion</b> to GDP.
    <br><br>
    These are big numbers, but they represent only part of ocean industries’ contribution to the broader economy.
    <br><br>
    To get a sense of the scale and composition of these economic ripple effects, NOAA’s Office for Coastal Management
    used the IMPLAN input-output model to estimate the total economic contribution of our country’s ocean economy.
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.button("Learn More", on_click=set_page, args=('details',))

# --- Details Page ---

# (Keep all your code from before this function the same)

def create_treemap(data_column, title):
    """Helper function to create and display a treemap with improved formatting."""
    
    # --- 1. Create Human-Readable Labels ---
    labels = []
    for _, row in national_totals_df.iterrows():
        impact_type = row['ImpactType']
        value = row[data_column]
        
        # Custom formatting based on the data type
        if data_column == 'WageAndSalaryEmployment':
            # Format for jobs (e.g., "1,838,885 jobs")
            formatted_value = f"{value / 1_000_000:,.1f} million jobs"
        else:
            # Format for billions of dollars (e.g., "$91 Billion")
            formatted_value = f"${value / 1_000_000_000:.0f} Billion"
            
        labels.append(f"{impact_type}\n{formatted_value}")

    sizes = national_totals_df[data_column].values
    colors = ['#056FB7', '#C6E6F0', '#A5AAAF']
    
    # --- 2. Increase Plot and Font Size ---
    # Increased figsize for a larger plot and fontsize for bigger labels
    fig, ax = plt.subplots(1, figsize=(16, 9))
    squarify.plot(
        sizes=sizes, 
        label=labels, 
        color=colors, 
        ax=ax, 
        text_kwargs={'color':'black', 'fontsize':40}
    )
    
    plt.title(title, fontsize=20, color="white")
    plt.axis('off')
    
    # Use a transparent background for the plot figure
    fig.patch.set_alpha(0.0)
    
    st.pyplot(fig)

def details_page():
    st.title("Economic Contribution Details")
    st.button("Back to Main Page", on_click=set_page, args=('main',))

    # --- Employment Section ---
    st.markdown("---")
    st.header("Employment")
    # Text is now full-width
    st.markdown(f"<div style='font-size: 20px; text-align: center;'>Marine industries supported about <b>{var_4_formatted} million</b> U.S. jobs in 2023.</div>", unsafe_allow_html=True)
    # Treemap is now full-width, placed below the text
    create_treemap(
        data_column='WageAndSalaryEmployment',
        title=' '
    )

    # --- Wages and Salary Section ---
    st.markdown("---")
    st.header("Wages and Salary")
    st.markdown(f"""<div style='font-size: 20px; text-align: center;'>
    Supported <b>{var_5_formatted} billion</b> in labor income, an average of about <b>{avg_wages_per_worker_formatted}</b> per worker.
    </div>""", unsafe_allow_html=True)
    create_treemap(
        data_column='Wages_and_Salary',
        title='W '
    )

    # --- Contribution to GDP Section ---
    st.markdown("---")
    st.header("Contribution to GDP")
    st.markdown(f"""<div style='font-size: 20px; text-align: center;'>
    Supported <b>{var_6_formatted} billion</b> in GDP, an average of almost <b>{avg_gdp_per_worker_formatted}</b> per worker.
    </div>""", unsafe_allow_html=True)
    create_treemap(
        data_column='Value_Added',
        title=' '
    )

    # --- Economic Output Section ---
    st.markdown("---")
    st.header("Economic Output")
    st.markdown(f"<div style='font-size: 20px; text-align: center;'>Supported about <b>{var_7_formatted} billion</b> in total economic activity.</div>", unsafe_allow_html=True)
    create_treemap(
        data_column='Output',
        title=' '
    )
        
# --- App Navigation Logic ---
if st.session_state.page == 'main':
    main_page()
elif st.session_state.page == 'details':
    details_page()
