import streamlit as st
from transformers import pipeline
from PIL import Image

st.set_page_config(page_title="Deepfake & AI Image Detector", page_icon="🔍", layout="centered")
st.title("🔍 Deepfake & AI Image Detector")
st.markdown("Upload an image below to detect whether it is **Real** or **AI-Generated / Deepfake**.")

@st.cache_resource
def load_model():
    return pipeline("image-classification", model="umm-maybe/AI-image-detector")

with st.spinner("Loading AI detection model..."):
    detector = load_model()

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_column_width=True)
    if st.button("Detect Deepfake"):
        with st.spinner("Analyzing..."):
            results = detector(image)
            for res in results:
                label = res['label']
                score = res['score']
                display_label = "🤖 AI-Generated / Deepfake" if label.lower() in ["artificial", "ai", "fake", "generated"] else "👤 Real Image"
                st.metric(label=display_label, value=f"{score * 100:.2f}%")
