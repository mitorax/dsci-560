

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import geopandas as gpd


@st.cache_data
def get_data(path, sample=False, sample_size=None):
    if sample:
        return pd.read_csv(path, engine='pyarrow').sample(frac=sample_size, random_state=1)

    return pd.read_csv(path, engine='pyarrow')


def make_map(
    selected_data,
    fig,
    park,
    cs,
    cs_sample,
    parks_size,
    parks_alpha,
    crime_size,
    crime_alpha,
    crime_years,
    hospitals_marker_size,
    hospitals_marker_alpha,
    social_marker_size,
    social_marker_alpha,
    selected_neighb
):

    # print(selected_data)

    if crime_years[0] != 2010 or crime_years[1] != 2023:
        cs['DATE OCC'] = pd.to_datetime(cs['DATE OCC'])
        cs = cs[cs["DATE OCC"].dt.year.le(
            crime_years[1]) & cs["DATE OCC"].dt.year.ge(crime_years[0])]
    else:
        cs = cs_sample

    # print(cs.shape[0])

    if len(selected_neighb):
        neighb = neighborhoods.loc[neighborhoods['name'] == selected_neighb[0]]
        fig = px.choropleth_mapbox(
            neighb,
            geojson=neighb.geometry,
            locations=neighb.index,
            # color_continuous_scale="Teal",
            color='name',
            color_discrete_map={selected_neighb[0]: 'rgba(179,205,227,0.5)'},
            mapbox_style="carto-positron",
            center={"lat": 34.0215432, "lon": -118.2855741}
        )
    else:
        fig = go.Figure(go.Scattermapbox())
    if "Parks" in selected_data:
        fig.add_scattermapbox(
            lat=park['GeoLat'],
            lon=park['GeoLong'],
            mode='markers',
            name='Parks',
            marker=go.scattermapbox.Marker(
                size=parks_size,
                color='rgba(99,110,250,' + str(parks_alpha) + ')'
            )
        )

    if "Crime" in selected_data:
        fig.add_scattermapbox(
            lat=cs['LAT'],
            lon=cs['LON'],
            mode='markers',
            name='Crimes',
            marker=go.scattermapbox.Marker(
                size=crime_size,
                color='rgba(239,85,59,' + str(crime_alpha) + ')'
            )
        )

    if "Hospitals" in selected_data:
        fig.add_scattermapbox(
            lat=hospital_la['latitude'],
            lon=hospital_la['longitude'],
            mode='markers',
            name='Hospitals',
            marker=go.scattermapbox.Marker(
                size=hospitals_marker_size,
                color='rgba(0,204,150,' + str(hospitals_marker_alpha) + ")"
            )
        )

    if "Social Places" in selected_data:
        fig.add_scattermapbox(
            lat=la_places['lat'],
            lon=la_places['lon'],
            mode='markers',
            name='Social Places',
            marker=go.scattermapbox.Marker(
                size=social_marker_size,
                color='rgba(255,255,0,' + str(social_marker_alpha) + ")"
            )
        )

    fig.update_layout(
        autosize=False,
        width=750,
        height=750,
        hovermode='closest',
        mapbox=dict(
            accesstoken=mapbox_access_token,
            bearing=0,
            center=dict(
                lat=34.02,
                lon=-118.43
            ),
            pitch=0,
            zoom=9
        ),
    )

    st.plotly_chart(fig, use_container_width=False)


st.set_page_config(page_title="Heat Maps", page_icon="🗺️")
# st.markdown("## Heat Maps")
st.sidebar.header("Heat Maps")


mapbox_access_token = "pk.eyJ1IjoibWFwYm94c2VvIiwiYSI6ImNsZHo0ejU0dzBxMHAzb292Ym41Yzk4bzMifQ.ZYVGCdm8E2kH2QGi2gd9ng"
park = get_data("Datasets_raw/park_facilities_la.csv")
cs = get_data("Datasets_raw/crime_all.csv", sample=True, sample_size=0.04)
cs_sample = cs
hospital_la = get_data('Datasets_raw/hospital_facility_la.csv')
la_places = get_data("Datasets_raw/LA_places_cleaned.csv",
                     sample=True, sample_size=0.1)

neighborhoods = gpd.read_file(
    'Datasets_raw/l.a. county neighborhood (current).shp')


# neighborhood_names = []
# for name in neighborhoods['slug']:
#     name = name.replace('-', ' ')
#     neighborhood_names.append(name.title())


selected_data = st.multiselect(
    'Select if you want to see more or less data 👇️:',
    ['Parks', 'Crime', 'Hospitals', 'Social Places'],
    ['Parks', 'Crime'])

selected_neighb = st.multiselect(
    'Select if you want to draw neighborhood boundaries 👇️:',
    neighborhoods['name'],
    max_selections=1
)


parks_marker_size = 9
parks_marker_alpha = 0.7

crime_marker_size = 7
crime_marker_alpha = 0.01
crime_years = (2010, 2023)

hospitals_marker_size = 9
hospitals_marker_alpha = 0.7

social_marker_size = 7
social_marker_alpha = 0.1

st.sidebar.success("Filter data below 👇️")

if "Parks" in selected_data:

    st.sidebar.header("Parks")
    parks_marker_size = st.sidebar.slider('Parks Marker Size:', 1, 15, 9)
    parks_marker_alpha = st.sidebar.slider(
        'Parks Marker Opacity:', 0.0, 1.0, 0.7, 0.1)

if "Crime" in selected_data:

    st.sidebar.header("Crime")
    crime_marker_size = st.sidebar.slider('Crime Marker Size:', 1, 15, 7)
    crime_marker_alpha = st.sidebar.slider(
        'Crime Marker Opacity:', 0.0, 0.1, 0.01, 0.01)
    crime_years = st.sidebar.slider(
        'Crime Years:', 2010, 2023, (2010, 2023))


if "Hospitals" in selected_data:

    st.sidebar.header("Hospitals")
    hospitals_marker_size = st.sidebar.slider(
        'Hospitals Marker Size:', 1, 15, 9)
    hospitals_marker_alpha = st.sidebar.slider(
        'Hospitals Marker Opacity:', 0.0, 1.0, 0.7, 0.1)


if "Social Places" in selected_data:

    st.sidebar.header("Social Places")
    social_marker_size = st.sidebar.slider(
        'Social Places Marker Size:', 1, 15, 7)
    social_marker_alpha = st.sidebar.slider(
        'Social Places Marker Opacity:', 0.0, 1.0, 0.1, 0.1)

fig = st.empty()

make_map(
    selected_data,
    fig,
    park,
    cs,
    cs_sample,
    parks_marker_size,
    parks_marker_alpha,
    crime_marker_size,
    crime_marker_alpha,
    crime_years,
    hospitals_marker_size,
    hospitals_marker_alpha,
    social_marker_size,
    social_marker_alpha,
    selected_neighb
)

if "Parks" in selected_data:
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
            'y': 0.99,
            'x': 0.6,
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


if "Crime" in selected_data:
    crime_occ = pd.read_csv('final_dataset/LA_crime_occ.csv')
    if crime_years[0] != 2010 or crime_years[1] != 2023:
        # crime_occ['year'] = pd.to_datetime(crime_occ['year'])
        crime_occ = crime_occ[crime_occ["year"].le(
            crime_years[1]-1) & crime_occ["year"].ge(crime_years[0])]
        # crime_occ = crime_occ[(crime_occ.year >=
        #   crime_years[0]) & (crime_occ.year < crime_years[1])]
        print(crime_occ)

    fig = px.line(crime_occ, x='year', y='occurences', markers=True)
    fig.update_layout(plot_bgcolor='white')
    fig.update_layout(
        title={
            'text': "Los Angeles County Crime occurences trend",
            'y': 0.99,
            'x': 0.6,
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
