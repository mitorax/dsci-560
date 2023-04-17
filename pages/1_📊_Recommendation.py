

import streamlit as st
import pandas as pd
import altair as alt
from urllib.error import URLError


def run_model(selected):
    st.write("Running recommendation model with interests:")
    for item in selected:
        st.write(item)


def recommendation():
    @st.cache_data
    def get_interests():

        return ['Interest1', "Interest2", "Interest3"]

    try:
        interests = get_interests()
        selected = st.multiselect(
            "Choose interests 👇️", interests, [
                "Interest1"]
        )
        if not selected:
            st.error("Please select at least one interest.")
        else:
            st.write("")
            st.write("Running recommendation model with interests:")
            for item in selected:
                st.write(item)

            # if st.button("Get Results", type='primary'):
            #     run_model(selected)

    except URLError as e:
        st.error(
            """
            **Something went wrong: %s
        """
            % e.reason
        )


st.set_page_config(page_title="Recommendation", page_icon="📊")
st.markdown("# Recommendation")
st.sidebar.header("Recommendation")
st.sidebar.text("[add descritption]")
st.write(
    """Choose below what you are interested in when looking for a place to live and see what recommendations you will get based on that"""
)
st.write("")

recommendation()
