import streamlit as st
import streamlit.components.v1 as components
from streamlit.logger import get_logger

LOGGER = get_logger(__name__)


def run():

    st.set_page_config(
        page_title="Project-Name",
        page_icon="🏠️",
    )
    st.sidebar.text("")
    st.sidebar.success("👆️ Select an option above")
    st.sidebar.text("")
    st.sidebar.text("©️2023 Data Trojans")

    st.write("# Welcome to [Project-Name]! 👋")

    st.markdown(
        """
			[Project-Name] is built for helping people find the best area to live in based on personal preferences.

    	"""
    )

    st.text("")

    st.markdown(
        """
            Whether you want to settle in as a young family, work hard and save up money, live a balanced life, [Project-Name] provides you with the tools to find a place to live that will support you in that lifestyle.
        """
    )

    st.text("")

    st.markdown(
        """
            **👈 Select an option from the sidebar** to see what [Project-Name] can do!
        """
    )

    st.text("")

    st.markdown(
        """
			### What you can do with [Project-Name]:
			- Get a recommendation on living areas based on your preferences
			- Future trends forecasting on living areas
			- Explore the data and discover on your own
		"""
    )

    st.text("")

    video_file = open('Assets/stars-6962.mp4', 'rb')
    video_bytes = video_file.read()
    st.video(video_bytes)

    st.text("")

    st.markdown(
        """
			##### 👉️ Check out [the GitHub repo](https://github.com/mitorax/dsci-560-project)
		"""
    )


if __name__ == "__main__":
    run()
