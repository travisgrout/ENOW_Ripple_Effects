import streamlit as st
import pandas as pd
from pathlib import Path

# --- Page Configuration and Styling ---
# Sets the layout of the page and injects custom CSS for colors.
st.set_page_config(layout="centered")

# --- Data Loading and Processing ---
try:
    # Using a simple relative path is the most reliable for Streamlit Cloud
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
        st.image("ENOW state maps/Map_United_States.jpg", use_container_width=True)
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
    st.button("View More Data", on_click=set_page, args=('details',))


# --- Details Page ---

def create_pictogram(data_column, icon, scale, color):
    """Helper function to create and display a pictogram."""
    st.markdown(f'<p style="color:{color}; font-size: 1.5em; font-weight: bold;">{icon * 20}</p>', unsafe_allow_html=True)
    for index, row in national_totals_df.iterrows():
        impact_type = row['ImpactType']
        value = row[data_column]
        num_icons = int(value / scale)
        # Display the icons for each category
        st.markdown(f"**{impact_type}:** {icon * num_icons}", unsafe_allow_html=True)

def details_page():
    st.title("Economic Contribution Details")
    st.button("Back to Main Page", on_click=set_page, args=('main',))

    # --- Employment Section ---
    st.markdown("---")
    st.header("Employment")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"<div style='font-size: 20px;'>Marine industries supported about <b>{var_4_formatted} million</b> U.S. jobs in 2023.</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("Each 👤 represents 100,000 workers.")
        create_pictogram('WageAndSalaryEmployment', '👤', 100000, '#FFFFFF') # White icon

    # --- Wages and Salary Section ---
    st.markdown("---")
    st.header("Wages and Salary")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""<div style='font-size: 20px;'>
        Supported <b>{var_5_formatted} billion</b> in labor income, an average of about <b>{avg_wages_per_worker_formatted}</b> per worker.
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("Each 💰 represents $10 billion.")
        create_pictogram('Wages_and_Salary', '💰', 10_000_000_000, '#FFD700') # Gold icon

    # --- Contribution to GDP Section ---
    st.markdown("---")
    st.header("Contribution to GDP")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""<div style='font-size: 20px;'>
        Supported <b>{var_6_formatted} billion</b> in GDP, an average of almost <b>{avg_gdp_per_worker_formatted}</b> per worker.
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("Each 🏭 represents $20 billion.")
        create_pictogram('Value_Added', '🏭', 20_000_000_000, '#ADD8E6') # Light Blue icon

    # --- Economic Output Section ---
    st.markdown("---")
    st.header("Economic Output")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"<div style='font-size: 20px;'>Supported about <b>{var_7_formatted} billion</b> in total economic activity.</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("Each 📈 represents $30 billion.")
        create_pictogram('Output', '📈', 30_000_000_000, '#90EE90') # Light Green icon


# --- App Navigation Logic ---
if st.session_state.page == 'main':
    main_page()
elif st.session_state.page == 'details':
    details_page()
