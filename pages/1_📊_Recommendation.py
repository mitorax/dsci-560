

import streamlit as st
import pandas as pd
import altair as alt
from urllib.error import URLError


rec_df=pd.read_csv("final_dataset/rec_df.csv")

def run_model(selected):
    print(rec_df.head())
    # st.write("Running recommendation model with interests:")
    # for item in selected:
    #     st.write(item)

def recommendation():
    @st.cache_data
    def get_interests():

        return ['Income (<$60k)', 'Income (<$100k)',  'Income (>$100k)',
                'Proximity to Social Places', "Proximity to Parks", "Proximity to Hospitals",
                'Less Population Density', 'High Population Density']

    try:
        interests = get_interests()
        selected = st.multiselect(
            "Choose Preferences 👇️", interests, [
                "Proximity to Parks"]
        )
        if not selected:
            st.error("Please select at least one preferences.")
        else:
            st.write("")
            st.write("Running recommendation model with Preferences:")
            for item in selected:
                st.write(item)

            if st.button("Get Results", type='primary'):
                run_model(selected)

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
