import streamlit as st
import pandas as pd
import joblib

# Load model and scaler
model = joblib.load("crop_svm_model.pkl")
scaler = joblib.load("crop_scaler.pkl")

st.set_page_config(
    page_title="Sowing Success",
    page_icon="🌾",
    layout="centered"
)

st.title("🌾 Sowing Success")
st.subheader("AI Crop Recommendation System")

st.write(
    "Enter soil nutrient values and pH level to receive a crop recommendation."
)

# Inputs
N = st.number_input("Nitrogen (N)", min_value=0.0)
P = st.number_input("Phosphorus (P)", min_value=0.0)
K = st.number_input("Potassium (K)", min_value=0.0)
ph = st.number_input("pH Level", min_value=0.0, max_value=14.0)

if st.button("Predict Crop"):

    input_data = pd.DataFrame(
        [[N, P, K, ph]],
        columns=["N", "P", "K", "ph"]
    )

    scaled_input = scaler.transform(input_data)

    prediction = model.predict(scaled_input)[0]

    st.success(f"Recommended Crop: {prediction}")

    if hasattr(model, "predict_proba"):
        confidence = model.predict_proba(scaled_input).max() * 100
        st.info(f"Confidence: {confidence:.2f}%")

st.divider()

st.markdown("""
### About the Model

- Algorithm: Support Vector Machine (RBF Kernel)
- Features: Nitrogen, Phosphorus, Potassium, pH
- Dataset: 2,200 soil samples
- Classes: 22 crop types
- Accuracy: 73%

### Key Insight

Potassium (K) was identified as the strongest individual predictor of crop type.
""")