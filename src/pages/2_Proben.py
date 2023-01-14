
from pathlib import Path

import streamlit as st
from PIL import Image

from hero import Hero
from twinkle import Twinkle


image = Image.open(Path.cwd() / "resources" / "dsa_logo.png")
st.sidebar.image(image)

st.markdown(
    """
    # Bestreite Proben
    """
)

attributes_container = st.container()

skill_container = st.container()

twinkle_container = st.container()
