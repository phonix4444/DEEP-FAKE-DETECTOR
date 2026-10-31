import streamlit as st
from transformers import pipeline
from PIL import Image
import torch

st.set_page_config(page_title='Ultimate Deepfake & AI Forensics Pro', page_icon='🕵️‍♂️', layout='centered')
st.title('🕵️‍♂️ Ultimate Deepfake & AI Forensics Pro')
st.markdown('Enterprise-grade forensic image analysis powered by a multi-model AI neural ensemble.')

@st.cache_resource
def load_ensemble():
    # Load three complementary state-of-the-art vision models for maximum forensic precision
    m1 = pipeline('image-classification', model='dima806/deepfake_vs_real_image_detection')
    m2 = pipeline('image-classification', model='umm-maybe/AI-image-detector')
    m3 = pipeline('image-classification', model='Organika/sdxl-detector')
    return m1, m2, m3

with st.spinner('Loading triple-model AI neural forensic ensemble...'):
    model1, model2, model3 = load_ensemble()

uploaded_file = st.file_uploader('Upload photo or face image...', type=['jpg', 'jpeg', 'png', 'webp'])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert('RGB')
    st.image(image, caption='Target Image for Forensic Scan', use_column_width=True)
    
    if st.button('Execute Deep Forensic Scan', type='primary'):
        with st.spinner('Running multi-layer neural network analysis...'):
            r1 = model1(image)
            r2 = model2(image)
            r3 = model3(image)
            
            fake_score = 0.0
            real_score = 0.0
            
            # Weighted ensemble aggregation (Model 1: 45%, Model 2: 35%, Model 3: 20%)
            for r in r1:
                lbl = r['label'].lower()
                if 'fake' in lbl or 'ai' in lbl or 'artificial' in lbl or 'sdxl' in lbl:
                    fake_score += r['score'] * 0.45
                else:
                    real_score += r['score'] * 0.45
                    
            for r in r2:
                lbl = r['label'].lower()
                if 'fake' in lbl or 'ai' in lbl or 'artificial' in lbl:
                    fake_score += r['score'] * 0.35
                else:
                    real_score += r['score'] * 0.35
                    
            for r in r3:
                lbl = r['label'].lower()
                if 'fake' in lbl or 'ai' in lbl or 'artificial' in lbl:
                    fake_score += r['score'] * 0.20
                else:
                    real_score += r['score'] * 0.20
            
            st.markdown('---')
            st.subheader('📊 Forensic Analysis Verdict')
            
            if fake_score > real_score:
                st.error('🚨 **RESULT: AI-Generated / Deepfake Detected**')
                st.metric('Manipulation Probability', f'{fake_score * 100:.2f}%')
            else:
                st.success('✅ **RESULT: Authentic / Real Photograph**')
                st.metric('Authenticity Probability', f'{real_score * 100:.2f}%')
                
            st.progress(float(max(fake_score, real_score)))
            
            with st.expander('🔬 Advanced Neural Breakdown'):
                st.write('**Model 1 (Deepfake vs Real Vision):**', r1)
                st.write('**Model 2 (AI Artifact Classifier):**', r2)
                st.write('**Model 3 (SDXL / Synth Detector):**', r3)
