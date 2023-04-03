

import streamlit as st
import pandas as pd
import pydeck as pdk
import plotly.graph_objects as go


from urllib.error import URLError


def mapping_demo():
    @st.cache_data
    def from_data_file(filename):
        url = (
            "http://raw.githubusercontent.com/streamlit/"
            "example-data/master/hello/v1/%s" % filename
        )
        return pd.read_json(url)

    try:
        ALL_LAYERS = {
            "Bike Rentals": pdk.Layer(
                "HexagonLayer",
                data=from_data_file("bike_rental_stats.json"),
                get_position=["lon", "lat"],
                radius=200,
                elevation_scale=4,
                elevation_range=[0, 1000],
                extruded=True,
            ),
            "Bart Stop Exits": pdk.Layer(
                "ScatterplotLayer",
                data=from_data_file("bart_stop_stats.json"),
                get_position=["lon", "lat"],
                get_color=[200, 30, 0, 160],
                get_radius="[exits]",
                radius_scale=0.05,
            ),
            "Bart Stop Names": pdk.Layer(
                "TextLayer",
                data=from_data_file("bart_stop_stats.json"),
                get_position=["lon", "lat"],
                get_text="name",
                get_color=[0, 0, 0, 200],
                get_size=15,
                get_alignment_baseline="'bottom'",
            ),
            "Outbound Flow": pdk.Layer(
                "ArcLayer",
                data=from_data_file("bart_path_stats.json"),
                get_source_position=["lon", "lat"],
                get_target_position=["lon2", "lat2"],
                get_source_color=[200, 30, 0, 160],
                get_target_color=[200, 30, 0, 160],
                auto_highlight=True,
                width_scale=0.0001,
                get_width="outbound",
                width_min_pixels=3,
                width_max_pixels=30,
            ),
        }
        st.sidebar.markdown("### Map Layers")
        selected_layers = [
            layer
            for layer_name, layer in ALL_LAYERS.items()
            if st.sidebar.checkbox(layer_name, True)
        ]
        if selected_layers:
            st.pydeck_chart(
                pdk.Deck(
                    map_style="mapbox://styles/mapbox/light-v9",
                    initial_view_state={
                        "latitude": 37.76,
                        "longitude": -122.4,
                        "zoom": 11,
                        "pitch": 50,
                    },
                    layers=selected_layers,
                )
            )
        else:
            st.error("Please choose at least one layer above.")
    except URLError as e:
        st.error(
            """
            **This demo requires internet access.**
            Connection error: %s
        """
            % e.reason
        )


st.set_page_config(page_title="Heat Maps", page_icon="🗺️")
st.markdown("# Heat Maps")
st.sidebar.header("Heat Maps")
st.write(
    """Select which heat map you want to look at from the tabs below 👇️"""
)


tab1, tab2 = st.tabs(
    ["Crime vs Parks", "Medical Facilities"])

with tab1:

    mapbox_access_token = "pk.eyJ1IjoibWFwYm94c2VvIiwiYSI6ImNsZHo0ejU0dzBxMHAzb292Ym41Yzk4bzMifQ.ZYVGCdm8E2kH2QGi2gd9ng"
    park = pd.read_csv("Datasets_raw/park_facilities_la.csv")
    cs = pd.read_csv("Datasets_raw/crime_data_la.csv")
    fig = go.Figure(go.Scattermapbox(
        lat=park['GeoLat'],
        lon=park['GeoLong'],
        mode='markers',
        name='Parks',
        marker=go.scattermapbox.Marker(
            size=5,
            color='rgba(99,110,250,0.7)'
        )
    ))

    fig.add_scattermapbox(
        lat=cs['LAT'],
        lon=cs['LON'],
        mode='markers',
        name='Crimes',
        marker=go.scattermapbox.Marker(
            size=3,
            color='rgba(239,85,59, 0.02)'
        )
    )

    fig.update_layout(
        autosize=True,
        hovermode='closest',
        title_text='Location of Parks and Crimes in LA county',
        title_x=0.5,
        mapbox=dict(
            accesstoken=mapbox_access_token,
            bearing=0,
            center=dict(
                lat=34.05575695805104,
                lon=-118.26479036698463
            ),
            pitch=0,
            zoom=9
        ),
    )

    st.plotly_chart(fig, use_container_width=True)

# mapping_demo()
