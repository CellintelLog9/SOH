import streamlit as st
import requests
st.set_page_config(layout="wide")
# Add custom CSS for box styling with box shadow and transparency
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
st.title("Project Update")

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

1. **Initial Cell Cycling**: Each cell undergoes individual cycling to gather essential data, which is input into the cell acer system. Cells are categorized into appropriate buckets based on performance metrics.

2. **Pack Assembly**: After categorization, cells are assembled into battery packs.

3. **Pack Cycling**: The assembled pack is cycled to measure the overall capacity and ensure compliance with performance standards. Additionally, the BMS functionality is tested using Pack Acer.

4. **8k and 2k Pack Testing**:
    - **8k Pack**: The BMS is attached inside the pack, with cut-off voltages between 2.7V (max) and 1.7V (min).
    - **2k Pack**: The BMS is housed in the ICC kit, with lower-end cut-off voltage between 2.7V (max) and 1.95V (min).

Following the testing, the cycler data, BMS data, and acceptance criteria are reviewed. The true capacity is derived from the cycler data, while the BMS data can also provides capacity values using coulomb counting by filtering the BMS data using Timestamp of cycler file (Plot Below of Current (I) data between cycler and BMS ). However, there is a noticeable difference between the cycler and BMS capacities, primarily due to current calibration discrepancies and power cut , with the BMS reporting larger current values compared to the cycler(Current (I) plot below).
""")

# Fetch and display the plot from GitHub
url = "https://raw.githubusercontent.com/CellintelLog9/SOH/main/line_chart_current3.html"
response = requests.get(url)
if response.status_code == 200:
    st.components.v1.html(response.text, height=500)
else:
    st.error("Failed to load the plot from GitHub.")

# ML Model Development Process box
create_box("Development Process", """

 Step 1: Data Collection
Data was fetched from custom reports where the charge-discharge cycle was less than 30. The telematics ID was mapped to the corresponding battery number, and outliers were removed, 
resulting in 193 packs out of which 22 packs for validation with available custom reports, cycler, and BMS data

 Step 2: Data Preprocessing
- Identified charging zones where current > 0 in Telematics data.
- Sorted data by datetime for each Telematics ID and assigned unique numbers to each charging session.
- Joined custom reports with cycler and BMS files, generated simultaneously during pack testing.

### Step 3: Data Transformation
For each charging session, the following values were identified:
- Mean, median, minimum, maximum of voltage, current, maximum and minimum monomer temperatures, SOC%, and device date.
- Values for charge-discharge cycles, capacity on day zero from both cycler and BMS (calculated via coulomb counting), average current, and time duration of step 8 in the BMS.

""")

# Model Training Approaches box
create_box("Model Training Approaches", """
 1st Approach:
 
- **Features**: Mean, median, min, max for voltage, current, temperatures, and SOC%.
- **Target**: Pack cycler capacity.
- **Result**: No significant correlation between input features and cycler capacity.

| Feature                | Correlation  |
|------------------------|--------------|
| capacity_first          | 1.000000     |
| BM_BattCurrrent_std     | 0.039267     |
| BM_SocPercent_max       | -0.001158    |
| BM_BattVoltage_min      | -0.005754    |
| SOC Change              | -0.001259    |
| session_duration        | -0.011942    |
""")

# Second approach box
create_box("Second Approach", """
A new set of features was added: SOC change (SOC percent max – SOC percent min) for each charging zone, expected capacity in SOC change, and capacity added per zone. Instead of predicting actual cycler capacity, we predicted expected capacity in SOC change, which had a high correlation with features:

| Feature               | Correlation  |
|-----------------------|--------------|
| SOC Change            | 0.999890     |
| BM_BattVoltage_std     | 0.899755     |
| Capacity Added         | 0.875162     |
| Session Duration       | 0.786534     |

This approach achieved an **R²** of 0.99986 with an **MSE** of 0.16147.

The predicted value was extrapolated to match cycler capacity using: `predicted capacity * 100 / SOC change`. However, 
the model showed a ~2 Ah difference between day 0 and predicted capacity due to smaller SOC changes in many sessions, 
resulting in imbalanced data (SoC change distribution in below plot).
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
To address this, the dataset was segregated into three categories based on SOC change and adding transformation on minorities 
and adding one more hidden layer along with increased number of neurons and epoch.

- **Category 1**: SOC Change 0-15.
- **Category 2**: SOC Change 15-30.
- **Category 3**: SOC Change > 30.

Separate models were trained for each category and their results were merged. 
This improved the accuracy, reducing the difference to < 1 Ah.

""")


create_box("Next Step", """
- The next step will be validating the model on Bosch's vehicle data with regularization by considering all charging sessions and will observe how the pack capacity has changed over time
""")


# Fetch and display the final plot from GitHub
url_final_plot = "https://raw.githubusercontent.com/CellintelLog9/SOH/main/cycler_vs_predicted_capacity.html"
response_final_plot = requests.get(url_final_plot)
if response_final_plot.status_code == 200:
    st.components.v1.html(response_final_plot.text, height=500)
else:
    st.error("Failed to load the final plot from GitHub.")


# Fetch and display the final plot from GitHub
url_final_plot = "https://raw.githubusercontent.com/CellintelLog9/SOH/main/difference_between_cycler_and_predicted_capacity.html"
response_final_plot = requests.get(url_final_plot)
if response_final_plot.status_code == 200:
    st.components.v1.html(response_final_plot.text, height=500)
else:
    st.error("Failed to load the final plot from GitHub.")
