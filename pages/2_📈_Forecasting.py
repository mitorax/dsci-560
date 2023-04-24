import streamlit as st
import time
import numpy as np
from utils import show_code


def plotting_demo():
    progress_bar = st.sidebar.progress(0)
    status_text = st.sidebar.empty()
    last_rows = np.random.randn(1, 1)
    chart = st.line_chart(last_rows)

    for i in range(1, 101):
        new_rows = last_rows[-1, :] + np.random.randn(5, 1).cumsum(axis=0)
        status_text.text("%i%% Complete" % i)
        chart.add_rows(new_rows)
        progress_bar.progress(i)
        last_rows = new_rows
        time.sleep(0.05)

    progress_bar.empty()

    # Streamlit widgets automatically run the script from top to bottom. Since
    # this button is not connected to any other logic, it just causes a plain
    # rerun.
    st.button("Re-run")


st.set_page_config(page_title="Forecasting", page_icon="📈")
st.markdown("# Forecasting")
st.sidebar.header("Forecasting")
st.write(
    """
    In this page, we show both the county-level and city/neighborhood growth forecasting result in LA county.
    
    Normally, when referring to city growth, it only projects population growth.
    However, in order to consider multiple aspects of the city, we propose an index that will effectively project city's growth trend that takes `Opportunity`, `Affordability`, and `Safety` into account.
    
    We will define this index as OASI(Opportunity, Affordability, Safety Index).
    
    """
)
st.text("")

st.markdown(
        """
           $$OASI = {\t{employment rate} \over \t{unemployment rate} + \t{cpi indexes} + \t{crime rate}}$$ 
        """
)

st.text("")

st.markdown(
        """
            As it is challenging to get specific economic indicator datasets for neighborhood level, we will build a time series model to project
            county-levle growth trend using:

            - CPI indexes
            - Employment stats 
            - Crime dataset
            - Population dataset

            Then, using this model we will approximate the city/neighborhood-level growth trend using neighborhood specific datsets, such as:

            - Housing price trend
            - Proximity to Hospitals/Parks/Social places
            - Census data
            - And more...

        """
)

plotting_demo()


st.text("")

st.markdown(
        """
            Neighborhoods with best Potential from our model:

            - Long Beach
            - Pasadena
            - Santa Clarita
            - Torrance
            - Glendale
            - ...
        """
)

# show_code(plotting_demo)
