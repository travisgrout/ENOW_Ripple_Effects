import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import squarify
from pywaffle import Waffle # <-- IMPORT THE NEW LIBRARY
import math

# --- Page Configuration ---
st.set_page_config(layout="wide") # Use wide layout for more space

# --- Data Loading ---
# It's good practice to load all data at the start.
try:
    national_totals_df = pd.read_csv("ica_nationalTotals.csv")
    state_totals_df = pd.read_csv("ica_stateTotals.csv")
except FileNotFoundError as e:
    st.error(f"Error loading data file: {e.name}. Please ensure it is in the root of your repository.")
    st.stop()

# --- Calculations for Main Page Variables ---
direct_impact = national_totals_df[national_totals_df['ImpactType'] == 'Direct'].iloc[0]
total_impact = national_totals_df.sum(numeric_only=True)

var_1_formatted = f"{(direct_impact['WageAndSalaryEmployment'] / 1_000_000):.1f}"
var_2_formatted = f"${(direct_impact['Wages_and_Salary'] / 1_000_000_000):.0f}"
var_3_formatted = f"${(direct_impact['Value_Added'] / 1_000_000_000):.0f}"
var_4_formatted = f"{(total_impact['WageAndSalaryEmployment'] / 1_000_000):.1f}"
var_5_formatted = f"${(total_impact['Wages_and_Salary'] / 1_000_000_000):.0f}"
var_6_formatted = f"${(total_impact['Value_Added'] / 1_000_000_000):.0f}"
var_7_formatted = f"${(total_impact['Output'] / 1_000_000_000):.0f}"
avg_wages_per_worker_formatted = f"${(total_impact['Wages_and_Salary'] / total_impact['WageAndSalaryEmployment']):,.0f}"
avg_gdp_per_worker_formatted = f"${(total_impact['Value_Added'] / total_impact['WageAndSalaryEmployment']):,.0f}"

# --- Page Navigation State ---
if 'page' not in st.session_state:
    st.session_state.page = 'main'
def set_page(page_name):
    st.session_state.page = page_name

# --- MAIN PAGE ---
def main_page_content():
    st.title("U.S. Ocean Economy")
    try:
        st.image("https://cdn.star.nesdis.noaa.gov/GOES19/ABI/CONUS/GEOCOLOR/1250x750.jpg", use_container_width=True)
    except Exception:
        st.warning("Could not load the map image.")
    
    st.markdown(f"""
    <div style="font-size: 22px;">
    About <b>{var_1_formatted} million</b> Americans are directly employed...
    </div>
    """, unsafe_allow_html=True) # Truncated for brevity
    st.markdown("---")
    st.button("Learn More", on_click=set_page, args=('details',))

# --- DETAILS PAGE (Treemaps) ---
def create_treemap(data_column, title):
    # This function remains the same as your version
    labels = []
    for _, row in national_totals_df.iterrows():
        impact_type = row['ImpactType']
        value = row[data_column]
        if data_column == 'WageAndSalaryEmployment':
            formatted_value = f"{value / 1_000_000:,.1f} million jobs"
        else:
            formatted_value = f"${value / 1_000_000_000:.0f} Billion"
        labels.append(f"{impact_type}\n{formatted_value}")
    sizes = national_totals_df[data_column].values
    colors = ['#056FB7', '#C6E6F0', '#A5AAAF']
    fig, ax = plt.subplots(1, figsize=(16, 9))
    squarify.plot(sizes=sizes, label=labels, color=colors, ax=ax, text_kwargs={'color':'black', 'fontsize':40})
    plt.title(title, fontsize=20, color="white")
    plt.axis('off')
    fig.patch.set_alpha(0.0)
    st.pyplot(fig)

def details_page():
    # This function remains the same as your version
    st.title("Economic Contribution Details")
    st.button("Back to Main Page", on_click=set_page, args=('main',))
    # ... (code for all 4 treemap sections)
    # Truncated for brevity, assuming this is unchanged
    st.header("Employment")
    st.markdown(f"<div style='font-size: 20px; text-align: center;'>...</div>", unsafe_allow_html=True)
    create_treemap('WageAndSalaryEmployment', 'Employment by Impact Type')
    # ... and so on for the other 3 charts

def state_page():
    st.title("State Ocean Economies")

    # --- 1. Setup Input Controls ---
    st.subheader("Select Your Criteria")
    
    state_list = ["All Coastal States"] + sorted(state_totals_df['DestinationState'].unique().tolist())
    metric_columns = state_totals_df.select_dtypes(include='number').columns.tolist()

    col1, col2 = st.columns(2)
    with col1:
        selected_state = st.selectbox("Select a State:", state_list)
    with col2:
        selected_metric = st.selectbox("Select an Economic Metric:", metric_columns, index=metric_columns.index('WageAndSalaryEmployment'))

    st.write("Select Effects to Include:")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        show_direct = st.checkbox("Direct", value=True)
    with c2:
        show_indirect = st.checkbox("Indirect", value=True)
    with c3:
        show_induced = st.checkbox("Induced", value=True)

    # --- 2. Filter Data Based on Inputs ---
    selected_impacts = []
    if show_direct: selected_impacts.append("Direct")
    if show_indirect: selected_impacts.append("Indirect")
    if show_induced: selected_impacts.append("Induced")
    
    if not selected_impacts:
        st.warning("Please select at least one effect type.")
        return

    filtered_by_impact = state_totals_df[state_totals_df['ImpactType'].isin(selected_impacts)]
    national_total = filtered_by_impact[selected_metric].sum()

    if selected_state == "All Coastal States":
        state_total = national_total
    else:
        state_total = filtered_by_impact[filtered_by_impact['DestinationState'] == selected_state][selected_metric].sum()

    # --- 3. Display Map and Waffle Chart ---
    st.markdown("---")
    map_col, chart_col = st.columns(2)

    with map_col:
        if selected_state == "All Coastal States":
            image_path = "https://cdn.star.nesdis.noaa.gov/GOES19/ABI/CONUS/GEOCOLOR/1250x750.jpg"
            st.image(image_path, use_container_width=True, caption="U.S. Coastal View")
        else:
            map_name = f"Map_{selected_state.replace(' ', '_')}.png"
            image_path = f"ENOW state maps/{map_name}"
            try:
                st.image(image_path, use_container_width=True)
            except FileNotFoundError:
                st.warning(f"Map image for '{selected_state}' not found.")
    
    with chart_col:
        st.subheader(f"{selected_metric} in {selected_state}")
        
        if national_total == 0:
            st.write("No data to display for the selected criteria.")
            return
            
        # --- NEW: Waffle Chart Logic with Fixed Scale ---
        if selected_metric in ['WageAndSalaryEmployment', 'ProprietorEmployment']:
            value_per_square = 25000
            info_text = "25,000 jobs"
        else: # For Wages_and_Salary, Value_Added, and Output
            value_per_square = 1_000_000_000
            info_text = "$1 billion"
        
        state_squares = int(round(state_total / value_per_square))
        other_squares = int(round((national_total - state_total) / value_per_square))
        
        # Prevent division by zero if total is zero
        if (state_squares + other_squares) == 0:
            st.write("The total value is too small to display on this chart.")
            return

        state_percentage = (state_total / national_total) * 100
        total_squares = state_squares + other_squares
        
        # Dynamically set the number of rows to keep the chart looking good
        rows = math.ceil(total_squares / 25) if total_squares > 0 else 1

        fig = plt.figure(
            FigureClass=Waffle,
            rows=rows,
            values=[state_squares, other_squares],
            colors=("#056FB7", "#A5AAAF"),
            labels=[f"{selected_state} ({state_percentage:.1f}%)", "Rest of U.S."],
            legend={'loc': 'upper left', 'bbox_to_anchor': (1, 1), 'fontsize': 12},
            font_size=20,
            icons='square',
            icon_style='solid',
            # Let pywaffle handle the layout automatically
        )
        fig.patch.set_alpha(0.0)
        ax = plt.gca()
        ax.set_facecolor('#00000000')
        ax.legend(facecolor='#DDDDDD')
        st.pyplot(fig)
        st.info(f"Each square represents **{info_text}** of '{selected_metric}'.")
        
# --- Main App Router ---

# Sidebar for main navigation
st.sidebar.title("Navigation")
app_mode = st.sidebar.radio("Choose a page:", ["U.S. Ocean Economy", "State Ocean Economies"])

if app_mode == "U.S. Ocean Economy":
    # Logic for the two-part US Economy pages
    if st.session_state.page == 'main':
        main_page_content()
    elif st.session_state.page == 'details':
        details_page()
else:
    # Set page state for the state page and call it
    st.session_state.page = 'state'
    state_page()
