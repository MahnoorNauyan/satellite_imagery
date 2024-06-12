from ultralytics import YOLO
import streamlit as st
import numpy as np
import cv2
from PIL import Image
import os



def output(image, confidence, st, name):
    # Use the trained model to predict the test result
    model = YOLO('./Weights/best.pt')

    file_path = os.path.join("output2/predict/labels/image0.txt")

    if os.path.exists(file_path):
        os.remove(file_path)
        
    results = model.predict(image, conf=confidence, save_txt=True, project="output2", name="", exist_ok=True)

    for result in results:
        st.image(result.plot())
    
    if os.path.exists(file_path):
        os.rename(file_path, os.path.join("output2/predict/labels", f"{name}.txt"))

def save_uploaded_file(uploaded_file, save_dir, filename):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    file_path = os.path.join(save_dir, filename)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

def run_app():
    img_file = st.file_uploader('Upload image (.jpg, .jpeg, .img)', type = [".jpg", ".jpeg", ".img", ".png"])
    st.subheader('Output Image')

    DEMO_IMAGE = './Image/Valencia_74.2522_31.39689.jpg'
    file_name="Valencia_74.2522_31.39689"

    if img_file is not None:
        img = cv2.imdecode(np.fromstring(img_file.read(), np.uint8), 1)
        image = np.array(Image.open(img_file))

    else:
        img = cv2.imread(DEMO_IMAGE)
        image = np.array(Image.open(DEMO_IMAGE))
        st.sidebar.text("Demo Image")
    
    if img_file != None:
        st.sidebar.text("Uploaded Image")
        # file_extension = img_file.name.split(".")[-1]
        file_name, file_extension = os.path.splitext(img_file.name)
        file = f"{file_name}{file_extension}"

        save_dir = "output2/predict/images"
        file_path = save_uploaded_file(img_file, save_dir, file)

        st.success(f"Image saved successfully at {file_path}")
    
    st.sidebar.image(img)
    st.sidebar.header("Parameters")
    confidence = st.sidebar.slider('Confidence:', min_value=0.0, max_value=1.0, value=0.4)
    output(img, confidence, st, file_name)
