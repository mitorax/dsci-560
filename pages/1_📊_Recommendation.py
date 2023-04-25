

import streamlit as st
import pandas as pd
import altair as alt
from urllib.error import URLError


rec_df=pd.read_csv("final_dataset/rec_df.csv")


def run_model(dense, income_s, selected):
    df= select_income(income_s[0])
    df= select_density(dense[0],df)
    
    df = df.sort_values(by=[selected[0]], ascending=False)
    df=df.drop(columns=['income'])
    st.dataframe(df)
    # st.write("Running recommendation model with interests:")
    # for item in selected:
    #     st.write(item)

def select_income(income_s):
    if income_s == 'Income (<$60k)':
        income_df = rec_df.loc[rec_df['income']<=30000].reset_index(drop=True)
    elif income_s == 'Income (<$100k)':
        x = rec_df.loc[rec_df['income']>30000].reset_index(drop=True)
        income_df = x.loc[x['income']<=45000].reset_index(drop=True)
    elif income_s == 'Income (>$100k)':
        income_df = rec_df.loc[rec_df['income']>45000].reset_index(drop=True)

    return income_df

def select_density(density_s,dff):
    if density_s == 'Less Population Density':
        density_df = dff.loc[dff['Population Density score']<0.3].reset_index(drop=True)
    elif density_s == 'High Population Density':
        density_df = dff.loc[dff['Population Density score']>=0.3].reset_index(drop=True)

    return density_df

def recommendation():
    @st.cache_data
    def get_interests():

        return ["Proximity to Social Places", "Proximity to Parks", "Proximity to Hospitals"]

    def get_income():

        return ['Income (<$60k)', 'Income (<$100k)',  'Income (>$100k)']

    def get_dense():

        return ['Less Population Density', 'High Population Density']

    try:
        interests = get_interests()
        incomes = get_income()
        density_pre = get_dense()

        income_selected = st.multiselect(
            "Choose one Affordability level 👇️", incomes, [
                "Income (<$60k)"]
        )
        selected = st.multiselect(
            "Choose Neighborhood Preferences, in order 👇️", interests, [
                "Proximity to Parks"]
        )
        density = st.multiselect(
            "Choose Population Density Preferences 👇️", density_pre, [
                'Less Population Density']
        )
        if not selected:
            st.error("Please select at least one preferences.")
        if not income_selected:
            st.error("Please select at least one Affordability level.")
        if not density:
            st.error("Please select at least one Population density level.")
        if len(income_selected) >1:
            st.error("Please select only one Affordability level.")
        if len(density) >1:
            st.error("Please select only one Population density level.")
        else:
            st.write("")
            st.write("Running recommendation model with Preferences:")
            for item in income_selected:
                st.write(item)
            for item in selected:
                st.write(item)
            for item in density:
                st.write(item)

            if st.button("Get Results", type='primary'):
                run_model(density, income_selected, selected)

    except URLError as e:
        st.error(
            """
            **Something went wrong: %s
        """
            % e.reason
        )


st.set_page_config(page_title="Recommendation", page_icon="📊")
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

st.markdown("# Recommendation")
# st.sidebar.header("Recommendation")
# st.sidebar.text("[add descritption]")
st.write(
    """Choose below what you are interested in when looking for a place to live and see what recommendations you will get based on that"""
)
st.write("")

recommendation()
