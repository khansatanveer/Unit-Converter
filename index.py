import streamlit as st
import pandas as pd

# ✅ Page Setup
st.set_page_config(page_title="Universal Unit Converter", layout="wide")

# ✅ Initialize Session State for Conversion History
if "history" not in st.session_state:
    st.session_state.history = []

# ✅ Theme Switch (Dark & Custom Blue)
dark_mode = st.sidebar.toggle("🌙 Dark Mode", value=True)

theme_colors = {
    True: {"bg": "#1e1e2f", "text": "#fff", "label": "#FFFFFF"},
    False: {"bg": "#D6D6D6", "text": "#000", "label": "#222"}
}
selected_theme = theme_colors[dark_mode]

st.markdown(
    f"""
    <style>
    .stApp {{ background: {selected_theme["bg"]}; color: {selected_theme["text"]}; }}

    .convert-btn {{
        background: #007BFF; /* Bright Blue */
    color: white !important;
    padding: 12px 18px;
    border: none;
    border-radius: 30px; /* Soft rounded edges */
    cursor: pointer;
    font-size: 16px;
    font-weight: 600;
    text-align: center;
    width: 50%;  
    max-width: 200px; 
    margin-top: 20px;
    margin-bottom: 20px;
    box-shadow: 0px 3px 8px rgba(0, 123, 255, 0.3);
    transition: all 0.3s ease-in-out;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    outline: 2px solid rgba(255, 255, 255, 0.2);
}}

.convert-btn:hover {{
     background: #0056b3; /* Darker Blue on Hover */
    transform: translateY(-3px) scale(1.03);
    box-shadow: 0px 5px 12px rgba(0, 123, 255, 0.5);
    outline-color: rgba(255, 255, 255, 0.4);
}}

    .result-box {{ background: rgba(255, 255, 255, 0.2); padding: 15px; border-radius: 10px; text-align: center; }}
    label, h4 {{ color: {selected_theme["label"]} !important; font-weight: bold; }}
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1>🌍 Universal Unit Converter</h1>", unsafe_allow_html=True)

# ✅ Sidebar for Category Selection
st.sidebar.markdown("<h3 style='color:#FF5733;'>⚡ Choose Conversion Type</h3>", unsafe_allow_html=True)
conversion_type = st.sidebar.selectbox("", ["📏 Length", "🌡️ Temperature", "⚖️ Weight"])


# ✅ User Input for Value
st.markdown("<h4>🔢 Enter Value</h4>", unsafe_allow_html=True)
value = st.number_input("", min_value=0.0, value=0.0, format="%.2f")

# ✅ Unit Selection
length_units = ["Meter", "Kilometer", "Miles", "Centimeter", "Inches"]
temp_units = ["Celsius", "Fahrenheit", "Kelvin"]
weight_units = ["Kg", "Lb", "Gram", "Ounce"]

# ✅ Restrict 'Convert From' and 'Convert To' Based on Category
if conversion_type == "📏 Length":
    from_unit = st.selectbox("🔄 Convert From", length_units)
    valid_to_units = [unit for unit in length_units if unit != from_unit]
elif conversion_type == "🌡️ Temperature":
    from_unit = st.selectbox("🔄 Convert From", temp_units)
    valid_to_units = [unit for unit in temp_units if unit != from_unit]
elif conversion_type == "⚖️ Weight":
    from_unit = st.selectbox("🔄 Convert From", weight_units)
    valid_to_units = [unit for unit in weight_units if unit != from_unit]
else:
    from_unit = ""
    valid_to_units = []

st.markdown("<h4>➡️ Convert To</h4>", unsafe_allow_html=True)
to_unit = st.selectbox("", valid_to_units)

# ✅ Conversion Logic
def convert(value, from_unit, to_unit):
    conversions = {
        ("Meter", "Kilometer"): value / 1000, ("Kilometer", "Meter"): value * 1000,
        ("Miles", "Kilometer"): value * 1.609, ("Kilometer", "Miles"): value / 1.609,
        ("Meter", "Centimeter"): value * 100, ("Centimeter", "Meter"): value / 100,
        ("Inches", "Centimeter"): value * 2.54, ("Centimeter", "Inches"): value / 2.54,
        ("Celsius", "Fahrenheit"): (value * 9/5) + 32, ("Fahrenheit", "Celsius"): (value - 32) * 5/9,
        ("Celsius", "Kelvin"): value + 273.15, ("Kelvin", "Celsius"): value - 273.15,
        ("Kg", "Lb"): value * 2.20462, ("Lb", "Kg"): value / 2.20462,
        ("Kg", "Gram"): value * 1000, ("Gram", "Kg"): value / 1000,
        ("Lb", "Ounce"): value * 16, ("Ounce", "Lb"): value / 16
    }
    return conversions.get((from_unit, to_unit), None)

# ✅ Convert Button
if st.markdown("<div class='convert-btn' onclick='window.convertClick()'>🔥 Convert</div>",
unsafe_allow_html=True):
    result = convert(value, from_unit, to_unit)
    
    if result is None:
        st.error("❌ Invalid conversion! Please choose compatible units.")
    else:
        st.session_state.history.append([value, from_unit, result, to_unit])
        st.markdown(f"<div class='result-box'>✅ {value} {from_unit} = {result:.2f} {to_unit}</div>", unsafe_allow_html=True)
