from dependancies import *

def run_app():
    img_file = st.file_uploader('Upload image (.jpg, .jpeg, .img)', type = [".jpg", ".jpeg", ".img"])
    st.subheader('Output Image')

    DEMO_IMAGE = './Image/Valencia_74.2522_31.39689.jpg'

    if img_file is not None:
        img = cv2.imdecode(np.fromstring(img_file.read(), np.uint8), 1)
        image = np.array(Image.open(img_file))

    else:
        img = cv2.imread(DEMO_IMAGE)
        image = np.array(Image.open(DEMO_IMAGE))
        st.sidebar.text("Demo Image")
    
    if img_file != None:
        st.sidebar.text("Uploaded Image")
    
    st.sidebar.image(img)
    st.sidebar.header("Parameters")
    confidence = st.sidebar.slider('Confidence:', min_value=0.0, max_value=1.0, value=0.4)
    output(img, confidence, st)