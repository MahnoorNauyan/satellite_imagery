from dependancies import *
from home import *
from login import *
from model import *
from about import *
from model import *
from draw_poly import *
from tax_potential import *
from dashboard import *

def main():
    st.set_page_config(
        page_title="Property Tax Calculator",
        page_icon="house",
        layout="wide",
    )

    st.title("Property Tax Calculator App")


    st.sidebar.title("Menu")
    app_mode = st.sidebar.selectbox('Get Started:', ['User', 'Home', 'Run Model', 'Show Polygon','Show tax for 2 story houses', 'Tax Potential', 'Dashboard','About'])

    if app_mode == 'User':
        login()
    
    elif app_mode == 'About':
        about()
        
    elif app_mode == "Run Model":
        run_app()

    elif app_mode == "Show Polygon":
        poly()

    elif app_mode == "Show tax for 2 story houses":
        double_storey_tax()        

    elif app_mode == "Tax Potential":
        tax_potential()
    
    elif app_mode == "Dashboard":
        dashboard()
        
    else:
        home()

if __name__ == "__main__":
    try:
        main()
    except SystemError:
        pass
