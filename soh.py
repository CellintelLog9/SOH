import streamlit as st
import requests

# Add custom CSS for box shadow and transparency
st.markdown("""
    <style>
    .box {
        background-color: rgba(255, 255, 255, 0.1);
        padding: 20px;
        margin-bottom: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    .box-header {
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .box-content {
        font-size: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Title of the presentation app
st.title("Project Presentation")


# Function to create a box with content
def create_box(header, content):
    st.markdown(f"""
    <div class="box">
        <div class="box-header">{header}</div>
        <div class="box-content">{content}</div>
    </div>
    """, unsafe_allow_html=True)


# Manufacturing Process box
create_box("Manufacturing Process", """
1. **Initial Cell Cycling**: Each cell undergoes an individual cycling process to gather essential data. This data is input into the cell acer system, which categorizes cells into appropriate buckets based on their performance metrics.

2. **Pack Assembly**: After categorization, the cells are assembled into battery packs.

3. **Pack Cycling**: Once assembled, the entire pack is cycled again to measure the overall capacity and ensure compliance with performance standards. Additionally, the functionality of the BMS is tested using Pack Acer.

4. **8k and 2k Pack Testing**:
    - **8k Pack**: The BMS is attached inside the battery pack. The testing process shows the actual capacity in the pack cycler data, with cut-off voltages set between 2.7V (max) and 1.7V (min).
    - **2k Pack**: The BMS is housed inside the ICC kit, with the lower-end cut-off voltage set between 2.7V (max) and 1.95V (min).

Following the testing, the cycler data, BMS data, and acceptance criteria are reviewed. The true capacity is derived from the cycler data, while the BMS data can also provides capacity values using coulomb counting by filtering the BMS data using Timestamp of cycler file (Plot Below of Current (I) data between cycler and BMS ). However, there is a noticeable difference between the cycler and BMS capacities, primarily due to current calibration discrepancies and power cut, with the BMS reporting larger current values compared to the cycler.
""")

# Fetch and display the plot as an HTML component from GitHub
url = "https://raw.githubusercontent.com/CellintelLog9/SOH/main/line_chart_current3.html"
response = requests.get(url)
if response.status_code == 200:
    st.components.v1.html(response.text, height=500)
else:
    st.error("Failed to load the plot from GitHub.")


# ML Model Development Process box
create_box("ML Model Development Process", """
### Step 1: Data Collection
- Data was fetched from custom reports where the charge-discharge cycle was less than 30.
- 193 packs were analyzed, and outliers were removed, leaving 22 packs for validation with custom reports, cycler, and BMS data.

### Step 2: Data Preprocessing
- Identified charging zones where current > 0 in the Telematics data.
-Sorted data based on the datetime for each telematics ID and assigned a unique number to each charging session.
-Joined the custom report with capacity data from cycler files and the average current, timestamp, and capacity data from BMS files (BMS and cycler files are generated simultaneously during pack testing).

### Step 3: Data Transformation
For each charging session, the following values were identified:
- Mean, median, minimum, maximum of voltage, current, maximum and minimum monomer temperatures, SOC%, and device date.
- Values for charge-discharge cycles, capacity on day zero from both cycler and BMS (calculated via coulomb counting), average current, and time duration of step 8 in the BMS.

""")


# Model Training Approaches box
create_box("Model Training Approaches", """
### 1st Approach:
- Features: Mean, median, min, max for voltage, current, temperatures, and SOC%.
- Target: Pack cycler capacity.
- Result: No significant correlation was identified between input features and cycler capacity.
- capacity_first                    1.000000
- BM_BattCurrrent_std               0.039267
- BM_SocPercent_max                -0.001158
- BM_BattVoltage_min               -0.005754
- Soc Change 			-0.001259
- session_duration                 -0.011942

""")



    
create_box("Model Training Approaches", """
### Second Approach:
A new set of features was added, including SOC change (Calculated using SOC percent maximum – SOC percent minimum value) for each charging zone, expected capacity in SOC change (capacity * SOC change / 100), and capacity added per zone. Instead of predicting the actual cycler capacity, the model predicted the expected capacity in SOC change, which showed high correlation with the features.
Correlation of expected_capacity_in_soc_change:
•	SOC change: 0.999890
•	BM_BattVoltage_std: 0.899755
•	Capacity added: 0.875162
•	Session duration: 0.786534
Using this approach, the model achieved an R² of 0.99986 with an MSE of 0.16147. The predicted value was then extrapolated to the actual predicted capacity (to match cycler capacity) using: (predicted capacity * 100 / change in SOC) (considering 100% soc). 
Last iteration Results discussed in last meeting: 
The model showed a difference of approximately 2 Ah between the day 0 capacity and the predicted capacity. This was attributed to smaller SOC changes during some charging sessions (with 80% of selected vehicles showing less than 20% SOC change). The model struggled with imbalanced data, penalizing infrequent values 
""")
# Fetch and display the histogram plot from GitHub
url_histogram = "https://raw.githubusercontent.com/CellintelLog9/SOH/main/histogram_soc_change.html"
response_histogram = requests.get(url_histogram)
if response_histogram.status_code == 200:
    st.components.v1.html(response_histogram.text, height=500)
else:
    st.error("Failed to load the histogram plot from GitHub.")
# Solution box
create_box("Solution", """
To improve accuracy, the dataset was segregated into three categories based on SOC change:

- **Category 1**: SOC Change 0-15
- **Category 2**: SOC Change 15-30
- **Category 3**: SOC Change > 30

Separate models were trained for each category, improving accuracy and reducing the difference to < 1 Ah.
""")


# Fetch and display the final plot from GitHub
url_final_plot = "https://raw.githubusercontent.com/CellintelLog9/SOH/main/cycler_vs_predicted_capacity.html"
response_final_plot = requests.get(url_final_plot)
if response_final_plot.status_code == 200:
    st.components.v1.html(response_final_plot.text, height=500)
else:
    st.error("Failed to load the final plot from GitHub.")
