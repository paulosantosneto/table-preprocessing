import streamlit as st
import fitz
from preprocessing import Methods
from PIL import Image
import numpy as np
import cv2
import zipfile
import io
import matplotlib.pyplot as plt

def app(): 
    
    st.session_state.image = st.file_uploader('', type=['png', 'jpg'])
    
    if st.session_state.image is not None:
        #print(st.session_state.image.read())
        #st.session_state.image = Methods(fitz.open(stream=st.session_state.image.read(), filetype="png"))
        file_bytes = np.asarray(bytearray(st.session_state.image.read()), dtype=np.uint8)
        st.session_state.image = Methods(image=cv2.imdecode(file_bytes, 1))
        st.image(st.session_state.image.get_image(), channels="RGB")
        st.session_state.image_received = True
        #print(st.session_state.image.get_image())

def check_states():

    if "image_received" not in st.session_state:
        st.session_state.image_received = False
    
    if "image" not in st.session_state:
        st.session_state.image = None

    if "methods_selected" not in st.session_state:
        st.session_state.methods_selected = []
    
    if "images" not in st.session_state:
        st.session_state.images = []
    
    if "zipimages" not in st.session_state:
        st.session_state.zipimages = None

def select_methods():
    
    st.success('Selected image!')
    st.session_state.methods_selected = st.multiselect('', ['Rotation', 'Remove Noise'])
        
    if len(st.session_state.methods_selected) > 0:
        button = st.button('Start Preprocessing')
        if button and st.session_state.methods_selected != None and len(st.session_state.methods_selected) > 0:
            st.session_state.image.run_methods(st.session_state.methods_selected)
            st.session_state.images = st.session_state.image.run_streamlit()
            st.session_state.zipimages = zipimages(st.session_state.images)
        if len(st.session_state.images) > 0:
            show_images = st.button('Show Images')
            if show_images:
                for image in st.session_state.images:
                    st.image(image, channels="RGB")
            download_images = st.download_button(label="Download ZIP", data=st.session_state.zipimages, file_name="myfile.zip", mime="application/zip")
    else:
        st.session_state.images = []

def zipimages(images):
    
    zip_buf = io.BytesIO()
    with zipfile.ZipFile(file=zip_buf, mode='w', compression=zipfile.ZIP_DEFLATED) as z:
        for i,fig in enumerate(images):
            buf = io.BytesIO()
            fig = plt.imshow(fig)
            plt.axis('off')
            fig.figure.savefig(buf, format='png', bbox_inches='tight')
            filename = f'orientation_{i}.png'
            z.writestr(zinfo_or_arcname=filename, data=buf.getvalue() )
            buf.close()
    
    buf = zip_buf.getvalue()
    zip_buf.close()
    return buf

if __name__ == '__main__':
    st.title('Table Preprocessing')
    st.markdown("**Methods used**")
    st.markdown("1. Rotation")
    st.markdown("2. Remove Noise")
    st.markdown("**How it works?** Choose one or more methods to apply to the inserted image. At the end of processing, a new image will be returned with the results of the application.")
    app()
    check_states()
    if st.session_state.image != None:
        select_methods()
        
    
    
    