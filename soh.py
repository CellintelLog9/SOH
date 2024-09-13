import streamlit as st

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
    </style>
    """, unsafe_allow_html=True)

# Title of the presentation app
st.title("Project Presentation")

# Manufacturing Process box
st.markdown('<div class="box">', unsafe_allow_html=True)
st.subheader("Manufacturing Process")
st.markdown("""
1. **Initial Cell Cycling**: Each cell undergoes an individual cycling process to gather essential data. This data is input into the cell acer system, which categorizes cells into appropriate buckets based on their performance metrics.

2. **Pack Assembly**: After categorization, the cells are assembled into battery packs.

3. **Pack Cycling**: Once assembled, the entire pack is cycled again to measure the overall capacity and ensure compliance with performance standards. Additionally, the functionality of the BMS is tested using Pack Acer.

4. **8k and 2k Pack Testing**:
    - **8k Pack**: The BMS is attached inside the battery pack. The testing process shows the actual capacity in the pack cycler data, with cut-off voltages set between 2.7V (max) and 1.7V (min).
    - **2k Pack**: The BMS is housed inside the ICC kit, with the lower-end cut-off voltage set between 2.7V (max) and 1.95V (min).

After testing, the cycler data, BMS data, and acceptance criteria are reviewed. The true capacity is derived from the cycler data, while the BMS data also provides capacity values using coulomb counting.
""")
st.markdown('</div>', unsafe_allow_html=True)

# Add the plot as an HTML component from GitHub
st.components.v1.html(
    '<iframe src="https://github.com/CellintelLog9/SOH/blob/main/line_chart_current3.html" width="700" height="500"></iframe>',
    height=500,
)

# ML Model Development Process box
st.markdown('<div class="box">', unsafe_allow_html=True)
st.subheader("ML Model Development Process")

st.markdown("""
### Step 1: Data Collection
- Data was fetched from custom reports where the charge-discharge cycle was less than 30.
- 193 packs were analyzed, and outliers were removed, leaving 22 packs for validation with custom reports, cycler, and BMS data.

### Step 2: Data Preprocessing
- Identified charging zones where current > 0 in the Telematics data.
- Joined custom reports with cycler and BMS data.

### Step 3: Data Transformation
- Calculated mean, median, min, max for voltage, current, SOC%, temperatures, and other features.
- Derived capacity on day zero using both cycler and BMS data.

""")
st.markdown('</div>', unsafe_allow_html=True)

# Model Training Approaches box
st.markdown('<div class="box">', unsafe_allow_html=True)
st.subheader("Model Training Approaches")

st.markdown("""
### 1st Approach:
- Features: Mean, median, min, max for voltage, current, temperatures, and SOC%.
- Target: Pack cycler capacity.
- Result: No significant correlation was identified between input features and cycler capacity.

### 2nd Approach:
- New features such as SOC change and capacity added per zone were added.
- The model predicted expected capacity in SOC change, which showed a high correlation with features.

**Correlation of expected capacity in SOC change:**
- SOC change: 0.999890
- BM_BattVoltage_std: 0.899755
- Capacity added: 0.875162

The model achieved an R² of 0.99986 with an MSE of 0.16147.
""")
st.markdown('</div>', unsafe_allow_html=True)

# Add another plot from GitHub
st.components.v1.html(
    '<iframe src="https://github.com/CellintelLog9/SOH/blob/main/histogram_soc_change.html" width="700" height="500"></iframe>',
    height=500,
)

# Solution box
st.markdown('<div class="box">', unsafe_allow_html=True)
st.subheader("Solution")

st.markdown("""
To improve accuracy, the dataset was segregated into three categories based on SOC change:

- **Category 1**: SOC Change 0-15
- **Category 2**: SOC Change 15-30
- **Category 3**: SOC Change > 30

Separate models were trained for each category, improving accuracy and reducing the difference to < 1 Ah.
""")
st.markdown('</div>', unsafe_allow_html=True)

# Add final plot
st.components.v1.html(
    '<iframe src="https://github.com/CellintelLog9/SOH/blob/main/cycler_vs_predicted_capacity.html" width="700" height="500"></iframe>',
    height=500,
)
