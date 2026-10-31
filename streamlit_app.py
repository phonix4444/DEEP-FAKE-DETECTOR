import streamlit as st
from transformers import pipeline
from PIL import Image

st.set_page_config(page_title='AI & Real Photo Detector', page_icon='🔍', layout='centered')
st.title('AI & Real Photo Detector')
st.markdown('Simple, reliable detection for AI-generated and Real photographs.')

@st.cache_resource
def load_detector():
    return pipeline('image-classification', model='dima806/deepfake_vs_real_image_detection')

with st.spinner('Initializing detector...'):
    detector = load_detector()

uploaded_file = st.file_uploader('Choose an image...', type=['jpg', 'jpeg', 'png', 'webp'])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert('RGB')
    st.image(image, caption='Uploaded Image', use_column_width=True)
    
    if st.button('Analyze Image', type='primary'):
        with st.spinner('Analyzing...'):
            try:
                results = detector(image)
                
                ai_score = 0.0
                real_score = 0.0
                
                for item in results:
                    lbl = item.get('label', '').lower()
                    score = float(item.get('score', 0.0)) * 100
                    if 'fake' in lbl or 'ai' in lbl or 'artificial' in lbl or 'deepfake' in lbl:
                        ai_score = score
                    else:
                        real_score = score
                        
                if ai_score == 0.0 and real_score == 0.0:
                    top = max(results, key=lambda x: x.get('score', 0))
                    top_score = float(top.get('score', 0.0)) * 100
                    if 'fake' in top.get('label', '').lower() or 'ai' in top.get('label', '').lower():
                        ai_score = top_score
                        real_score = 100.0 - top_score
                    else:
                        real_score = top_score
                        ai_score = 100.0 - top_score
                elif ai_score > 0 and real_score == 0:
                    real_score = 100.0 - ai_score
                elif real_score > 0 and ai_score == 0:
                    ai_score = 100.0 - real_score
                    
                st.markdown('---')
                st.subheader('Results')
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric(label='AI / Deepfake', value=f'{ai_score:.1f}%')
                with col2:
                    st.metric(label='Real Photo', value=f'{real_score:.1f}%')
                    
                st.markdown('### Verdict:')
                if ai_score > real_score:
                    st.error(f'This image is likely **AI-Generated / Deepfake** ({ai_score:.1f}% confidence).')
                else:
                    st.success(f'This image is likely a **Real Photograph** ({real_score:.1f}% confidence).')
            except Exception as e:
                st.error(f'Error: {e}')
