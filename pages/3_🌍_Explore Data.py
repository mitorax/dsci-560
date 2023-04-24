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
        df = pd.read_csv("final_dataset/acs2017_county_data.csv")
        df = df.loc[df['State'] == 'California'].reset_index(drop=True)
        return df.set_index("County")

    try:
        df = get_census_data()
        selected = st.multiselect(
            "Choose counties 👇️", list(df.index), [
                "Los Angeles County", "Orange County"]
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


@st.cache_data
def get_data(filename, index):
    df = pd.read_csv("final_dataset/" + filename + ".csv")
    df = df.set_index(index)

    return df


def show_table(df, title):
    st.write("### " + title, df.sort_index())
    st.write("")
    st.write("")
    df = pd.melt(df)


st.set_page_config(page_title="Explore Data", page_icon="📊")
st.markdown("# Explore Data")
st.write("")
st.sidebar.header("Explore Data")
st.sidebar.text("[add descritption]")
st.write(
    """Select which data you want to look at from the tabs below 👇️"""
)
st.write("")

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(
    ["Census", "Parks & Recreation", "Crime", "Education", "Medical Facilities", "Population", "Employment"])

# Census
with tab1:
    st.write("")
    st.write("")
    census_data()

# Parks
with tab2:
    st.write("")
    st.write("")

    park = pd.read_csv("final_dataset/park_facilities_la.csv")
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

    st.write("")
    st.write("")
    parks = get_data(filename="park_facilities_la", index="CouncilDistrict")
    show_table(parks, "LA Parks And Recreational Facilities Data")

# Crime
with tab3:
    st.write("")
    st.write("")
    crime_years = st.slider(
        'Crime Years:', 2010, 2023, (2010, 2023))

    st.write("")
    st.write("")

    crime_occ = pd.read_csv('final_dataset/LA_crime_occ.csv')
    if crime_years[0] != 2010 or crime_years[1] != 2023:
        crime_occ = crime_occ[crime_occ["year"].le(
            crime_years[1]-1) & crime_occ["year"].ge(crime_years[0])]

    fig = px.line(crime_occ, x='year', y='occurences', markers=True)
    fig.update_layout(plot_bgcolor='white')
    fig.update_layout(
        title={
            'text': "Los Angeles County Crime occurences trend",
            'y': 0.99,
            'x': 0.55,
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

# Education
with tab4:
    st.header("Education")

# Hospital
with tab5:
    hospitals = get_data("hospital_facility_la", "City")
    hospitals = hospitals[["Name", "Address", "URL"]]
    cities = hospitals.index.fillna("Los Angeles")
    selected_hospitals = st.multiselect(
        "Filter by City 👇️", sorted(set(cities)))
    if not selected_hospitals:
        show_table(hospitals, "LA Medical Centers and Facilities")

    else:
        hospitals = hospitals.loc[selected_hospitals]
        show_table(hospitals, "LA Medical Centers and Facilities")

# Population
with tab6:
    st.write("Population")

# Employment
with tab7:
    st.write("Employment")
