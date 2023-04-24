import streamlit as st
import streamlit.components.v1 as components
from streamlit.logger import get_logger
import plotly.express as px
import pandas as pd

LOGGER = get_logger(__name__)


def run():

    st.set_page_config(
        page_title="LA neighborhood Recommender",
        page_icon="🏠️",
    )

    hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
    st.markdown(hide_menu_style, unsafe_allow_html=True)
    st.sidebar.text("")
    st.sidebar.success("👆️ Select an option above")
    st.sidebar.text("")
    st.sidebar.text("©️2023 Data Trojans")

    st.write("# Living Recommendation and Trend Prediction within the LA County")
    st.write("")

    st.markdown(
        """ 
            Most of the Southern California Counties have shown decreasing population trend recent years, with so called *"California Exodus"* (see graph below).
        """
    )
    st.markdown(
        """
            
            
            This web application aims to help you find what is the best city/neighborhood to live in within LA county based on your goals and preferences to make your life easier and more enjoyable!


    	"""
    )

    st.write("")

    socal_pop = pd.read_csv('final_dataset/socal_pop.csv')

    fig = px.line(socal_pop, x='Year', y='Normalized Population',
                  color='County', hover_data=['Population'], markers=True)
    fig.update_layout(plot_bgcolor='white')
    fig.update_layout(
        title={
            'text': "Southern California County Population Trend",
            'y': 0.95,
            'x': 0.445,
            'xanchor': 'center',
            'yanchor': 'top'},
        xaxis=dict(
            showgrid=True,
            gridwidth=0.5,
            gridcolor='grey',
            griddash='dash',
            mirror=True,
            ticks='outside',
            showline=True,
            tickmode='linear',
            linecolor='black',
            linewidth=1),
        yaxis=dict(
            mirror=True,
            ticks='outside',
            showline=True,
            linecolor='black',
            linewidth=1),
        font=dict(
            family="Times New Roman",
            size=15,
            color="Black"))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        """
			### Avaiable features:
			- Get a recommendation on living areas based on your preferences
			- Future trends forecasting on living areas
			- Explore the data and discover on your own
		"""
    )

    st.text("")

    st.markdown(
        """
            **👈 Select an option from the sidebar** to see what you can do!
        """
    )

    st.text("")

    st.markdown(
        """
            Whether you want to settle in as a young family, work hard and save up money, live a balanced life, this application provides you with the tools to find a place to live that will support you in that lifestyle.
            
            City Officials and Investors can leverage the application using the interactive data exploration tools and the deep learning based neighborhood growth forecasting result to support their decision making. 
        """
    )
    st.text("")

    # st.text("")

    # video_file = open('Assets/stars-6962.mp4', 'rb')
    # video_bytes = video_file.read()
    # st.video(video_bytes)

    st.text("")

    st.markdown(
        """
			##### 👉️ Check out [the GitHub repo](https://github.com/mitorax/dsci-560-project)
		"""
    )


if __name__ == "__main__":
    run()
