import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import matplotlib.pyplot as plt

from urllib.error import URLError


def census_data():
    @st.cache_data
    def get_census_data():
        # AWS_BUCKET_URL = "http://streamlit-demo-data.s3-us-west-2.amazonaws.com"
        # df = pd.read_csv(AWS_BUCKET_URL + "/agri.csv.gz")
        df = pd.read_csv("Datasets_raw/acs2017_county_data.csv")
        return df.set_index("County")

    try:
        df = get_census_data()
        selected = st.multiselect(
            "Choose counties 👇️", list(df.index), [
                "Los Angeles County"]
        )
        if not selected:
            st.error("Please select at least one county.")
        else:
            data = df.loc[selected]
            # data /= 1000000.0
            st.write("### Census County Data 2017",
                     data.sort_index())

            data = pd.melt(data)

            # data = data.T.reset_index()
            # data = pd.melt(data, id_vars=["index"]).rename(
            #     columns={"index": "year",
            #              "value": "Gross Agricultural Product ($B)"}
            # )
            # chart = (
            #     alt.Chart(data)
            #     .mark_area(opacity=0.3)
            #     .encode(
            #         x="year:T",
            #         y=alt.Y("Gross Agricultural Product ($B):Q", stack=None),
            #         color="Region:N",
            #     )
            # )
            # st.altair_chart(chart, use_container_width=True)

    except URLError as e:
        st.error(
            """
            **Something went wrong: %s
        """
            % e.reason
        )


st.set_page_config(page_title="Explore Data", page_icon="📊")
st.markdown("# Explore Data")
st.sidebar.header("Explore Data")
st.sidebar.text("[add descritption]")
st.write(
    """Select which data you want to look at from the tabs below 👇️"""
)

tab1, tab2, tab3, tab4 = st.tabs(
    ["Census", "Parks & Recreation", "Crime", "Education"])

with tab1:
    st.write("")
    st.write("")
    census_data()


with tab2:
    st.write("")
    st.write("")

    park = pd.read_csv("Datasets_raw/park_facilities_la.csv")
    fig = px.histogram(park, x="LocationType")
    fig.update_traces(marker_line=dict(width=2.5, color='black'))
    fig.update_layout(paper_bgcolor="white",
                      plot_bgcolor='white')
    fig.update_xaxes(tickangle=-90)
    fig.update_layout(
        width=500,
        height=500,
        title={
            'text': 'Type of Parks and Recreation in LA county',
            'y': 0.975,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        showlegend=False,
        xaxis=dict(
            mirror=True,
            ticks='outside',
            title='Location Type',
            tickmode='linear',
            showline=True,
            linecolor='black',
            linewidth=2.5),
        yaxis=dict(
            mirror=True,
            ticks='outside',
            showline=True,
            title='count',
            titlefont=dict(size=20),
            linecolor='black',
            linewidth=2.5),
        font=dict(
            family="Times New Roman",
            size=20,
            color="Black"
        ))
    st.plotly_chart(fig, use_container_width=True)


with tab3:
    st.header("Crime")
    st.image("https://static.streamlit.io/examples/owl.jpg", width=200)

with tab4:
    st.header("Education")
