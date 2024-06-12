from dependancies import *
from login import *

def home():
    st.markdown("""Welcome to the **Property Tax Calculator App**. This App will calculate property tax of your house. Wondering how this works? You just need to simply upload satellite image of your house and the app will do the rest. 
        Our App runs on a pre-trained **YOLOv8** model.""")
    
    # user_dash = st.button('User Dashboard')
    # if user_dash:
    #     try:
    #         while True:
    #             user_dashboard()
    #     except TypeError as e:
    #         if '\'NoneType\' object is not subscriptable' in str(e):
    #             st.error('Please login first.')