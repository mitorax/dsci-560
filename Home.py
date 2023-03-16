import streamlit as st
import streamlit.components.v1 as components
from streamlit.logger import get_logger

LOGGER = get_logger(__name__)


def run():

    st.set_page_config(
        page_title="Home",
        page_icon="🏠️",
    )

    st.sidebar.success("👆️ Select an option above")

    st.write("# Welcome to [Project-Name]! 👋")

    st.markdown(
        """
			[Project-Name] is an app built specifically for [placeholder].
   
			**👈 Select an option from the sidebar** to see what [Project-Name] can do!
   
    	"""
    )

    st.text("")

    st.markdown(
        """
			### What you can do with [Project-Name]:
			- [Feature]
			- [Feature]
			- [Feature]
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
