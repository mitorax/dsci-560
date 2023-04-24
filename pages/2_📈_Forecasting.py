import streamlit as st
import time
import numpy as np
from PIL import Image


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


st.set_page_config(page_title="Forecasting", page_icon="📈")
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

st.markdown("# Forecasting")
st.write("")
# st.sidebar.header("Forecasting")

st.write(
    """
    In this page, we show both the county-level and city/neighborhood growth forecasting result in LA county.
    
    Normally, when referring to city growth, it only projects population growth.
    However, in order to consider multiple aspects of the city, we propose an index that will effectively project city's growth trend that takes `Opportunity`, `Affordability`, and `Safety` into account.
    
    """
)
st.text("")

oasi_components = Image.open('Assets/oasi_components_trend.png')
st.text("")
st.text("")
st.image(oasi_components, caption='OASI Component Trend')

st.write("")
st.markdown("#### How our Growth Index works")
st.write("")

st.write(
    """
    We will define this index as OASI(Opportunity, Affordability, Safety Index).
    """
)
st.text("")

st.markdown(
    """
           $$OASI = {\t{employment rate} \over \t{unemployment rate} + \t{cpi indexes} + \t{crime rate}}$$ 
        """
)

oasi_trend = Image.open("Assets/oasi_trend.png")
st.text("")
st.text("")
st.image(oasi_trend, caption='OASI Trend')

st.text("")

st.markdown(
    """
            As it is challenging to get specific economic indicator datasets for neighborhood level, we will build a time series model to project
            county-levle growth trend using:

            - CPI indexes
            - Employment stats 
            - Crime dataset
            - Population dataset

        """
)

xgb = Image.open("Assets/xgboost_forecast.png")
st.text("")
st.text("")
st.image(xgb, caption='XGBoost Forecast Results')

st.write("")
st.markdown(
    """
            Then, using this model we will approximate the city/neighborhood-level growth trend using neighborhood specific datsets, such as:

            - Income per capita
            - Proximity to Hospitals/Parks/Social places
            - Population density data

            Finally, we add explainability of how we derived the neighborhood OASI forecasting result:
        """
)


shap = Image.open("Assets/shap.png")
st.text("")
st.text("")
st.image(shap)


# plotting_demo()


st.text("")

st.markdown("#### Neighborhoods with best Potential from our model")

st.markdown(
    """
            - Long Beach
            - Pasadena
            - Santa Clarita
            - Torrance
            - Glendale
    """
)


st.markdown("#### Examples of Neighborhood level forecasting")


st.success('Good potential: Long Beach!', icon="✅")
# st.markdown(
#     """
#             - Good potential: Long Beach
#         """
# )

lb = Image.open("final_dataset/longbeach.png")
st.text("")
st.text("")
st.image(lb)


st.error('Bad potential: Hollywood', icon="🚨")
# st.markdown(
#     """
#             - Bad potential: Hollywood
#         """
# )

hw = Image.open("final_dataset/hollywood.png")
st.text("")
st.text("")
st.image(hw)


# show_code(plotting_demo)
