import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path # <-- IMPORT THIS

# Get the directory of the current script
script_dir = Path(__file__).parent

# --- Data Loading and Processing ---
try:
    # Construct the full path to the CSV file
    csv_path = script_dir / "ica_nationalTotals.csv"
    national_totals_df = pd.read_csv(csv_path)
except FileNotFoundError:
    st.error(f"The file '{csv_path.name}' was not found. Please make sure it is in the same directory as the script.")
    st.stop()

# --- Calculations for Variables ---

# Isolate the 'Direct' impact data from the DataFrame
direct_impact = national_totals_df[national_totals_df['ImpactType'] == 'Direct'].iloc[0]

# Calculate the sum of all impact types for the totals
total_impact = national_totals_df.sum(numeric_only=True)

# <VAR_1>: Direct WageAndSalaryEmployment in millions
var_1 = direct_impact['WageAndSalaryEmployment'] / 1_000_000
var_1_formatted = f"{var_1:.1f}" # We format to one decimal place

# <VAR_2>: Direct Wages_and_Salary in billions
var_2 = direct_impact['Wages_and_Salary'] / 1_000_000_000
var_2_formatted = f"${var_2:,.0f}" # We format as a whole number with a dollar sign

# <VAR_3>: Direct Value_Added in billions
var_3 = direct_impact['Value_Added'] / 1_000_000_000
var_3_formatted = f"${var_3:,.0f}"

# <VAR_4>: Sum of WageAndSalaryEmployment in millions
var_4 = total_impact['WageAndSalaryEmployment'] / 1_000_000
var_4_formatted = f"{var_4:.1f}"

# <VAR_5>: Sum of Wages_and_Salary in billions
var_5 = total_impact['Wages_and_Salary'] / 1_000_000_000
var_5_formatted = f"${var_5:,.0f}"

# <VAR_6>: Sum of Value_Added in billions
var_6 = total_impact['Value_Added'] / 1_000_000_000
var_6_formatted = f"${var_6:,.0f}"

# <VAR_7>: Sum of Output in billions
var_7 = total_impact['Output'] / 1_000_000_000
var_7_formatted = f"${var_7:,.0f}"

# Calculations for the second page (per-worker averages)
avg_wages_per_worker = (total_impact['Wages_and_Salary'] / total_impact['WageAndSalaryEmployment'])
avg_wages_per_worker_formatted = f"${avg_wages_per_worker:,.0f}"

avg_gdp_per_worker = (total_impact['Value_Added'] / total_impact['WageAndSalaryEmployment'])
avg_gdp_per_worker_formatted = f"${avg_gdp_per_worker:,.0f}"


# --- Page Navigation ---
# Streamlit reruns the script on each interaction. We use 'session_state' to remember
# which page the user is on.
if 'page' not in st.session_state:
    st.session_state.page = 'main'

def set_page(page_name):
    """A helper function to change the page in session_state."""
    st.session_state.page = page_name

# --- Main Page Function ---
def main_page():
    """This function draws the main page of the app."""
    st.title("U.S. Ocean Economy")
    
    # Construct the full path to the image file
    image_path = script_dir / "ENOW state maps" / "Map_United_States.png"
    
    try:
        # st.image needs the path as a string
        st.image(str(image_path), use_column_width=True)
    except FileNotFoundError:
        st.warning(f"Could not find the map image at '{image_path}'")

    # The main explanatory text, with our calculated variables inserted.
    st.markdown(f"""
    <div style="font-size: 22px;">
    About <b>{var_1_formatted} million</b> Americans are directly employed in the six ocean economy sectors tracked by NOAA. 
    These workers earned over <b>{var_2_formatted} billion</b> in wages in 2023, and the United States ocean economy 
    contributed about <b>{var_3_formatted} billion</b> to GDP.
    <br><br>
    These are big numbers, but they represent only part of ocean industries’ contribution to the broader economy. 
    Businesses in the ocean economy support additional American jobs by purchasing goods and services from in-state 
    suppliers (indirect effects). Workers in the ocean economy support additional jobs through local household 
    spending (induced effects).
    <br><br>
    To get a sense of the scale and composition of these economic ripple effects, NOAA’s Office for Coastal Management 
    used the IMPLAN input-output model to estimate the total economic contribution of our country’s ocean economy.
    </div>
    """, unsafe_allow_html=True)

    # This button, when clicked, will change the page to 'details'
    st.button("View More Data", on_click=set_page, args=('details',))

# --- Details Page Function ---
def details_page():
    """This function draws the details page of the app."""
    st.title("Economic Contribution Details")
    st.button("Back to Main Page", on_click=set_page, args=('main',))

    # --- Employment Section ---
    st.markdown("---") # This creates a horizontal line
    st.header("Employment")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"<div style='font-size: 20px;'>Marine industries directly or indirectly supported about <b>{var_4_formatted} million</b> U.S. jobs in 2023.</div>", unsafe_allow_html=True)
    with col2:
        # For the pictograph, we calculate how many icons to show and then print them.
        num_icons = int(total_impact['WageAndSalaryEmployment'] / 100000)
        # Using a larger emoji for better visibility
        st.write("".join(["👨‍💼" for _ in range(num_icons)]))
        st.caption("Each icon represents 100,000 workers.")

    # --- Wages and Salary Section ---
    st.markdown("---")
    st.header("Wages and Salary")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""<div style='font-size: 20px;'>
        Marine industries directly or indirectly supported <b>{var_5_formatted} billion</b> in labor income, 
        an average of about <b>{avg_wages_per_worker_formatted}</b> per worker.
        </div>""", unsafe_allow_html=True)
    with col2:
        fig, ax = plt.subplots()
        national_totals_df.plot.bar(x='ImpactType', y='Wages_and_Salary', ax=ax, legend=None, color=['#1f77b4', '#ff7f0e', '#2ca02c'])
        ax.set_xlabel("Impact Type")
        ax.set_ylabel("Wages and Salary (in Billions USD)")
        ax.set_title("Wages and Salary by Impact Type")
        st.pyplot(fig)

    # --- Contribution to GDP Section ---
    st.markdown("---")
    st.header("Contribution to GDP")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""<div style='font-size: 20px;'>
        Marine industries directly or indirectly supported <b>{var_6_formatted} billion</b> in GDP, 
        an average of almost <b>{avg_gdp_per_worker_formatted}</b> per worker.
        </div>""", unsafe_allow_html=True)
    with col2:
        fig, ax = plt.subplots()
        national_totals_df.plot.bar(x='ImpactType', y='Value_Added', ax=ax, legend=None, color=['#1f77b4', '#ff7f0e', '#2ca02c'])
        ax.set_xlabel("Impact Type")
        ax.set_ylabel("Contribution to GDP (in Billions USD)")
        ax.set_title("Contribution to GDP by Impact Type")
        st.pyplot(fig)

    # --- Economic Output Section ---
    st.markdown("---")
    st.header("Economic Output")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"<div style='font-size: 20px;'>Marine industries supported about <b>{var_7_formatted} billion</b> in total economic activity around the United States.</div>", unsafe_allow_html=True)
    with col2:
        fig, ax = plt.subplots()
        national_totals_df.plot.bar(x='ImpactType', y='Output', ax=ax, legend=None, color=['#1f77b4', '#ff7f0e', '#2ca02c'])
        ax.set_xlabel("Impact Type")
        ax.set_ylabel("Economic Output (in Billions USD)")
        ax.set_title("Economic Output by Impact Type")
        st.pyplot(fig)


# --- App Navigation Logic ---
# This is the main part of the app that decides which page function to call.
if st.session_state.page == 'main':
    main_page()
elif st.session_state.page == 'details':
    details_page()
